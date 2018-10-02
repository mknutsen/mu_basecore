##
## Script to Build Project Mu compliant packages
##
##
## Copyright Microsoft Corporation, 2018
##
import os
import sys
import logging
import json
import glob
import stat
import subprocess
import shutil
import struct
from datetime import datetime
from datetime import date
import time
import copy
import csv
import time
import pkgutil
import importlib
import argparse


#==========================================================================
# PLATFORM BUILD ENVIRONMENT CONFIGURATION
#
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__)) 
#Project Mu requires BaseCore to be located at <workspace/SM_BASECORE
BASECORE_PATH = os.path.dirname(os.path.dirname(SCRIPT_PATH)) # we assume that we are in UefiBuild/CoreBuild and that SM_BASECORE has been cloned in it's entirety?
PROJECT_MU_UEFI_BUILD_PATH = os.path.join(BASECORE_PATH, "UefiBuild")
PROJECT_MU_BASETOOLS_BUILD_PATH = os.path.join(BASECORE_PATH, "BaseTools")
PROJECT_MU_BASETOOLS_PYLIB_BUILD_PATH = os.path.join(BASECORE_PATH, "BaseTools","PythonLibrary")
sys.path.append(PROJECT_MU_UEFI_BUILD_PATH)
sys.path.append(PROJECT_MU_BASETOOLS_BUILD_PATH)
sys.path.append(PROJECT_MU_BASETOOLS_PYLIB_BUILD_PATH)


logfile = None
#
#==========================================================================
#
##

IgnoreList = [  "nt32pkg.dsc",                      #NT32 pkg requires windows headers which are not supplied on build system
                "Nt32PkgMsCapsule.dsc",             #NT32 capsule pkg requires windows headers which are not supplied on build system
                "IntelFrameworkModulePkg.dsc",      #Plan to depricate
                "IntelFrameworkPkg.dsc",            #Plan to depricate
                "ArmCrashDumpDxe.dsc",               ## 
                "ArmPkg.dsc",
                "ArmPlatformPkg.dsc",
                "ArmVirtQemu.dsc",                  ## Requires OvmfPkg, which we don't want yet.
                "ArmVirtQemuKernel.dsc",            ## Requires OvmfPkg, which we don't want yet.
                "ArmVirtXen.dsc",                   ## Requires OvmfPkg, which we don't want yet.
                "EmbeddedPkg.dsc",
                "MsSampleFmpDevicePkg.dsc",         #Sample package requires user input to build
                "MicrocodeCapsulePdb.dsc",          #Not buildable
                "MicrocodeCapsuleTxt.dsc",          #Not buildable
                "vtf.inf",                          #Not buildable - Shares GUID with resetvector
                "vtf0.inf",                         #Not buildable - Shares GUID with resetvector
                "microcode.inf",                    #Not buildable - No sources
                "useridentifymanagerdxe.inf",       #Template with #error
                "pwdcredentialproviderdxe.inf",     #Template with #error
                "usbcredentialproviderdxe.inf",     #Template with #error
                "openssllib",                       #Third party lib that does not follow library header practice
                "intrinsiclib",                     #Lib that does not follow library header practice
                "logodxe.inf",                      #Temporarily ignored due to idf file
                "opalpassworddxe.inf",              #Temproarily ignored awaiting refactor
                "tcg2configdxe.inf",                #Temproarily ignored awaiting refactor
                "SafeIntLibUnitTests.inf",          #Ignore this unit test for now, in future we'll ignore all of them
                "ArmMmuLib",                        #Remove this once ArmPkg is added to code tree
                "ArmPkg/ArmPkg.dec"                 #Remove this once ArmPkg is added to code tree
]

import Tests.BaseTestLib
from Tests.XmlArtifact import XmlOutput
import ShellEnvironment

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

loghandle = None
TEMP_MODULE_DIR = "temp_modules"



