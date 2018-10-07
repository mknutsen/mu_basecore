import logging
from PluginManager import IMuBuildPlugin
import os 
import time

from Uefi.EdkII.Parsers.DscParser import *
from Uefi.EdkII.Parsers.DecParser import *
from Uefi.EdkII.Parsers.InfParser import *

class DSCCheck(IMuBuildPlugin):

    #
    # Returns the target
    #
    def GetTarget(self):
        if self._env is not None:
            return self._env.GetValue("TARGET")
        else:
            return ""

    #   - package is the edk2 path to package.  This means workspace/packagepath relative.  
    #   - edk2path object configured with workspace and packages path
    #   - any additional command line args
    #   - RepoConfig Object (dict) for the build
    #   - PkgConfig Object (dict) for the pkg
    #   - EnvConfig Object 
    #   - Plugin Manager Instance
    #   - Plugin Helper Obj Instance
    #   - Summary Object used for printing results
    #   - xmlunittestlogger Object used for outputing junit results
    # RunBuildPlugin(self, packagename, Edk2pathObj, args, repoconfig, pkgconfig, environment, PLM, PLMHelper, summary, xmlunittestlogger):
    def RunBuildPlugin(self, packagename, Edk2pathObj, args, repoconfig, pkgconfig, environment, PLM, PLMHelper, summary, xmlartifact):
        self._env = environment
        self.summary = summary
        self.xmlartifact = xmlartifact
       
        overall_status = 0
        starttime = time.time()

        abs_pkg_path = Edk2pathObj.GetAbsolutePathOnThisSytemFromEdk2RelativePath(packagename)
        abs_dsc_path = self.get_dsc_name_in_dir(abs_pkg_path)
        wsr_dsc_path = Edk2pathObj.GetEdk2RelativePathFromAbsolutePath(abs_dsc_path)

        if abs_dsc_path is None or wsr_dsc_path is "" or not os.path.isfile(abs_dsc_path):
            xmlartifact.add_skipped("DSCCheck", "DSCCheck " + packagename + " " + str(self.GetTarget()),"DSCCheck." + packagename, time.time()-starttime, "DSCCheck Skipped")
            summary.AddResult("1 warning(s) in " + packagename + " Compile. DSC not found.", 2)
            return 0

        if self.GetTarget() is None:
            logging.error("DSCCHECK: Unknown target")

        #Get INF Files
        INFFiles = self.WalkDirectoryForExtension([".inf"], abs_pkg_path)
        INFFiles = [x.lower() for x in INFFiles]
        INFFiles = [Edk2pathObj.GetEdk2RelativePathFromAbsolutePath(x) for x in INFFiles]  #make edk2relative path so can compare with DSC

        #remote ignores
        if( "DscCheckConfig" in pkgconfig):
            if "IgnoreInf" in pkgconfig["DscCheckConfig"]:
                for a in pkgconfig["DscCheckConfig"]["IgnoreInf"]:
                    a = a.lower().replace(os.sep, "/")
                    try:
                        INFFiles.remove(a)
                    except:
                        logging.info("DscCheckConfig.IgnoreInf -> {0} not found in filesystem.  Invalid ignore file".format(a))

        #DSC Parser
        #self.dp = Dsc()
        #TODO: modify the DSCObject to be a replacement for the EDK version?
        # Eventually this will just be a part of the environment we bring up?
        self.dp = DscParser()
        self.dp.SetBaseAbsPath(Edk2pathObj.WorkspacePath)
        self.dp.SetPackagePaths(Edk2pathObj.PackagePathList)
        self.dp.ParseFile(wsr_dsc_path)

        #lowercase for matching
        self.dp.Libs = [x.lower() for x in self.dp.Libs]
        self.dp.ThreeMods = [x.lower() for x in self.dp.ThreeMods]
        self.dp.SixMods = [x.lower() for x in self.dp.SixMods]
        self.dp.OtherMods = [x.lower() for x in self.dp.OtherMods]

        #Check if INF in component section
        for INF in INFFiles:
            if not any(INF.lower().strip() in x for x in self.dp.ThreeMods) \
            and not any(INF.lower().strip() in x for x in self.dp.SixMods) and not any(INF.lower().strip() in x for x in self.dp.OtherMods):
                if self.summary is not None:
                    self.summary.AddError("DSC: " + INF + " not in " + wsr_dsc_path, 2)
                logging.critical(INF + " not in " + wsr_dsc_path)
                overall_status = overall_status + 1

        # If summary object exists, add result
        if self.summary is not None:
            self.summary.AddResult(str(overall_status) + " error(s) in " + wsr_dsc_path + " DSC Check", 2)

        # If XML object esists, add result
        if overall_status is not 0 and self.xmlartifact is not None:
            self.xmlartifact.add_failure("DSCCheck", "DSCCheck " + wsr_dsc_path + " " + str(self.GetTarget()),"DSCCheck." + wsr_dsc_path, (wsr_dsc_path + " DSCCheck failed with " + str(overall_status) + " errors", "DSCCHECK_FAILED"), time.time()-starttime)
        elif self.xmlartifact is not None:
            self.xmlartifact.add_success("DSCCheck", "DSCCheck " + wsr_dsc_path + " " + str(self.GetTarget()),"DSCCheck." + wsr_dsc_path, time.time()-starttime, "DSCCheck Success")

        return overall_status
