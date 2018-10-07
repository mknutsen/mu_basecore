import logging
from PluginManager import IMuBuildPlugin
import copy
import os
import time

from Uefi.EdkII.Parsers.DecParser import *
from Uefi.EdkII.Parsers.InfParser import *

class DependencyCheck(IMuBuildPlugin):

      #
    # Returns the active platform if the envdict is inherited
    #
    def GetActivePlatform(self):
        if self._env is not None:
            return self._env.GetValue("ACTIVE_PLATFORM") 
        else:
            return ""

    #
    # Returns the active platform if the envdict is inherited
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

        #DEC Parser
        self.decp = DecParser()
        self.decp.SetBaseAbsPath(Edk2pathObj.WorkspacePath)
        self.decp.SetPackagePaths(Edk2pathObj.PackagePathList)

        overall_status = 0
        starttime = time.time()
        logging.critical("RUNNING DEPENDENCY CHECK")

        #Get current platform
        abs_pkg_path = Edk2pathObj.GetAbsolutePathOnThisSytemFromEdk2RelativePath(packagename)

        DEC_Dict = dict()
        DEC_Used = list()

        #Get INF Files
        INFFiles = self.WalkDirectoryForExtension([".inf"], abs_pkg_path)
        INFFiles = [x.lower() for x in INFFiles]
        INFFiles = [Edk2pathObj.GetEdk2RelativePathFromAbsolutePath(x) for x in INFFiles]  #make edk2relative path so can compare with Ignore List

        #remote ignores
        if( "DependencyConfig" in pkgconfig):
            if "IgnoreInf" in pkgconfig["DependencyConfig"]:
                for a in pkgconfig["DependencyConfig"]["IgnoreInf"]:
                    a = a.lower().replace(os.sep, "/")
                    try:
                        INFFiles.remove(a)
                    except:
                        logging.info("DscCheckConfig.IgnoreInf -> {0} not found in filesystem.  Invalid ignore file".format(a))

        INFFiles = [Edk2pathObj.GetAbsolutePathOnThisSytemFromEdk2RelativePath(x) for x in INFFiles]  #make abs path so can process

        #For each INF file
        for file in INFFiles:
            ip = InfParser()
            ip.SetBaseAbsPath(Edk2pathObj.WorkspacePath).SetPackagePaths(Edk2pathObj.PackagePathList).ParseFile(file)

            Protocols = copy.copy(ip.ProtocolsUsed)
            Packages = copy.copy(ip.PackagesUsed)
            Libraries = copy.copy(ip.LibrariesUsed)
            Guids = copy.copy(ip.GuidsUsed)
            PCDs = copy.copy(ip.PcdsUsed)
            Ppis = copy.copy(ip.PpisUsed)


            #Get text of DECs used and add to dictionary for later use
            for DEC in Packages:
                if DEC not in DEC_Dict:
                    if not DEC.lower().strip() in self.ignorelist:
                        self.decp.__init__()                            
                        try:
                            self.decp.ParseFile(self.FindFile(DEC))
                        except Exception as e:
                            if self.summary is not None:
                                self.summary.AddError("DEPENDENCY: Failed to parse DEC %s. Exception: %s" % (DEC,str(e)),  2)
                            logging.error("DEPENDENCY: Failed to parse DEC %s. Exception: %s" % (DEC,str(e)))
                            continue

                        DEC_Dict[DEC] = (copy.copy(self.decp.ProtocolsUsed), 
                                        copy.copy(self.decp.LibrariesUsed),
                                        copy.copy(self.decp.GuidsUsed),
                                        copy.copy(self.decp.PcdsUsed), 
                                        copy.copy(self.decp.PPIsUsed))

            #Make sure libraries exist within DEC
            for Library in Libraries:
                if not Library.lower().strip() in self.ignorelist:
                    found = False
                    for Package in DEC_Dict:
                        if any(s.startswith(Library.strip()) for s in DEC_Dict[Package][1]):
                            found = True
                            if Package not in DEC_Used:
                                DEC_Used.append(Package)
                    if not found:
                        logging.critical(Library + " defined in " + file + " but not found in packages")
                        if self.summary is not None:
                            self.summary.AddError("DEPENDENCY: " + Library + " defined in " + file + " but not found in packages", 2)
                        overall_status = overall_status + 1

            #Make sure protocol exists within DEC
            for Protocol in Protocols:
                if not Protocol.lower().strip() in self.ignorelist:
                    found = False
                    for Package in DEC_Dict:
                        if any(s.startswith(Protocol.strip()) for s in DEC_Dict[Package][0]):
                            found = True
                            if Package not in DEC_Used:
                                DEC_Used.append(Package)
                    if not found:
                        logging.critical(Protocol + " defined in " + file + " but not found in packages")
                        if self.summary is not None:
                            self.summary.AddError("DEPENDENCY: " + Protocol + " defined in " + file + " but not found in packages", 2)
                        overall_status = overall_status + 1

            #Make sure GUID exist within DEC
            for GUID in Guids:
                if not GUID.lower().strip() in self.ignorelist:
                    found = False
                    for Package in DEC_Dict:
                        if any(s.startswith(GUID.strip()) for s in DEC_Dict[Package][2]):
                            found = True
                            if Package not in DEC_Used:
                                DEC_Used.append(Package)
                    if not found:
                        logging.critical(GUID + " defined in " + file + " but not found in packages")
                        if self.summary is not None:
                            self.summary.AddError("DEPENDENCY: " + GUID + " defined in " + file + " but not found in packages", 2)
                        overall_status = overall_status + 1

            #Make sure PCD exist within DEC
            for PCD in PCDs:
                if not PCD.lower().strip() in self.ignorelist:
                    if('|' in PCD.lower().strip()):
                        continue #This is a PCD line that is setting the value. No dependency to check
                    found = False
                    for Package in DEC_Dict:
                        if any(s.startswith(PCD.strip()) for s in DEC_Dict[Package][3]):
                            found = True
                            if Package not in DEC_Used:
                                DEC_Used.append(Package)
                    if not found:
                        logging.critical(PCD + " defined in " + file + " but not found in packages")
                        if self.summary is not None:
                            self.summary.AddError("DEPENDENCY: " + PCD + " defined in " + file + " but not found in packages", 2)
                        overall_status = overall_status + 1

            #Make sure Ppi exist within DEC
            for PPI in Ppis:
                if not PPI.lower().strip() in self.ignorelist:
                    found = False
                    for Package in DEC_Dict:
                        if any(s.startswith(PPI.strip()) for s in DEC_Dict[Package][4]):
                            found = True
                            if Package not in DEC_Used:
                                DEC_Used.append(Package)
                    if not found:
                        logging.critical(PPI + " defined in " + file + " but not found in packages")
                        if self.summary is not None:
                            self.summary.AddError("DEPENDENCY: " + PPI + " defined in " + file + " but not found in packages", 2)
                        overall_status = overall_status + 1

        #List all packages used in Pkg
        logging.critical("Packages declared in " + AP)
        for item in DEC_Dict:
            logging.critical(item)

        #Check that every package declared is actually used
        for Package in DEC_Dict:
            if Package not in DEC_Used:
                logging.critical(Package + " declared but never used in " + AP)
                if self.summary is not None:
                    self.summary.AddWarning("DEPENDENCY: " + Package + " declared but never used in " + AP, 3)

        # If summary object exists, add results
        if self.summary is not None:
            temp = str()
            for index,item in enumerate(DEC_Dict):
                if index == 0:
                    temp = item
                else:
                    temp = temp + ", " + item + " "
            self.summary.AddResult("Packages declared in " + str(AP) + ": " + temp, 3)
            self.summary.AddResult(str(overall_status) + " error(s) in " + AP + " Dependency Check", 2)

        # If XML object exists, add results
        if overall_status is not 0 and self.xmlartifact is not None:
            self.xmlartifact.add_failure("DependencyCheck", "DependencyCheck " + os.path.basename(AP) + " " + str(self.GetTarget()),"DependencyCheck." + os.path.basename(AP), (AP + " DependencyCheck failed with " + str(overall_status) + " errors", "DEPENDENCYCHECK_FAILED"), time.time()-starttime)
        elif self.xmlartifact is not None:
            self.xmlartifact.add_success("DependencyCheck", "DependencyCheck " + os.path.basename(AP) + " " + str(self.GetTarget()),"DependencyCheck." + os.path.basename(AP), time.time()-starttime, "DependencyCheck Success")

        return overall_status