# function that strips comments from a json files
def strip_json_from_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
        out = ""
        for a in lines:
            a = a.partition("//")[0]
            a = a.rstrip()
            out += a
        return out



##
## Script to Build CORE UEFI firmware
##
##
## Copyright Microsoft Corporation, 2015
##

IgnoreList = [  "nt32pkg.dsc",                      #NT32 pkg requires windows headers which are not supplied on build system
                "Nt32PkgMsCapsule.dsc",             #NT32 capsule pkg requires windows headers which are not supplied on build system
                "IntelFrameworkModulePkg.dsc",      #Plan to depricate
                "IntelFrameworkPkg.dsc",            #Plan to depricate
                "ArmCrashDumpDxe.dsc",               ## 
                "ArmPkg.dsc",
                "ArmPlatformPkg.dsc",
                "ArmVirtQemu.dsc",                  ## Requires OvmfPkg, which we don't want yet.
                "ArmVirtQemuKernel.dsc",            ## Requires OvmfPkg, which we don't want yet.
                "ArmVirtXen.dsc",                   ## Requires OvmfPkg, which we don't want yet.
                "EmbeddedPkg.dsc",
                "MsSampleFmpDevicePkg.dsc",         #Sample package requires user input to build
                "MicrocodeCapsulePdb.dsc",          #Not buildable
                "MicrocodeCapsuleTxt.dsc",          #Not buildable
                "vtf.inf",                          #Not buildable - Shares GUID with resetvector
                "vtf0.inf",                         #Not buildable - Shares GUID with resetvector
                "microcode.inf",                    #Not buildable - No sources
                "useridentifymanagerdxe.inf",       #Template with #error
                "pwdcredentialproviderdxe.inf",     #Template with #error
                "usbcredentialproviderdxe.inf",     #Template with #error
                "openssllib",                       #Third party lib that does not follow library header practice
                "intrinsiclib",                     #Lib that does not follow library header practice
                "logodxe.inf",                      #Temporarily ignored due to idf file
                "opalpassworddxe.inf",              #Temproarily ignored awaiting refactor
                "tcg2configdxe.inf",                #Temproarily ignored awaiting refactor
                "SafeIntLibUnitTests.inf",          #Ignore this unit test for now, in future we'll ignore all of them
                "ArmMmuLib",                        #Remove this once ArmPkg is added to code tree
                "ArmPkg/ArmPkg.dec"                 #Remove this once ArmPkg is added to code tree
]


Test_List = list() #Default test list


class Summary():
    def __init__(self):
        self.errors = list()
        self.warnings = list()
        self.results = list()
        self.layers = 0

    def PrintStatus(self, loghandle = None):
        logging.critical("\n\n\n************************************************************************************************************************************\n" + \
                            "************************************************************************************************************************************\n" + \
                            "************************************************************************************************************************************\n\n")

        logfile,loghandle = SetLogFile("BUILDLOG_SUMMARY.txt", loghandle)

        logging.critical("\n_______________________RESULTS_______________________________\n")
        for layer in self.results:
            logging.critical("")
            for result in layer:
                logging.critical(result)

        logging.critical("\n_______________________ERRORS_______________________________\n")
        for layer in self.errors:
            logging.critical("")
            for error in layer:
                logging.critical("ERROR: " + error)

        logging.critical("\n_______________________WARNINGS_____________________________\n")
        for layer in self.warnings:
            logging.critical("")
            for warning in layer:
                logging.critical("WARNING: " + warning)

    def AddError(self, error, layer = 0):
        if len(self.errors) <= layer:
            self.AddLayer(layer)
        self.errors[layer].append(error)

    def AddWarning(self, warning, layer = 0):
        if len(self.warnings) <= layer:
            self.AddLayer(layer)
        self.warnings[layer].append(warning)

    def AddResult(self, result, layer = 0):
        if len(self.results) <= layer:
            self.AddLayer(layer)
        self.results[layer].append(result)

    def AddLayer(self, layer):
        self.layers = layer
        while len(self.results) <= layer:
            self.results.append(list())

        while len(self.errors) <= layer:
            self.errors.append(list())

        while len(self.warnings) <= layer:
            self.warnings.append(list())

    def NumLayers(self):
        return self.layers

