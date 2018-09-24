
import logging
from PluginManager import IDscProcessorPlugin
#This is an example DSC PLUGIN

class example_dsc_plugin(IDscProcessorPlugin):
    
    def do_transform(self, dsc, thebuilder):
        logging.critical("WE RAN THE TRANSFORM")
        return 0


    def get_level(self, thebuilder):

        return 1