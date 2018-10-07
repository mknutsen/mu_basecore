import logging
from PluginManager import IMuBuildPlugin
import time
from UefiBuild import UefiBuilder
import os
import sys

class Compiler_plugin(IMuBuildPlugin):

    ##
    # External function of plugin.  This function is used to perform the task of the MuBuild Plugin
    # 
    #   - package is the edk2 path to package.  This means workspace/packagepath relative.  
    #   - absolute path to workspace 
    #   - packagespath csv
    #   - any additional command line args
    #   - RepoConfig Object (dict) for the build
    #   - PkgConfig Object (dict)
    #   - EnvConfig Object 
    #   - Plugin Manager Instance
    #   - Plugin Helper Obj Instance
    #   - Summary Object used for printing results
    #   - xmlunittestlogger Object used for outputing junit results
    def RunBuildPlugin(self, packagename, Edk2pathObj, args, repoconfig, pkgconfig, environment, PLM, PLMHelper, summary, xmlunittestlogger):
        logging.critical("COMPILECHECK: Compile check test running")
        self._env = environment
        AP = Edk2pathObj.GetAbsolutePathOnThisSytemFromEdk2RelativePath(packagename)
        APDSC = self.get_dsc_name_in_dir(AP)
        AP= Edk2pathObj.GetEdk2RelativePathFromAbsolutePath(APDSC)
        starttime = time.time()

        if AP is None or not os.path.isfile(APDSC):
            xmlartifact.add_skipped("Compile", "Compile " + packagename + " " + str(self.GetTarget()),"Compile." + packagename, time.time()-starttime, "Compile Skipped")
            summary.AddResult("1 warning(s) in " + packagename + " Compile. DSC not found.", 2)
            return 0

        self._env.SetValue("ACTIVE_PLATFORM", AP, "Set in Compiler Plugin") 
        #WorkSpace, PackagesPath, PInManager, PInHelper, args, BuildConfigFile=None):
        uefiBuilder = UefiBuilder(Edk2pathObj.WorkspacePath, ", ".join(Edk2pathObj.PackagePathList), PLM, PLMHelper, args)
        #do all the steps
        ret = uefiBuilder.Go()
        if ret != 0: #failure:
            if summary is not None:
                summary.AddResult("1 error(s) in " + AP + " Compile. Error Code:"+str(ret), 2)
                # If XML object exists, add result
            if xmlunittestlogger is not None:
                xmlunittestlogger.add_failure("Compile", "Compile " + packagename + " " + str(self.GetTarget()),"Compile." + packagename, (AP + " Compile failed with error code " + str(ret), "Compile_FAILED_"+str(ret)), time.time()-starttime)
            return 1
        else:
            if summary is not None:
                summary.AddResult("0 error(s) in " + AP + " Compile", 2)

            if xmlunittestlogger is not None:
                xmlunittestlogger.add_success("Compile", "Compile " + packagename + " " + str(self.GetTarget()),"Compile." + packagename, time.time()-starttime, "Compile Success")
            return 0


    #
    # Returns the active platform if the envdict is inherited
    #
    def GetTarget(self):
        if self._env is not None:
            return self._env.GetValue("TARGET")
        else:
            return ""