#Implementation for platform wide tests
def RunPlatformTests(test_list, workpath, packagepath, ignore_list = None):
    pass

##
# Walks until it finds a .dependencies and generates a list of packages we need to find
# returns an empty array if it can't find anything
##
def GenerateModulesDependencies(module, workspace = None):

    global ws
    if workspace is None:
        workspace = ws

    modules = []
    
    currentDir = module
    if os.path.isfile(currentDir):
        currentDir = os.path.dirname(currentDir)

    # make sure we add the module that we are currently in
    #TODO: use git toplevel instead?
    #WARNING: this uses the assumption that it will be named SM_ something
    findSMRoot = currentDir

    while not os.path.basename(findSMRoot).startswith("SM_"):
        findSMRoot = os.path.dirname(findSMRoot)
        #logging.critical("Scanning for git folder: %s"%os.path.basename(findSMRoot)[0:2])
        if os.path.dirname(findSMRoot) == findSMRoot:
           break
    
    if not os.path.dirname(findSMRoot) == findSMRoot:
        modules.append(findSMRoot)

    while not os.path.isfile(os.path.join(currentDir,".depends")):
        currentDir = os.path.dirname(currentDir)
        #logging.critical("Scanning Dependency file: %s"%currentDir)
        if os.path.dirname(currentDir) == currentDir:
            return modules
    
    #we have our currentDir -> read in the dependencies
    logging.info("Loading Module Dependency file: %s"%currentDir)

    dependencies = ReadDependencyFile(os.path.join(currentDir,".depends"))

    #find the folder of each module that our dependency file specified
    for module in dependencies:
        path = FindModule(ws,module["name"],module["url"])
        if path is None:
            logging.info("Unable to find: %s. Cloning " % module)
            path = CloneModule(ws,module["name"],module["url"], module["branch"], module["commit"])
        if path is None:
            logging.critical("Unable to find: %s. Cloning failed " % module)
        else:#we found the path
            modules.append(path)
    return modules

##
# reads the .depends files. An example of the file format
#[Common/SM_MU_TIANO_PLUS]
#	url = https://github.com/Microsoft/mu_tiano_plus.git
#    branch = release/20180529
#    commit = 5d4a51b4a8d20e5ff1f75adeb969697b1cc201cb
##
def ReadDependencyFile(file):
    
    try:
        file = open(file,'r')
        line = file.readline()
        modules = []        
        while not line == "":
            line = line.strip()
            if line[0] == '[':                
                modules.insert(0,{"name":line[1:-1]})
            elif "=" in line:
                defines = line.split("=")
                key = defines[0].strip()
                value = defines[1].strip()
                modules[0][key] = value #insert into the 
            else:
                logging.warn("Malformatted line in dependency file: %s" % line )
            line = file.readline() #read in a new file
        
        return modules
    except IOError as e:
        logging.critical("Unable to open file %s" % infFile)
        return []

##
# finds the module requested from the workspace- we assume that it is here at some point
def FindModule(ws,module, url):
    currentDir = ws
    if os.path.isfile(currentDir):
        currentDir = os.path.dirname(currentDir)
    for Root, Dirs, Files in os.walk(ws):
        #look for the directory module if we don't find it, we clone it
        for directory in Dirs: 
            #todo read the git information in the directory we find and make sure it matches the URL we find
            if directory == module:
                return os.path.join(Root,directory)
            #logging.info(os.path.join(Root,directory))

    return None
    

