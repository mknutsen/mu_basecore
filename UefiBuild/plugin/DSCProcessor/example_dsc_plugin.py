
import logging
from PluginManager import IDscProcessorPlugin
#This is an example DSC PLUGIN

class example_dsc_plugin(IDscProcessorPlugin):
    
    def do_transform(self, dsc, thebuilder):
        logging.critical("WE RAN THE TRANSFORM")
        SettingsManagerDxe = dsc.components.KeyFilter(lambda x : "SettingsManagerDxe" in str(x))
        # make sure we are only affecting one components
        SettingsManagerDxe.MapKeys(lambda x: "DfciPkg/SettingsManager_PATCH3123123/SettingsManagerDxe.inf" )

        return 0


    def get_level(self, thebuilder):

        return 1