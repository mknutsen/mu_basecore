import logging
from PluginManager import IMuBuildPlugin
import time
from UefiBuild import UefiBuilder
import os, sys

class Compiler_plugin(IMuBuildPlugin):

    ##
    # Function that allows plugin to register its functions with the
    # obj.  
    # @param obj[in, out]: HelperFunctions object that allows functional 
    # registration.  
    #
    def RunMu(self, workspace="", packagespath="", args=[], ignorelist = None, environment = None, summary = None, xmlartifact = None):
        self._env = environment
        logging.critical("COMPILECHECK: Compile check test running")
        #WorkSpace, PackagesPath, pluginlist, args, BuildConfigFile=None
        logging.critical("The packages we are going to use {0}".format(packagespath))
        starttime = time.time()

        AP = self.GetActivePlatform()
        AP_Root = os.path.dirname(AP)

        uefiBuilder = UefiBuilder(workspace,packagespath, [], args)
        #do all the steps
        ret = uefiBuilder.Go()
        if ret != 0: #failure:
            if summary is not None:
                summary.AddError("Compiler Error: "+str(ret), 2)
                # If XML object esists, add result
            if xmlartifact is not None:
                xmlartifact.add_failure("Compile", "Compile " + os.path.basename(AP) + " " + str(self.GetTarget()),"Compile." + os.path.basename(AP), (AP + " Compile failed with error code " + str(ret), "Compile_FAILED_"+str(ret)), time.time()-starttime)
            return 1
        else:
            if summary is not None:
                summary.AddResult("0 error(s) in " + AP + " Compile", 2)

            if xmlartifact is not None:
                xmlartifact.add_success("Compile", "Compile " + os.path.basename(AP) + " " + str(self.GetTarget()),"Compile." + os.path.basename(AP), time.time()-starttime, "Compile Success")
            return 0
        pass
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