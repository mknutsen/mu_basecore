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
import MuLogging
import PackageResolver

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
    def __init__(self,PKG_PATH, helper = None): #dir is the folder or file that we want to walk over
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
                    helper.generate_dsc_from_json(os.path.join(Root,File),dscFile)
                    #register as helper function
                    #from DSCGenerator import JsonToDSCGenerator 
                    #JsonToDSCGenerator(os.path.join(Root,File)).write(dscFile)
                    #self._list.append(dscFile)
                    #DSCFiles.append(dscFile)
                
    def __iter__(self):
        return iter(self._list)


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
    mu_config["Scopes"] = tuple(mu_config["Scopes"])
    
    PROJECT_SCOPE += mu_config["Scopes"]
    print("Running ProjectMu Build: ", mu_config["Name"])
    print("WorkSpace: ", WORKSPACE_PATH)

    # if a package isn't specifed as needing to be built- we are going to 
    if mu_pk_path is None:
        mu_pk_path = WORKSPACE_PATH

    #Setup the logging to the file as well as the console
    MuLogging.clean_build_logs(WORKSPACE_PATH)
    MuLogging.setup_logging(WORKSPACE_PATH)
    
    # Bring up the common minimum environment.
    CommonBuildEntry.update_process(WORKSPACE_PATH, PROJECT_SCOPE)
    
    # The SDE should have already been initialized.
    # This call *should* only return the handles to the
    # pre-initialized environment objects.
    (build_env, shell_env) = SelfDescribingEnvironment.BootstrapEnvironment(WORKSPACE_PATH, PROJECT_SCOPE)

    
    #Create summary object
    summary_log = MuLogging.Summary()
    #Generate consumable XML object
    xml_artifact = XmlOutput()

    failure_num = 0
    total_num = 0

    #Get our list of plugins
    pluginManager = PluginManager.PluginManager()
    pluginManager.SetListOfEnvironmentDescriptors(build_env.plugins)
    helper = PluginManager.HelperFunctions()
    helper.LoadFromPluginManager(pluginManager)

    for buildableFile in FindBuildableFiles(mu_pk_path,helper):
        #
        # run all loaded MuBuild Plugins/Tests
        #
        _, loghandle = MuLogging.setup_logging(WORKSPACE_PATH,"BUILDLOG_{0}.txt".format(os.path.basename(buildableFile)))
        print("\n-----------------------------------------------------------")
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
            MODULE_PACKAGES = PackageResolver.generate_modules_dependencies(buildableFile, WORKSPACE_PATH)
            MODULE_PACKAGES.append(WORKSPACE_PATH)
            module_pkg_paths = os.pathsep.join(pkg_name for pkg_name in MODULE_PACKAGES)
            
            #self, workspace="", packagespath="", args=[], ignorelist = None, environment = None, summary = None, xmlartifact = None
            rc = Descriptor.Obj.RunBuildPlugin(WORKSPACE_PATH, module_pkg_paths,sys.argv,list(),env, summary_log, xml_artifact)

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
        MuLogging.stop_logging(loghandle)
    #Finished builldable file loop

    print("______________________________________________________________________")
      #Print Overall Success
    if(failure_num != 0):
        logging.critical("Overall Build Status: Error")
        logging.critical("There were {0} failures out of {1} attempts".format(failure_num,total_num))        
    else:
        logging.critical("Overall Build Status: Success")
    
    #Print summary struct
    summary_log.print_status(WORKSPACE_PATH)
    #write the XML artifiact
    xml_artifact.write_file(os.path.join(WORKSPACE_PATH, "Build", "BuildLogs", "TestSuites.xml"))
