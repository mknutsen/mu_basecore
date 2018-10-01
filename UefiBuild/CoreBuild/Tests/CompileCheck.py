'''
    This test attempts to compile the enviroment that we are asked to
'''
from Tests.BaseTestLib import *

class CompileCheckClass(BaseTestLibClass):

    def __init__(self, workspace, packagespath, args, ignorelist = None, environment = None, summary = None, xmlartifact = None):
        BaseTestLibClass.__init__(self, workspace, packagespath, args, ignorelist, environment, summary, xmlartifact)
        logging.critical("Compile Check Test Loaded")

    def RunTest(self):
        logging.info("Compile check test running")