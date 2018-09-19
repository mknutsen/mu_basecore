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

#Project Mu requires BaseCore to be located at <workspace/SM_BASECORE
PROJECT_MU_UEFI_BUILD_PATH = os.path.join("SM_BASECORE", "UefiBuild")
#
#==========================================================================
# PLATFORM BUILD ENVIRONMENT CONFIGURATION
#
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__)) 
#WORKSPACE_PATH = os.path.dirname(os.path.dirname(SCRIPT_PATH))
BASECORE_PATH = os.path.dirname(os.path.dirname(SCRIPT_PATH)) # we assume that we are in UefiBuild/CoreBuild and that SM_BASECORE has been cloned in it's entirety?
#PKG_PATH = os.path.dirname(os.path.dirname(SCRIPT_PATH))
#PROJECT_SCOPE = ('corebuild',)

sys.path.append(os.path.join(BASECORE_PATH, 'UefiBuild'))

# MODULE_PKGS = ('SM_UDK', "SM_UDK_INTERNAL", "SURF_KBL", "SM_INTEL_KBL")
# MODULE_PKG_PATHS = ";".join(os.path.join(WORKSPACE_PATH, pkg_name) for pkg_name in MODULE_PKGS)
#
#==========================================================================
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

    # Bring up the common minimum environment.
    CommonBuildEntry.update_process(WORKSPACE_PATH, PROJECT_SCOPE)

    # Now that we've got the environment updated, we can bring in the worker.
    import PlatformBuildWorker

    # Tear down logging so the following script doesn't trample it.
    # NOTE: This uses some non-standard calls.
    default_logger = logging.getLogger('')
    while default_logger.handlers:
        default_logger.removeHandler(default_logger.handlers[0])

    # Finally, jump to the main routine.
    PlatformBuildWorker.main(WORKSPACE_PATH, PROJECT_SCOPE)
