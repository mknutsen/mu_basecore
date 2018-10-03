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
import argparse
from datetime import datetime
from datetime import date
import subprocess
import shutil


#get path to self and then find SDE path
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__)) 
SDE_PATH = os.path.dirname(SCRIPT_PATH) #Path to SDE build env
sys.path.append(SDE_PATH)

import SelfDescribingEnvironment
import PluginManager
from XmlArtifact import XmlOutput
import CommonBuildEntry
import ShellEnvironment

PROJECT_SCOPE = ("project_mu",)
TEMP_MODULE_DIR = "temp_modules"


#
# To support json that has comments it must be preprocessed
#
def strip_json_from_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
        out = ""
        for a in lines:
            a = a.partition("//")[0]
            a = a.rstrip()
            out += a
        return out

def Setup_logging(filename=None, loghandle = None):

    if loghandle is not None:
        Stop_logging(loghandle)

    
    if filename is None:
        filename = "BUILDLOG_MASTER.txt"
    
    #setup logger
    logger = logging.getLogger('')
    logger.setLevel(logging.DEBUG)

    if len(logger.handlers) == 0:
        #Create the main console as logger
        formatter = logging.Formatter("%(levelname)s- %(message)s")
        console = logging.StreamHandler()
        console.setLevel(logging.WARNING)
        console.setFormatter(formatter)
        logger.addHandler(console)

    
    logfile = os.path.join(WORKSPACE_PATH, "Build", "BuildLogs", filename)
    if(not os.path.isdir(os.path.dirname(logfile))):
        os.makedirs(os.path.dirname(logfile))
    
    #Create master file logger
    fileformatter = logging.Formatter("%(levelname)s - %(message)s")
    filelogger = logging.FileHandler(filename=(logfile), mode='w')
    filelogger.setLevel(logging.DEBUG)
    filelogger.setFormatter(fileformatter)
    logger.addHandler(filelogger)
    logging.info("Log Started: " + datetime.strftime(datetime.now(), "%A, %B %d, %Y %I:%M%p" ))
    logging.info("Running Python version: " + str(sys.version_info))

    return logfile,filelogger

def Stop_logging(loghandle):
    loghandle.close()
    logging.getLogger('').removeHandler(loghandle)


def get_mu_config():
    parser = argparse.ArgumentParser(description='Run the Mu Build')
    parser.add_argument ('-c', '--mu_config', dest = 'mu_config', required = True, type=str, help ='Provide the Mu config ')
    parser.add_argument (
    '-p', '--pkg','--pkg-dir', dest = 'pkg', required = False, type=str,help = 'The package or folder you want to test/compile'
    )
    #programArg0 = sys.argv[0]
    args, sys.argv = parser.parse_known_args() 
    return args

# An iterator that you can iterate over the list of buildable files
class FindBuildableFiles(object):
    def __init__(self,PKG_PATH): #dir is the folder or file that we want to walk over
        self._list = list()
        DSCFiles = list()
        for Root, Dirs, Files in os.walk(PKG_PATH):
            for File in Files:
                if File.lower().endswith('.dsc'):
                    if File.lower().endswith(".temp.dsc"):
                        logging.debug("%s - Ignored" % File)
                    else:                  
                        self._list.append(os.path.join(Root, File))
                if File.lower().endswith('.mu.dsc.json'): #temporarily turned off
                    fileWoExtension = os.path.splitext(os.path.basename(str(File)))[0]
                    dscFile = os.path.join(Root, fileWoExtension+ ".temp.dsc")
                    from DSCGenerator import JsonToDSCGenerator 
                    JsonToDSCGenerator(os.path.join(Root,File)).write(dscFile)
                    #self._list.append(dscFile)
                    #DSCFiles.append(dscFile)
                
    def __iter__(self):
        return iter(self._list)



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

        logfile,loghandle = Setup_logging("BUILDLOG_SUMMARY.txt", loghandle)

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

##
# Walks until it finds a .dependencies and generates a list of packages we need to find
# returns an empty array if it can't find anything
##
def GenerateModulesDependencies(module, workspace):

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
        path = FindModule(workspace,module["name"],module["url"])
        if path is None:
            logging.info("Unable to find: %s. Cloning " % module)
            path = CloneModule(workspace,module["name"],module["url"], module["branch"], module["commit"])
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


