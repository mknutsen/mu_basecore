import logging
import os
import sys
from datetime import datetime
import subprocess
import argparse
import hashlib
from DscObject import Dsc, DscManipulator
import PluginManager


class DscProcessor():

    @staticmethod
    def do_processing(thebuilder):
        
        logging.info("-------------------------------------------------")
        logging.info("Pre-Parsing DSC")
        BaseDsc = Dsc()
        filename = thebuilder.mws.join(thebuilder.ws, thebuilder.env.GetValue("ACTIVE_PLATFORM"))
        if filename.endswith(".temp.dsc"):
            logging.critical("We cannot reprocess a dsc that has already been outputted")
            return 0
        status = BaseDsc.Parse(filename, thebuilder)
        #get the BaseDSC and then translate it to the modification proxy.
        #check to see if there are any python plugins in this folder
        if (status != 0):
            logging.critical("Pre-Parsing failed!! {0}".format(status))
            return status
            
        
        #request the plugins of our type from plugin manager
        for Descriptor in thebuilder.PluginManager.GetPluginsOfClass(PluginManager.IDscProcessorPlugin):
            manipulator = DscManipulator(BaseDsc,Descriptor.Name)
            try:
                rc = Descriptor.Obj.do_transform(manipulator,thebuilder)
            except Exception:
                logging.error("DSC Plugin: {0} failed".format(str(Descriptor.Name)))
                raise

        
        filename = ".temp.".join(filename.split("."))
        with open (filename, "w") as finaldsc:
            BaseDsc.Write(finaldsc)

        if (status == 0):
            thebuilder.env.GetEntry("ACTIVE_PLATFORM").Overrideable = True
            thebuilder.env.SetValue("ACTIVE_PLATFORM", ".temp.".join(thebuilder.env.GetValue("ACTIVE_PLATFORM").split(".")), "Magic")
            thebuilder.env.GetEntry("ACTIVE_PLATFORM").Overrideable = False
        else:
            logging.critical("Failed to override ACTIVE_PLATFORM")

        return 0

    
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


