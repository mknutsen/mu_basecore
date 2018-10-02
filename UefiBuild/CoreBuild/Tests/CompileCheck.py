'''
    This test attempts to compile the enviroment that we are asked to
'''
from Tests.BaseTestLib import *

from UefiBuild import UefiBuilder
class CompileCheckClass(BaseTestLibClass):

    def __init__(self, workspace, packagespath, args, ignorelist = None, environment = None, summary = None, xmlartifact = None):
        BaseTestLibClass.__init__(self, workspace, packagespath, args, ignorelist, environment, summary, xmlartifact)
        logging.critical("Compile Check Test Loaded")
        self._ws = workspace
        self._pp = packagespath
        self._args = args
        self._ignoreList = ignorelist
        self._env = environment
        self._summary = summary
        self._xml = xmlartifact        

    def RunTest(self):
        logging.critical("COMPILECHECK: Compile check test running")
        #WorkSpace, PackagesPath, pluginlist, args, BuildConfigFile=None
        logging.critical("The packages we are going to use {0}".format(self._pp))
        starttime = time.time()

        AP = self.GetActivePlatform()
        AP_Root = os.path.dirname(AP)

        uefiBuilder = UefiBuilder(self._ws, self._pp, [], self._args)
        #do all the steps
        ret = uefiBuilder.Go()
        if ret != 0: #failure:
            if self.summary is not None:
                self.summary.AddError("Compiler Error: "+str(ret), 2)
             # If XML object esists, add result
            if self.xmlartifact is not None:
                self.xmlartifact.add_failure("Compile Check", "Compile Check " + os.path.basename(AP) + " " + str(self.GetTarget()),"Compile Check." + os.path.basename(AP), (AP + " Compile failed with " + str(ret) + " errors", "Compile_FAILED"), time.time()-starttime)
            return ret
        else:
            if self.summary is not None:
                self.summary.AddResult("0 error(s) in " + AP + " Compile", 2)

            if self.xmlartifact is not None:
                self.xmlartifact.add_success("Compile", "Compile " + os.path.basename(AP) + " " + str(self.GetTarget()),"Compile." + os.path.basename(AP), time.time()-starttime, "Compile Success")
            return 0