def CloneModule(ws,module, url, branch, commit):
    tempdir = os.path.join(ws,TEMP_MODULE_DIR)
    if not os.path.isdir(tempdir):
        os.mkdir(tempdir)
    dest = os.path.join(tempdir,module)
    
    cmd = "git clone --depth 1 --shallow-submodules --recurse-submodules -b %s %s %s " % (branch, url, dest)
    logging.info("Cloning into %s" % dest)
    p = subprocess.Popen(cmd, shell=True)
    p.wait()
    return dest

##
# Add a filehandler to the current logger
# If a loghandle is passed in then close that loghandle
##
def SetLogFile(filename, loghandle = None):
    if loghandle is not None:
        loghandle.close()
        logging.getLogger('').removeHandler(loghandle)

    logfile = os.path.join(ws, "Build", "BuildLogs", filename)
    if(not os.path.isdir(os.path.dirname(logfile))):
        os.makedirs(os.path.dirname(logfile))

    filelogger = logging.FileHandler(filename=(logfile), mode='w')
    filelogger.setLevel(logging.DEBUG)
    filelogger.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
    logging.getLogger('').addHandler(filelogger)
    logging.info("Log Started: " + datetime.strftime(datetime.now(), "%A, %B %d, %Y %I:%M%p" ))
    logging.info("Running Python version: " + str(sys.version_info))
    return logfile,filelogger

#Run test for platform
#test to run
#ws workspace
#pp package path
#args is sys.argv
#ignoreList = modules to ignore
#env is enviroment setup

def RunTest(test, ws, pp, args, ignoreList=[], env=None, summary = None, xmlartifact = None):
    
    if test is None:
        return 0

    overall_success = False
    logging.critical("\n\n------------------------------------------------------------------------------------------------------------------------------------\n")
    try:
        test_object = test(ws, pp, args, ignoreList, env, summary, xmlartifact)
        ret = test_object.RunTest()
        if (ret != 0):
            logging.critical("Test Failure")
            
        else:
            logging.critical("Test Success")
            overall_success = True

        logging.critical("\n\n__________________________________________________________________\n")
    except Exception:
        logging.error("EXCEPTION THROWN BY TEST")
        raise
    if overall_success:
        return 0
    else:
        return -1
    
class FindBuildableFiles(object):
    def __init__(self,dir):
        self._list = list()
        DSCFiles = list()
        for Root, Dirs, Files in os.walk(PKG_PATH):
            for File in Files:
                if File.lower().endswith('.dsc'):
                    if(File.lower() in IgnoreList) or File.lower().endswith(".temp.dsc"):
                        logging.debug("%s - Ignored" % File)
                        continue                    
                    self._list.append(os.path.join(Root, File))
                if File.lower().endswith('.mu.dsc.json'): #temporarily turned off
                    fileWoExtension = os.path.splitext(os.path.basename(str(File)))[0]
                    dscFile = os.path.join(Root, fileWoExtension+ ".temp.dsc")
                    from GenerateDSC import JsonToDSCGenerator 
                    JsonToDSCGenerator(os.path.join(Root,File)).write(dscFile)
                    #DSCFiles.append(dscFile)
                
    def __iter__(self):
        return iter(self._list)

