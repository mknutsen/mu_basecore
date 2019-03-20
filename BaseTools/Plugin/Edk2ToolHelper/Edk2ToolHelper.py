import yapsy.UefiBuildPluginTypes as UefiBuildPluginTypes
import logging
import os
from UtilityFunctions import RunCmd
from UtilityFunctions import RunPythonScript
from UtilityFunctions import CatalogSignWithSignTool
import shutil
import datetime

class Edk2ToolHelper(UefiBuildPluginTypes.IUefiHelperPlugin):

    def RegisterHelpers(self, obj):
        fp = os.path.abspath(__file__)
        obj.Register("PackageMsFmpHeader", Edk2ToolHelper.PackageMsFmpHeader, fp)
        obj.Register("PackageFmpImageAuth", Edk2ToolHelper.PackageFmpImageAuth, fp)
        obj.Register("PackageWindowsCapsuleFiles", Edk2ToolHelper.PackageWindowsCapsuleFiles, fp)
        obj.Register("PackageFmpCapsuleHeader", Edk2ToolHelper.PackageFmpCapsuleHeader, fp)
        obj.Register("PackageCapsuleHeader", Edk2ToolHelper.PackageCapsuleHeader, fp)


    ##
    # Function to Create binary with MsFmp Header prepended with data supplied
    # InputBin: Input binary to wrap with new header (file path)
    # OutputBin: file path to write Output binary to
    # VersionInt: integer parameter for the version
    # LsvInt: Integer parameter for the lowest supported version
    # DepList: (optional) list of dependences. Dep format is tuple (FmpGuidForDep, FmpIndex, IntFmpMinVersion, IntFlags ) 
    ### Dep format can change overtime.  Flags can be added for new behavior.  See the version and library implementing behavior.  
    ### V1 details.  
    ####Flag bit 0: dep MUST be in system if 1.  Otherwise dep only applied if fmp found in system.
    ####Flag bit 1: dep version MUST be exact match if 1.  Otherwise dep must be equal or greater than version.    
    ##
    @staticmethod
    def PackageMsFmpHeader(InputBin, OutputBin, VersionInt, LsvInt, DepList = []):
        logging.debug("CapsulePackage: Fmp Header")
        cmd = "genmspayloadheader.exe -o " + OutputBin
        cmd = cmd + " --version " + hex(VersionInt).rstrip("L")
        cmd = cmd + " --lsv " + hex(LsvInt)
        cmd = cmd + " -p " + InputBin + " -v"
        #append depedency if supplied
        for dep in DepList:
            depGuid = dep[0]
            depIndex = int(dep[1])
            depMinVer = hex(dep[2])
            depFlag = hex(dep[3])
            logging.debug("Adding a Dependency:\n\tFMP Guid: %s \nt\tFmp Descriptor Index: %d \n\tFmp DepVersion: %s \n\tFmp Flags: %s\n" % (depGuid, depIndex, depMinVer, depFlag))
            cmd += " --dep " + depGuid + " " + str(depIndex) + " " + depMinVer + " " + depFlag
        ret = RunCmd(cmd)
        if(ret != 0):
            raise Exception("GenMsPayloadHeader Failed with errorcode %d" % ret)
        return ret

    ##
    # Function to create binary wrapped with FmpImage Auth using input supplied
    # InputBin: Input binary to wrap with new fmp image auth header (file path)
    # OutputBin: file path to write final output binary to
    # DevPfxFilePath: (optional) file path to dev pfx file to sign with.  If not supplied production signing is assumed. 
    # 
    ##
    @staticmethod
    def PackageFmpImageAuth(InputBin, OutputBin, DevPfxFilePath = None, DevPfxPassword = None, DetachedSignatureFile = None):
        logging.debug("CapsulePackage: Fmp Image Auth Header/Signing")
  
        #temp output dir is in the outputbin folder
        ret = 0
        TempOutDir = os.path.join(os.path.dirname(os.path.abspath(OutputBin)), "_Temp_FmpImageAuth_" + str(datetime.datetime.now().time()).replace(":", "_"))
        logging.debug("Temp Output dir for FmpImageAuth: %s" % TempOutDir)
        os.mkdir(TempOutDir)
        cmd =  "GenFmpImageAuth.py"
        cmd = cmd + " -o " + OutputBin
        cmd = cmd + " -p " + InputBin + " -m 1"
        cmd = cmd + " --debug"
        cmd = cmd + " -l " + os.path.join(TempOutDir, "GenFmpImageAuth_Log.log")
        if(DevPfxFilePath is not None):
            logging.debug("FmpImageAuth is dev signed. Do entire process in 1 step locally.")

             #Find Signtool 
            SignToolPath = os.path.join(os.getenv("ProgramFiles(x86)"), "Windows Kits", "8.1", "bin", "x64", "signtool.exe")
            if not os.path.exists(SignToolPath):
                SignToolPath = SignToolPath.replace('8.1', '10')
            if not os.path.exists(SignToolPath):
                raise Exception("Can't find signtool on this machine.")

            cmd = cmd + " --SignTool \"" + SignToolPath + "\""

            cmd = cmd + " --pfxfile " + DevPfxFilePath
            if( DevPfxPassword is not None):
                cmd += " --pfxpass " + DevPfxPassword
            ret = RunPythonScript(cmd, workingdir=TempOutDir)
            #delete the temp dir
            shutil.rmtree(TempOutDir, ignore_errors=True)
        else:
            #production
            logging.debug("FmpImageAuth is Production signed")

            if(DetachedSignatureFile is None):
                logging.debug("FmpImageAuth Step1: Make ToBeSigned file for production") 
                cmd = cmd + " --production"  
                ret = RunPythonScript(cmd, workingdir=TempOutDir)
                if(ret != 0):
                    raise Exception("GenFmpImageAuth Failed production signing: step 1.  Errorcode %d" % ret)
                #now we have a file to sign at 
                TBS = os.path.join(os.path.dirname(OutputBin), "payload.Temp.ToBeSigned")
                if(not os.path.exists(TBS)):
                    raise Exception("GenFmpImageAuth didn't create ToBeSigned file")
                os.rename(TBS, OutputBin)
            
            else:
                logging.debug("FmpImageAuth Step3: Final Packaging of production signed")
                cmd = cmd + " --production -s " + DetachedSignatureFile
                ret = RunPythonScript(cmd, workingdir=TempOutDir)
                #delete the temp dir
                shutil.rmtree(TempOutDir, ignore_errors=True)

        if(ret != 0):
            raise Exception("GenFmpImageAuth Failed with errorcode %d" % ret)
        return ret

    @staticmethod
    def PackageFmpCapsuleHeader(InputBin, OutputBin, FmpGuid):
        logging.debug("CapsulePackage: Fmp Capsule Header")
        cmd = "genfmpcap.exe -o " + OutputBin
        cmd = cmd + " -p " + InputBin + " " + FmpGuid + " 1 0 -V"
        ret = RunCmd(cmd)
        if(ret != 0):
            raise Exception("GenFmpCap Failed with errorcode" % ret)
        return ret

    @staticmethod
    def PackageCapsuleHeader(InputBin, OutputBin, FmpDeviceGuid=None):
        logging.debug("CapsulePackage: Final Capsule Header")
        if(FmpDeviceGuid == None):
            logging.debug("CapsulePackage: Using default industry standard FMP guid")
            FmpDeviceGuid = "6dcbd5ed-e82d-4c44-bda1-7194199ad92a"
            
        cmd = "genfv -o " + OutputBin
        cmd = cmd + " -g " + FmpDeviceGuid
        cmd = cmd + " --capsule -v -f " + InputBin
        cmd = cmd + " --capFlag PersistAcrossReset --capFlag InitiateReset"
        ret = RunCmd(cmd)
        if(ret != 0):
            raise Exception("GenFv Failed with errorcode" % ret)
        return ret 

    @staticmethod
    def PackageWindowsCapsuleFiles(OutputFolder, ProductName, ProductFmpGuid, CapsuleVersion_DotString, CapsuleVersion_HexString, ProductFwProvider, ProductFwMfgName, ProductFwDesc, CapsuleFileName, PfxFile=None, PfxPass=None, Rollback=False):
        logging.debug("CapsulePackage: Create Windows Capsule Files")
        CatFileName = os.path.realpath(os.path.join(OutputFolder, ProductName + ".cat"))

        #Make INF
        cmd = "CreateWindowsInf.py"
        cmd = cmd + " " + ProductName + " " + CapsuleVersion_DotString + " " + ProductFmpGuid
        cmd = cmd + " " + CapsuleFileName + " " + CapsuleVersion_HexString + " " + ProductFwProvider + " " + ProductFwMfgName
        cmd = cmd + " " + ProductFwDesc
        if (Rollback):
          cmd = cmd + " rollback"
        ret = RunPythonScript(cmd, workingdir=OutputFolder)
        if(ret != 0):
            raise Exception("CreateWindowsInf Failed with errorcode %d" % ret)

        #Find Signtool 
        SignToolPath = os.path.join(os.getenv("ProgramFiles(x86)"), "Windows Kits", "10", "bin", "x64", "signtool.exe")
        if not os.path.exists(SignToolPath):
            SignToolPath = SignToolPath.replace('10', '8.1')
        if not os.path.exists(SignToolPath):
            raise Exception("Can't find signtool on this machine.")
        
        #Find Inf2Cat tool
        Inf2CatToolPath = os.path.join(os.getenv("ProgramFiles(x86)"), "Windows Kits", "10", "bin", "x86", "Inf2Cat.exe")
        if not os.path.exists(Inf2CatToolPath):
            raise Exception("Can't find Inf2Cat on this machine.  Please install the Windows 10 WDK - https://developer.microsoft.com/en-us/windows/hardware/windows-driver-kit")
        
        #Make Cat file
        cmd = Inf2CatToolPath + " /driver:. /os:10_X64 /verbose"
        ret = RunCmd(cmd, workingdir=OutputFolder)
        if(ret != 0):
            raise Exception("Creating Cat file Failed with errorcode %d" % ret)

        if(PfxFile is not None):
            #dev sign the cat file
            ret = CatalogSignWithSignTool(SignToolPath, CatFileName, PfxFile, PfxPass)
            if(ret != 0):
                raise Exception("Signing Cat file Failed with errorcode %d" % ret)
        
        return ret 
