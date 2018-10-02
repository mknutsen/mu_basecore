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


#get path to self and then find SDE path
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__)) 
SDE_PATH = os.path.dirname(SCRIPT_PATH) #Path to SDE build env
sys.path.append(SDE_PATH)

import SelfDescribingEnvironment
import PluginManager

PROJECT_SCOPE = ("project_mu",)


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
def Setup_logging(root):
    from datetime import datetime
    from datetime import date
    
    #setup logger
    logger = logging.getLogger('')
    logger.setLevel(logging.DEBUG)

    #Create the main console as logger
    formatter = logging.Formatter("%(levelname)s- %(message)s")
    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)
    console.setFormatter(formatter)
    logger.addHandler(console)

    
    logfile = os.path.join(WORKSPACE_PATH, "Build", "BuildLogs", "BUILDLOG_MASTER.txt")
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
                        continue
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
    



#
# Main driver of Project Mu Builds
#
if __name__ == '__main__':

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

    if mu_pk_path is None:
        mu_pk_path = WORKSPACE_PATH

    Setup_logging(WORKSPACE_PATH)

    logging.debug("CAN YOU SEE ME")

    #Allow config to override
    #if(RepoConfig.get("BaseCorePath") is not None):
    #    PROJECT_MU_UEFI_BUILD_PATH = os.path.join(WORKSPACE_PATH,RepoConfig["BaseCorePath"], "UefiBuild")

    #print("Basecore: ", PROJECT_MU_UEFI_BUILD_PATH)


    # Include the most basic paths so that we can get to known build components.
    #sys.path.append(os.path.join(WORKSPACE_PATH, PROJECT_MU_UEFI_BUILD_PATH))
    import CommonBuildEntry

    # Bring up the common minimum environment.
    #CommonBuildEntry.update_process(WORKSPACE_PATH, PROJECT_SCOPE)
    
   

    # Finally, jump to the main routine.
    #PlatformBuildWorker.main(WORKSPACE_PATH, PROJECT_SCOPE)

    # The SDE should have already been initialized.
    # This call *should* only return the handles to the
    # pre-initialized environment objects.
    (build_env, shell_env) = SelfDescribingEnvironment.BootstrapEnvironment(WORKSPACE_PATH, PROJECT_SCOPE)

    pluginManager = PluginManager.PluginManager()
    pluginManager.SetListOfEnvironmentDescriptors(build_env.plugins)

    import ShellEnvironment

    for buildableFile in FindBuildableFiles(mu_pk_path):
        #
        # run all loaded MuBuild Plugins/Tests
        #
        print("\n-----------------------------------------------------------")
        print("Running against: {0}".format(buildableFile))
        for Descriptor in pluginManager.GetPluginsOfClass(PluginManager.IMuBuildPlugin):

            ShellEnvironment.ClearBuildVars()
            env = ShellEnvironment.GetBuildVars()

            CommonBuildEntry.update_process(WORKSPACE_PATH, PROJECT_SCOPE)
            
            env.SetValue("PRODUCT_NAME", "CORE", "Platform Hardcoded")
            env.SetValue("TARGET_ARCH", "IA32 X64", "Platform Hardcoded")
            env.SetValue("TARGET", "DEBUG", "Platform Hardcoded")
            env.SetValue("LaunchBuildLogProgram", "Notepad", "default - will fail if already set", True)
            env.SetValue("LaunchLogOnSuccess", "False", "default - do not log when successful")
            env.SetValue("LaunchLogOnError", "True", "default - will fail if already set", True)
            
            env.SetValue("ACTIVE_PLATFORM",buildableFile,"Override for building this DSC")

            MODULE_PACKAGES = list()
            MODULE_PACKAGES.append(WORKSPACE_PATH)
            module_pkg_paths = os.pathsep.join(pkg_name for pkg_name in MODULE_PACKAGES)
            
            #self, workspace="", packagespath="", args=[], ignorelist = None, environment = None, summary = None, xmlartifact = None
            rc = Descriptor.Obj.RunMu(WORKSPACE_PATH, module_pkg_paths,sys.argv,None,env)
            
            logging.warning("We aren't doing this correctly")

            if(rc != 0):
                if(rc is None):
                    logging.error("Plugin Failed: %s returned NoneType" % Descriptor.Name)
                    ret = -1
                else:
                    logging.error("Plugin Failed: %s returned %d" % (Descriptor.Name, rc))
                    ret = rc
            else:
                logging.debug("Plugin Success: %s" % Descriptor.Name)