# Smallest 'main' possible. Please don't add unnecessary code.
if __name__ == '__main__':

    #get the <repo>.mu.json.
    # either no args are supplied and cwd is checked for *.mu.json
    # or its the first argument

    PROJECT_SCOPE = []
    REPO_MU_JSON = None
    if len(sys.argv) < 2:
        files = glob.glob("*.mu.json")
        if(len(files) >= 1):
            REPO_MU_JSON = os.path.abspath(files[0])
        else:
            print("No mu.json files found")
    else:
        REPO_MU_JSON = os.path.abspath(sys.argv[1])
        del sys.argv[1]

    if REPO_MU_JSON is None or not os.path.isfile(REPO_MU_JSON):
        raise Exception("Invalid path to <Repo>.mu.json file for build: %s", REPO_MU_JSON)
    
    #have a config file
    RepoConfig = json.loads(strip_json_from_file(REPO_MU_JSON))
    WORKSPACE_PATH = os.path.realpath(os.path.join(os.path.dirname(REPO_MU_JSON), RepoConfig["RelativeWorkspaceRoot"]))
    PROJECT_SCOPE = tuple(RepoConfig["Scopes"])
    print("Running ProjectMu Build: ", RepoConfig["Name"])
    print("WorkSpace: ", WORKSPACE_PATH)


    #Allow repo config to override
    if(RepoConfig.get("BaseCorePath") is not None):
        PROJECT_MU_UEFI_BUILD_PATH = os.path.join(WORKSPACE_PATH,RepoConfig["BaseCorePath"], "UefiBuild")

    print("Basecore: ", PROJECT_MU_UEFI_BUILD_PATH)


    # Include the most basic paths so that we can get to known build components.
    sys.path.append(os.path.join(WORKSPACE_PATH, PROJECT_MU_UEFI_BUILD_PATH))
    import CommonBuildEntry

    # Make sure that we can get some logging out.
    CommonBuildEntry.configure_base_logging('verbose')    

    ws = WORKSPACE_PATH
    pp = WORKSPACE_PATH
    bp = WORKSPACE_PATH

    #TODO add all argument parsing into here
    PKG_PATH = ws
    parser = argparse.ArgumentParser()
    parser.add_argument (
    '-p', '--pkg','--pkg-dir', dest = 'WorkSpace', required = False, type=str,
    help = '''Specify the absolute path to your workspace by passing -w WORKSPACE or --workspace WORKSPACE.'''
    )
    programArg0 = sys.argv[0]
    args, sys.argv = parser.parse_known_args() #consume the arguments we care about and then set the remaining arguments back to argv
    sys.argv.insert(0, programArg0)
    if args.WorkSpace:

        # pre-process the parsed paths to abspath
        args.WorkSpace = os.path.abspath(args.WorkSpace)
        if os.path.isfile(args.WorkSpace):
            args.WorkSpace =  os.path.dirname(args.WorkSpace)
        if not os.path.isdir(args.WorkSpace):
            raise RuntimeError("Workspace path is invalid.")
        PKG_PATH= args.WorkSpace

    # Make sure that we have a clean environment.
    if os.path.isdir(os.path.join(ws, "Build", "BuildLogs")):
        shutil.rmtree(os.path.join(ws, "Build", "BuildLogs"))

    #Import all tests
    pkg_dir = os.path.join(os.path.dirname(__file__), "Tests")
    for (module_loader, name, ispkg) in pkgutil.iter_modules([pkg_dir]):
        importlib.import_module('.' + name, package="Tests")

    #Create list of tests
    All_Tests = list()
    for item in Tests.BaseTestLib.BaseTestLibClass.__subclasses__():
        All_Tests.append((item.__name__, item))

    #Convert ignore list to lowercase
    for index,item in enumerate(IgnoreList):
        IgnoreList[index] = item.lower()

    #setup main console as logger
    logger = logging.getLogger('')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    console = logging.StreamHandler()

    #Create summary object
    summary_log = Summary()
    #Generate consumable XML object
    xml_artifact = XmlOutput()

    #Setup the main console logger differently if VSMODE is on.  
    # This allows more debug messages out
    # 
    levelset = False
    ignorefile_given = False
    testfile_given = False

    #TODO conver to to use arg parser
    for a in sys.argv:
        if (a == "--VSMODE"):
            console.setLevel(logging.DEBUG)
            console.setFormatter(logging.Formatter("%(message)s"))
            levelset = True
            sys.argv.remove(a)
        #Check if ignore file list is provided
        elif ("ignore_file=" in a.lower()):
            try:
                IgnoreFile = open(a.split('=', 1)[1], 'r')
                CsvReader = csv.reader(IgnoreFile)
            except:
                logging.error("Could not read Ignore File")
                sys.exit(-1)
            else:
                ignorefile_given = True
                IgnoreList_Not_Flat = list(CsvReader)
                #Flatten all rows into single list and lowercase
                IgnoreList_Flat = [Item for List_Sub in IgnoreList_Not_Flat for Item in List_Sub]
                for item in IgnoreList_Flat:
                    IgnoreList.append(item.lower())
                sys.argv.remove(a)
        #Check if test list file is probided
        elif ("test_list=" in a.lower()):
            try:
                TestFile = open(a.split('=', 1)[1], 'r')
                CsvReader = csv.reader(TestFile)
            except:
                logging.error("Could not read Test File")
                sys.exit(-1)
            else:
                testfile_given = True
                TestList_Not_Flat = list(CsvReader)
                #Flatten all rows into single list and lowercase
                TestList_Flat = [Item for List_Sub in TestList_Not_Flat for Item in List_Sub]
                for item in TestList_Flat:
                    for index,test in enumerate(All_Tests):
                        if item.lower() == test[0].lower():
                            Test_List.append(All_Tests[index])

                sys.argv.remove(a)
    #Run all tests

    #TODO why would we not run all the tests?
    if "--alltests" in str(sys.argv).lower():
        Test_List = copy.copy(All_Tests)

    #Setup default logging
    if(not levelset):
        console.setLevel(logging.CRITICAL)
        console.setFormatter(formatter)
    #logger.addHandler(console)

    overall_success = True
    logfile = os.path.join(ws, "Build", "BuildLogs", "BUILDLOG_MASTER.txt")
    logfile_master = copy.copy(logfile)
    if(not os.path.isdir(os.path.dirname(logfile))):
        os.makedirs(os.path.dirname(logfile))

    filelogger = logging.FileHandler(filename=(logfile), mode='w')
    filelogger.setLevel(logging.DEBUG)
    filelogger.setFormatter(formatter)
    logging.getLogger('').addHandler(filelogger)
    logging.info("Log Started: " + datetime.strftime(datetime.now(), "%A, %B %d, %Y %I:%M%p" ))
    logging.info("Running Python version: " + str(sys.version_info))

    testsRun = 0
    from VarDict import VarDict 
    #TODO create iterator that will figure out what we need to build
    for buildableFile in FindBuildableFiles(pkg_dir):
        #testsRun+= 1
        for testname,test in Test_List:
            logging.critical("Running {0} test on {1}".format(test,buildableFile))
            #setup the enviroment
            env = VarDict()
            
            env.SetValue("PRODUCT_NAME", "CORE", "Platform Hardcoded")
            env.SetValue("TARGET_ARCH", "IA32 X64", "Platform Hardcoded")
            env.SetValue("LaunchBuildLogProgram", "Notepad", "default - will fail if already set", True)
            env.SetValue("LaunchLogOnSuccess", "False", "default - do not log when successful")
            env.SetValue("LaunchLogOnError", "True", "default - will fail if already set", True)
            
            env.SetValue("ACTIVE_PLATFORM",buildableFile,"Override for building this DSC")
            '''
            # Bring up the common minimum environment.
            #CommonBuildEntry.update_process(BASECORE_PATH, PROJECT_SCOPE)
            '''
            #Run each test on it
            RunTest(test, ws,pp, sys.argv, IgnoreList, env, summary_log,xml_artifact)
            #figure out if we failed or not
            
   
    
    #Print Overall Success
    if(overall_success == False):
        logging.critical("Overall Build Status: Error")
        logging.critical("Log file at " + logfile)
    else:
        logging.critical("Overall Build Status: Success")

    #Print summary struct
    summary_log.PrintStatus(loghandle)
    xml_artifact.write_file(os.path.join(ws, "Build", "BuildLogs", "TestSuites.xml"))
    
    #end logging
    logging.shutdown()
    #no more logging

    
    if overall_success:
        sys.exit(0)
    else:
        sys.exit(-1)
