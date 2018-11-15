<<<<<<< HEAD
import PluginManager
import logging
import os
from UtilityFunctions import RunCmd
from UtilityFunctions import RunPythonScript
from UtilityFunctions import CatalogSignWithSignTool
=======
from MuEnvironment import PluginManager
import logging
import os
from MuPythonLibrary.UtilityFunctions import RunCmd
from MuPythonLibrary.UtilityFunctions import RunPythonScript
from MuPythonLibrary.UtilityFunctions import CatalogSignWithSignTool
>>>>>>> moving mu_build 1808 in HEAD=7f6adb264392130c1b9aa01b8796fa9fdf87b66f
import shutil
import datetime

class Edk2ToolHelper(PluginManager.IUefiHelperPlugin):

    def RegisterHelpers(self, obj):
        fp = os.path.abspath(__file__)
        obj.Register("PackageMsFmpHeader", Edk2ToolHelper.PackageMsFmpHeader, fp)
        obj.Register("PackageFmpImageAuth", Edk2ToolHelper.PackageFmpImageAuth, fp)
        obj.Register("PackageFmpCapsuleHeader", Edk2ToolHelper.PackageFmpCapsuleHeader, fp)
        obj.Register("PackageCapsuleHeader", Edk2ToolHelper.PackageCapsuleHeader, fp)


    ##
    # Function to Create binary with MsFmp Header prepended with data supplied
    # InputBin: Input binary to wrap with new header (file path)
    # OutputBin: file path to write Output binary to
    # VersionInt: integer parameter for the version
    # LsvInt: Integer parameter for the lowest supported version
<<<<<<< HEAD
    # DepList: (optional) list of dependences. Dep format is tuple (FmpGuidForDep, FmpIndex, IntFmpMinVersion, IntFlags ) 
    ### Dep format can change overtime.  Flags can be added for new behavior.  See the version and library implementing behavior.  
    ### V1 details.  
    ####Flag bit 0: dep MUST be in system if 1.  Otherwise dep only applied if fmp found in system.
    ####Flag bit 1: dep version MUST be exact match if 1.  Otherwise dep must be equal or greater than version.    
=======
    # DepList: (optional) list of dependences. Dep format is tuple (FmpGuidForDep, FmpIndex, IntFmpMinVersion, IntFlags )
    ### Dep format can change overtime.  Flags can be added for new behavior.  See the version and library implementing behavior.
    ### V1 details.
    ####Flag bit 0: dep MUST be in system if 1.  Otherwise dep only applied if fmp found in system.
    ####Flag bit 1: dep version MUST be exact match if 1.  Otherwise dep must be equal or greater than version.
>>>>>>> moving mu_build 1808 in HEAD=7f6adb264392130c1b9aa01b8796fa9fdf87b66f
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
<<<<<<< HEAD
    # DevPfxFilePath: (optional) file path to dev pfx file to sign with.  If not supplied production signing is assumed. 
    # 
=======
    # DevPfxFilePath: (optional) file path to dev pfx file to sign with.  If not supplied production signing is assumed.
    #
>>>>>>> moving mu_build 1808 in HEAD=7f6adb264392130c1b9aa01b8796fa9fdf87b66f
    ##
    @staticmethod
    def PackageFmpImageAuth(InputBin, OutputBin, DevPfxFilePath = None, DevPfxPassword = None, DetachedSignatureFile = None, Eku = None):
        logging.debug("CapsulePackage: Fmp Image Auth Header/Signing")
<<<<<<< HEAD
  
=======

>>>>>>> moving mu_build 1808 in HEAD=7f6adb264392130c1b9aa01b8796fa9fdf87b66f
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

<<<<<<< HEAD
             #Find Signtool 
=======
             #Find Signtool
>>>>>>> moving mu_build 1808 in HEAD=7f6adb264392130c1b9aa01b8796fa9fdf87b66f
            SignToolPath = os.path.join(os.getenv("ProgramFiles(x86)"), "Windows Kits", "8.1", "bin", "x64", "signtool.exe")
            if not os.path.exists(SignToolPath):
                SignToolPath = SignToolPath.replace('8.1', '10')
            if not os.path.exists(SignToolPath):
                raise Exception("Can't find signtool on this machine.")

            cmd = cmd + " --SignTool \"" + SignToolPath + "\""

            cmd = cmd + " --pfxfile " + DevPfxFilePath
            if( DevPfxPassword is not None):
                cmd += " --pfxpass " + DevPfxPassword
            if (Eku is not None):
                cmd += " --eku " + Eku
            ret = RunPythonScript(cmd, workingdir=TempOutDir)
            #delete the temp dir
            shutil.rmtree(TempOutDir, ignore_errors=True)
        else:
            #production
            logging.debug("FmpImageAuth is Production signed")

            if(DetachedSignatureFile is None):
<<<<<<< HEAD
                logging.debug("FmpImageAuth Step1: Make ToBeSigned file for production") 
                cmd = cmd + " --production"  
                ret = RunPythonScript(cmd, workingdir=TempOutDir)
                if(ret != 0):
                    raise Exception("GenFmpImageAuth Failed production signing: step 1.  Errorcode %d" % ret)
                #now we have a file to sign at 
=======
                logging.debug("FmpImageAuth Step1: Make ToBeSigned file for production")
                cmd = cmd + " --production"
                ret = RunPythonScript(cmd, workingdir=TempOutDir)
                if(ret != 0):
                    raise Exception("GenFmpImageAuth Failed production signing: step 1.  Errorcode %d" % ret)
                #now we have a file to sign at
>>>>>>> moving mu_build 1808 in HEAD=7f6adb264392130c1b9aa01b8796fa9fdf87b66f
                TBS = os.path.join(os.path.dirname(OutputBin), "payload.Temp.ToBeSigned")
                if(not os.path.exists(TBS)):
                    raise Exception("GenFmpImageAuth didn't create ToBeSigned file")
                os.rename(TBS, OutputBin)
<<<<<<< HEAD
            
=======

>>>>>>> moving mu_build 1808 in HEAD=7f6adb264392130c1b9aa01b8796fa9fdf87b66f
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
<<<<<<< HEAD
            
=======

>>>>>>> moving mu_build 1808 in HEAD=7f6adb264392130c1b9aa01b8796fa9fdf87b66f
        cmd = "genfv -o " + OutputBin
        cmd = cmd + " -g " + FmpDeviceGuid
        cmd = cmd + " --capsule -v -f " + InputBin
        cmd = cmd + " --capFlag PersistAcrossReset --capFlag InitiateReset"
        ret = RunCmd(cmd)
        if(ret != 0):
            raise Exception("GenFv Failed with errorcode" % ret)
<<<<<<< HEAD
        return ret 
=======
        return ret
>>>>>>> moving mu_build 1808 in HEAD=7f6adb264392130c1b9aa01b8796fa9fdf87b66f
