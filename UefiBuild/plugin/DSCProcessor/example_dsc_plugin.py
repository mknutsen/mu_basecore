
import logging
import DscProcessor

#This is an example DSC PLUGIN
#All DSC plugins must end in dsc_plugin.py

class KayakDscProcessor(DscProcessor.IDscBuildPlugin):
    def process(self, dsc):
        return 0 #So it doesn't accidentally get loaded
        #Add some elements to the defines section
        dsc.AddOrGetSection("Defines").AddOrUpdate("Testing","Test","Because I feel like it").AddOrUpdate("Testing2","Test","Because I feel like it").AddOrUpdate("Testing3","Test","Because I feel like it")
        
        #filter to just those added elements, add something to their values, then remove them from the DSC
        dsc.GetSection("Defines").Filter(lambda x : str(x).startswith("Testing")).Transform(lambda k,v: v+"_testing","Adding on more testing").Remove("Get rid of all the defines?")

        if (dsc.GetSection("Defines").HasKey("PLATFORM_VERSION")):
            dsc.GetSection("Defines").FilterToKey("SH_MSFT_FAMILY_PACKAGE").Set("PalindromeFamilyPkg","for the lols")
    def getScope(self):
        return DscProcessor.EnumDscPluginScopeLevel.device

    