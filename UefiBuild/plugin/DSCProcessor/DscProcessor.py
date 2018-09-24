import logging
import os
import sys
from datetime import datetime
import subprocess
import argparse
import hashlib

try: 

  
    
    import PluginManager
    SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(SCRIPT_PATH)
            


    class DscProcessor(PluginManager.IUefiBuildPlugin):

        def do_pre_build(self, thebuilder):
            
            from DscObject import Dsc
            from DscManipulator import DscManipulator
            from pathlib import Path

            #get the list of DSC plugins
            self._plugins = list(Path(thebuilder.ws).glob('**/*_dsc_plugin.py'))
        
            logging.info("-------------------------------------------------")
            logging.info("Pre-Parsing DSC")
            BaseDsc = Dsc()
            status = BaseDsc.Parse(thebuilder.mws.join(thebuilder.ws, thebuilder.env.GetValue("ACTIVE_PLATFORM")), thebuilder)
            #get the BaseDSC and then translate it to the modification proxy.
            #check to see if there are any python plugins in this folder
            if (status != 0):
                logging.critical("Pre-Parsing failed!!")
                #return 0

            #foreach plugin, run the plugins
            #TODO deterministiclly determine the order that plugins get run 
            #TODO also only run the plugins that match the scope that this works on
            import importlib.util
            import inspect
            for pluginPath in self._plugins:
                module_name = os.path.splitext(os.path.basename(pluginPath))[0]
                logging.info("Loading %s from %s" % (module_name,str(pluginPath)))
                spec = importlib.util.spec_from_file_location(module_name, pluginPath)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                for _, obj in inspect.getmembers(module):                    
                    if inspect.isclass(obj) and issubclass(type(obj),type(IDscBuildPlugin)):
                            #logging.critical("Creating a plugin %s which is %s" % (name,obj))                            
                            pluginObj = obj()
                            level = pluginObj.getLevel()
                            manipulator = DscManipulator(BaseDsc,str(pluginPath),level)
                            pluginObj.process(manipulator)
            #END of plugin processing
            
            filename = thebuilder.mws.join(thebuilder.ws, thebuilder.env.GetValue("ACTIVE_PLATFORM"))
            filename = ".temp.".join(filename.split("."))
            with open (filename, "w") as finaldsc:
                BaseDsc.Write(finaldsc)
            if (status != 0):
                thebuilder.env.GetEntry("ACTIVE_PLATFORM").Overrideable = True
                thebuilder.env.SetValue("ACTIVE_PLATFORM", ".temp.".join(thebuilder.env.GetValue("ACTIVE_PLATFORM").split(".")), "Magic")
            

            return 0
except ImportError:
    pass
################################################
# This plugin python file is also
# a command line tool
#
################################################
# Setup import and argument parser
def path_parse():

    parser = argparse.ArgumentParser()

    parser.add_argument (
        '-w', '--workspace', dest = 'WorkSpace', required = True, type=str,
        help = '''Specify the absolute path to your workspace by passing -w WORKSPACE or --workspace WORKSPACE.'''
        )

    Paths = parser.parse_args()
    # pre-process the parsed paths to abspath
    Paths.WorkSpace = os.path.abspath(Paths.WorkSpace)    

    if not os.path.isdir(Paths.WorkSpace):
        raise RuntimeError("Workspace path is invalid.")
    
    return Paths

#Support running this module standalone
if __name__ == '__main__':

    SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
    
    UDK_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_PATH)))),"SM_BASECORE")
    WORKSPACE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_PATH))))
    UEFIBUILD_PATH = os.path.join(UDK_PATH,"UefiBuild")
    sys.path.append(UDK_PATH)
    sys.path.append(UEFIBUILD_PATH)

    PY_LIB_PATH = os.path.join(UDK_PATH, "BaseTools", "PythonLibrary")
    sys.path.append(PY_LIB_PATH)    

    from UefiBuild import UefiBuilder
    from ParseDsc import Dsc
    from DscManipulator import DscManipulator 
    # Parse required paths passed from cmd line arguments
    Paths = path_parse()
    
    modulePath = os.path.join(Paths.WorkSpace,"SurfaceSelfhostPkg/KayakPkg/PlatformPkg.dsc")


    REQUIRED_REPOS = ('SM_BASECORE', 'Common/SM_MS_OPEN', 'Common/SM_MS_CLOSED',
                  'Common/SM_INTEL', 'Common/SM_TIANO', 'Silicon/Intel/SM_KBL')
    PROJECT_SCOPE = ('kayak', 'palindrome', 'ivanhoe', "kblfamily")

    MODULE_PKGS = ('SM_BASECORE', 'Common/SM_TIANO', 'Common/SM_MS_OPEN', 'Common/SM_MS_CLOSED', 'SurfaceSelfhostPkg', 'SURF_KBL', 'Silicon/Intel/SM_KBL')
    MODULE_PKG_PATHS = ";".join(os.path.join(WORKSPACE, pkg_name) for pkg_name in MODULE_PKGS)

    #self, WorkSpace, PackagesPath, pluginlist, args, BuildConfigFile=None
    builder = UefiBuilder(WORKSPACE, MODULE_PKG_PATHS, [], None )
    
    builder.SetPlatformEnv()
    builder.SetPlatformEnvAfterTarget()
    builder.PlatformPreBuild()
    
    builder.env.SetValue("ACTIVE_PLATFORM", "KayakPkg/PlatformPkg.dsc", "Platform Hardcoded")
    builder.env.SetValue("PRODUCT_NAME", "Kayak", "Platform Hardcoded")
    #builder.env.SetValue("MSFT_FAMILY_PACKAGE", "SurfPlatKblPkg", "Platform Hardcoded")
    #builder.env.SetValue("SH_MSFT_FAMILY_PACKAGE", "PalindromeFamilyPkg", "Platform Hardcoded")
        
    BaseDsc = Dsc(modulePath, builder)
    status = BaseDsc.Parse()
    if (status != 0):
        logging.critical("Pre-Parsing failed!!")
    else:
        manipulator = DscManipulator(BaseDsc,"testing")
    
###############################################################################
##                           PLUGIN Base Classes                             ##
###############################################################################
from enum import Enum
#Maybe like default -> silicon provider -> silicon family -> OEM -> device
class EnumDscPluginScopeLevel(Enum):
    default = 1
    silicon = 2
    silicon_family = 3
    oem = 4
    device = 5

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented
    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented
    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

###
# Plugin that supports Pre and Post Build steps
###
class IDscBuildPlugin(object):
    ##
	# Run Post Build Operations
	#
	# @param dsc - The DSC manipulator
	#
	# @return 0 for success NonZero for error. 
	##
    def process(self,dsc):

        return 0

    ##
    # returns the scope that this module operates at
    ##
    def getLevel(self) -> EnumDscPluginScopeLevel:

        return EnumDscPluginScopeLevel.default

    def getScope(self):
        return []


