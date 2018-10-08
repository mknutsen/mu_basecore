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
    #   - edk2path object configured with workspace and packages path
    #   - any additional command line args
    #   - RepoConfig Object (dict) for the build
    #   - PkgConfig Object (dict)
    #   - EnvConfig Object 
    #   - Plugin Manager Instance
    #   - Plugin Helper Obj Instance
    #   - testsuite Object used for outputing junit results
    def RunBuildPlugin(self, packagename, Edk2pathObj, args, repoconfig, pkgconfig, environment, PLM, PLMHelper, testsuite):
        logging.critical("COMPILECHECK: Compile check test running")
        self._env = environment
        AP = Edk2pathObj.GetAbsolutePathOnThisSytemFromEdk2RelativePath(packagename)
        APDSC = self.get_dsc_name_in_dir(AP)
        AP= Edk2pathObj.GetEdk2RelativePathFromAbsolutePath(APDSC)

        testcasename = "MuBuild Compile " + packagename
        testclassname = "MuBuild.CompileCheck." + packagename
        tc = testsuite.create_new_testcase(testcasename, testclassname)

        if AP is None or not os.path.isfile(APDSC):
            tc.SetSkipped()
            tc.LogStdError("1 warning(s) in {0} Compile. DSC not found.".format(packagename))
            return 0

        self._env.SetValue("ACTIVE_PLATFORM", AP, "Set in Compiler Plugin") 
        #WorkSpace, PackagesPath, PInManager, PInHelper, args, BuildConfigFile=None):
        uefiBuilder = UefiBuilder(Edk2pathObj.WorkspacePath, ", ".join(Edk2pathObj.PackagePathList), PLM, PLMHelper, args)
        #do all the steps
        ret = uefiBuilder.Go()
        if ret != 0: #failure:     
            tc.SetFailed("Compile failed for {0}".format(packagename), "Compile_FAILED")
            tc.LogStdError("{0} Compile failed with error code {1}".format(AP, ret))
            return 1

        else:
            tc.SetSuccess()
            return 0

    #
    # Returns the active platform if the envdict is inherited
    #
    def GetTarget(self):
        if self._env is not None:
            return self._env.GetValue("TARGET")
        else:
            return ""