#
# Main driver of Project Mu Builds
#
if __name__ == '__main__':

    #Parse command line arguments
    buildArgs = get_mu_config()
    mu_config_filepath = os.path.abspath(buildArgs.mu_config)
    mu_pk_path = os.path.abspath(buildArgs.pkg)

    if mu_config_filepath is None or not os.path.isfile(mu_config_filepath):
        raise Exception("Invalid path to mu.json file for build: ", mu_config_filepath)
    
    #have a config file
    mu_config = json.loads(strip_json_from_file(mu_config_filepath))
    WORKSPACE_PATH = os.path.realpath(os.path.join(os.path.dirname(mu_config_filepath), mu_config["RelativeWorkspaceRoot"]))
    if not isinstance(mu_config["Scopes"],tuple):
        mu_config["Scopes"] = tuple(mu_config["Scopes"])
    
    PROJECT_SCOPE += mu_config["Scopes"]
    print("Running ProjectMu Build: ", mu_config["Name"])
    print("WorkSpace: ", WORKSPACE_PATH)

    # if a package isn't specifed as needing to be built- we are going to 
    if mu_pk_path is None:
        mu_pk_path = WORKSPACE_PATH

    #Setup the logging to the file as well as the console
    Setup_logging()
    
    # Bring up the common minimum environment.
    CommonBuildEntry.update_process(WORKSPACE_PATH, PROJECT_SCOPE)
    
   
    # The SDE should have already been initialized.
    # This call *should* only return the handles to the
    # pre-initialized environment objects.
    (build_env, shell_env) = SelfDescribingEnvironment.BootstrapEnvironment(WORKSPACE_PATH, PROJECT_SCOPE)

    
    #Create summary object
    summary_log = Summary()
    #Generate consumable XML object
    xml_artifact = XmlOutput()

    failure_num = 0
    total_num = 0

    #Get our list of plugins
    pluginManager = PluginManager.PluginManager()
    pluginManager.SetListOfEnvironmentDescriptors(build_env.plugins)


    for buildableFile in FindBuildableFiles(mu_pk_path):
        #
        # run all loaded MuBuild Plugins/Tests
        #
        _, loghandle = Setup_logging("BUILDLOG_{0}.txt".format(os.path.basename(buildableFile)))
        print("\n------------------------------------- ----------------------")
        print("Running against: {0}".format(buildableFile))
        for Descriptor in pluginManager.GetPluginsOfClass(PluginManager.IMuBuildPlugin):

            
            total_num +=1
            ShellEnvironment.CheckpointBuildVars()
            env = ShellEnvironment.GetBuildVars()

            #set up our enviroment
            env.SetValue("PRODUCT_NAME", "CORE", "Platform Hardcoded")
            env.SetValue("TARGET_ARCH", "IA32 X64", "Platform Hardcoded")
            env.SetValue("TARGET", "DEBUG", "Platform Hardcoded")
            env.SetValue("LaunchBuildLogProgram", "Notepad", "default - will fail if already set", True)
            env.SetValue("LaunchLogOnSuccess", "False", "default - do not log when successful")
            env.SetValue("LaunchLogOnError", "True", "default - will fail if already set", True)
            
            env.SetValue("ACTIVE_PLATFORM",buildableFile,"Override for building this DSC")

            CommonBuildEntry.update_process(WORKSPACE_PATH, PROJECT_SCOPE)
            #Generate our module pcokages
            MODULE_PACKAGES = GenerateModulesDependencies(buildableFile, WORKSPACE_PATH)            
            MODULE_PACKAGES.append(WORKSPACE_PATH)
            module_pkg_paths = os.pathsep.join(pkg_name for pkg_name in MODULE_PACKAGES)
            
            #self, workspace="", packagespath="", args=[], ignorelist = None, environment = None, summary = None, xmlartifact = None
            rc = Descriptor.Obj.RunMu(WORKSPACE_PATH, module_pkg_paths,sys.argv,None,env, summary_log, xml_artifact)

            if(rc != 0):
                failure_num += 1
                if(rc is None):
                    logging.error("Test Failed: %s returned NoneType" % Descriptor.Name)
                    ret = -1
                else:
                    logging.error("Test Failed: %s returned %d" % (Descriptor.Name, rc))
                    ret = rc
            else:
                logging.debug("Test Success: %s" % Descriptor.Name)
            #revert to the checkpoint we created previously
            ShellEnvironment.RevertBuildVars()
        #Finished plugin loop
        Stop_logging(loghandle)
    #Finished builldable file loop

    print("______________________________________________________________________")
      #Print Overall Success
    if(failure_num != 0):
        logging.critical("Overall Build Status: Error")
        logging.critical("There were {0} failures out of {1} attempts".format(failure_num,total_num))        
    else:
        logging.critical("Overall Build Status: Success")
    
    #Print summary struct
    summary_log.PrintStatus()
    #write the XML artifiact
    xml_artifact.write_file(os.path.join(WORKSPACE_PATH, "Build", "BuildLogs", "TestSuites.xml"))
