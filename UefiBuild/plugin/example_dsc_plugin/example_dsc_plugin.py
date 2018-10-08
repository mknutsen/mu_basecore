
import logging
from PluginManager import IDscProcessorPlugin
#This is an example DSC PLUGIN

class example_dsc_plugin(IDscProcessorPlugin):
    
    def do_transform(self, dsc, thebuilder):
        #logging.critical("WE RAN THE TRANSFORM")
        dsc.components.ModuleFilter(lambda x : "SettingsManagerDxe" in str(x)).MapModules(lambda x: "DfciPkg/SettingsManager_PATCH3123123/SettingsManagerDxe.inf","APPLYING SECURITY FIX 3123123").Reset()
        #dsc.components.SubsectionFilter("PcdsFeatureFlag").MapKeys(lambda x: "TESTING"+x,"MAPPING KEYS").MapValues(lambda x: "TESTING"+str(x),"MAPPING VALUES")

        return 0


    def get_level(self, thebuilder):
        return 1
    
    