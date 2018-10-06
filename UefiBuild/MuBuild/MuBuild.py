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
BASECORE_PATH = os.path.dirname(SDE_PATH) # we assume that 


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
    parser.add_argument ('-c', '--mu_config', dest = 'mu_config', required = True, type=str, help ='Provide the Mu config relative to the current working directory')
    parser.add_argument (
    '-p', '--pkg','--pkg-dir', dest = 'pkg', required = False, type=str,help = 'The package or folder you want to test/compile relative to the Mu Config'
    )
    #programArg0 = sys.argv[0]
    args, sys.argv = parser.parse_known_args() 
    return args

#
# Main driver of Project Mu Builds
#
if __name__ == '__main__':

    #Parse command line arguments
    buildArgs = get_mu_config()
    mu_config_filepath = os.path.abspath(buildArgs.mu_config)
    mu_pk_path = buildArgs.pkg

    if mu_config_filepath is None or not os.path.isfile(mu_config_filepath):
        raise Exception("Invalid path to mu.json file for build: ", mu_config_filepath)
    
    #have a config file
    mu_config = json.loads(strip_json_from_file(mu_config_filepath))
    WORKSPACE_PATH = os.path.realpath(os.path.join(os.path.dirname(mu_config_filepath), mu_config["RelativeWorkspaceRoot"]))
    mu_config["Scopes"] = tuple(mu_config["Scopes"])
    
    PROJECT_SCOPE += mu_config["Scopes"]
    print("Running ProjectMu Build: ", mu_config["Name"])
    print("WorkSpace: ", WORKSPACE_PATH)
    print("Basecore Path: ",BASECORE_PATH)
    
    # if a package isn't specifed as needing to be built- we are going to 
    if mu_pk_path is None and mu_config["Packages"]:
        packageList = mu_config["Packages"]
    elif mu_pk_path:
        packageList = [mu_pk_path]
    else:
        packageList = []

    #Setup the logging to the file as well as the console
    MuLogging.clean_build_logs(WORKSPACE_PATH)
    MuLogging.setup_logging(WORKSPACE_PATH)
    
    # Bring up the common minimum environment.
    CommonBuildEntry.update_process(WORKSPACE_PATH, PROJECT_SCOPE)
    env = ShellEnvironment.GetBuildVars()
    
    #set up our enviroment
    env.SetValue("PRODUCT_NAME", "CORE", "Platform Hardcoded")
    env.SetValue("TARGET_ARCH", "IA32 X64", "Platform Hardcoded")
    env.SetValue("TARGET", "DEBUG", "Platform Hardcoded")
    
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

    logging.critical(packageList)
    for pkgToRunOn in packageList:
        #
        # run all loaded MuBuild Plugins/Tests
        #
        _, loghandle = MuLogging.setup_logging(WORKSPACE_PATH,"BUILDLOG_{0}.txt".format(pkgToRunOn))
        print("\n-----------------------------------------------------------")
        logging.info("\tPackage Running: {0}".format(pkgToRunOn))
        print("\tPackage Running: {0}".format(pkgToRunOn))
        print("\n-----------------------------------------------------------")
        ShellEnvironment.CheckpointBuildVars()
        env = ShellEnvironment.GetBuildVars()

        #find or generate the DSC for this particular package
        dscPath = PackageResolver.get_dsc_for_pacakge(pkgToRunOn,WORKSPACE_PATH)
        env.SetValue("ACTIVE_PLATFORM",dscPath,"Override for building this DSC")

        for Descriptor in pluginManager.GetPluginsOfClass(PluginManager.IMuBuildPlugin):
            
            total_num +=1
            ShellEnvironment.CheckpointBuildVars()
            env = ShellEnvironment.GetBuildVars()

            CommonBuildEntry.update_process(WORKSPACE_PATH, PROJECT_SCOPE)
            #Generate our module pcokages
            MODULE_PACKAGES = list() 
            MODULE_PACKAGES.append(WORKSPACE_PATH)
            if not BASECORE_PATH in MODULE_PACKAGES: #make sure we include basecore in our Module packages in case our workspace is somewhere else
                MODULE_PACKAGES.append(BASECORE_PATH)
            module_pkg_paths = os.pathsep.join(pkg_name for pkg_name in MODULE_PACKAGES)
            try:
                #self, workspace="", packagespath="", args=[], ignorelist = None, environment = None, summary = None, xmlartifact = None
                rc = Descriptor.Obj.RunBuildPlugin(pkgToRunOn,WORKSPACE_PATH, module_pkg_paths,sys.argv,list(),env, summary_log, xml_artifact)
            except Exception as exp:
                logging.critical(exp)
                summary_log.AddError("Exception thrown by {0} in package {1}\n{2}".format(Descriptor.Name,pkgToRunOn,str(exp)),2)
                rc = 1

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
        
        MuLogging.stop_logging(loghandle) #stop the logging for this particularbuild file
        ShellEnvironment.RevertBuildVars()
    #Finished builldable file loop

    
    #Print summary struct
    summary_log.print_status(WORKSPACE_PATH)
    #write the XML artifiact
    xml_artifact.write_file(os.path.join(WORKSPACE_PATH, "Build", "BuildLogs", "TestSuites.xml"))

    print("______________________________________________________________________")
      #Print Overall Success
    if(failure_num != 0):
        logging.critical("Overall Build Status: Error")
        logging.critical("There were {0} failures out of {1} attempts".format(failure_num,total_num))        
    else:
        logging.critical("Overall Build Status: Success")
    
