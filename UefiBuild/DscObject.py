import logging
import io
import re
import os
import collections
from operator import itemgetter, attrgetter

#TODO rewrite this to be more friendly

from enum import Enum
#Maybe like default -> silicon provider -> silicon family -> OEM -> device
class DscScopeLevel(Enum):
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

class DscValue(object):
    def __init__(self, newValue, history, scope):
        self._value = [newValue] 
        self._revisions = 1
        self._history = [history]
        self._scope = [scope]
        
    def set(self, newValue, history, scope):

        if (newValue != self._value[0] and self._scope[0] == scope):
            logging.warn("Same scope level conflict of %s for value %s from %s" % (scope, newValue, history))
        
        if (newValue != self._value[0] and self._scope[0] <= scope):
            self._revisions += 1
            self._value.insert(0,newValue) # put the new value at the front of the array
            self._history.insert(0,history)
            self._scope.insert(0,scope)

        elif (newValue != self._value[0] and self._scope[0] > scope) or newValue == self._value[0]:
            self._revisions += 1
            self._value.insert(1,newValue) # put the new value at the front of the array            
            self._history.insert(1,"Ignored: %s" % (history))
            self._scope.insert(1,scope)
            logging.debug("Ignoring this input %s vs %s" % (newValue, self._value[0]))

    def __str__(self):
        return self._value[0]    

    def Get(self):
        return self._value[0]

    # get the history for this DSC value
    def History(self):
        def _ConvertHistory(index):
            return "\t# Revision:%s from %s: scope=%s" %(self._value[index],self._history[index], self._scope[index])
        historyList = list(map(_ConvertHistory, range(len(self._value))))
        return str.join("\n",historyList)

    def __lt__(self, other):
        return str(self) < str(other)
    def __gt__(self, other):
        return str(self) > str(other)

    def __eq__(self, other):
        return str(self) == str(other)

        
#
# Super-class of all DSC sections. Allows defines to be scoped to sections (if needed).
#

class DscSection(object):
    def __init__(self, dscparser):        
        self._default = "__defines"
        self.__defines = {}
        self._name = "DEFAULT_NAME"
    
   
    def Get(self, key):
        store = getattr(self,self._default)
        if (key not in store):
            return None
        elif (store[key].Get() is not None):
            return str(store[key])
        else:
            return None

    def GetRaw(self,key):
        store = getattr(self,self._default)
        if (key not in store):
            return None
        elif (store[key].Get() is not None):
            return store[key].Get()
        else:
            return None

    def __contains__(self, key):
        store = getattr(self,self._default)
        return key in store

    def GetKeys(self):
        store = getattr(self,self._default)
        return list(store.keys())

    def GetHistory(self, key):
        store = getattr(self,self._default)
        if (key not in store):
            return ""
        else:
            return str(store[key].History())

    def Update(self, key, value, history, scope=DscScopeLevel.default):
        store = getattr(self,self._default)
        if (key not in store):
            store[key] = DscValue(value,history, scope)
        else:
            store[key].set(value, history, scope)

    def Write(self, stream):
        stream.write("[%s]\n" % self._name)
        #Global defines may be used in FDF, so print them here.
        for k in sorted(self.__defines):
            stream.write("%s\n" % (self.GetHistory(k)))
            if (self.Get(k) is None):
                stream.write("#")    
            stream.write("    DEFINE %s = %s\n" % (k, self.Get(k)))

        for k in sorted(self.GetKeys()):
            stream.write("%s\n" % (self.GetHistory(k)))
            if (self.Get(k) is None):
                stream.write("#")
            stream.write("    %s = %s\n" % (k, self.Get(k)))
        stream.write("\n")

#[Defines] section parser class.
class DscDefines(DscSection):
    def __init__(self, dscparser):
        super().__init__(dscparser)
        self.parser = dscparser
        self.globals = {}
        self._default = "globals"
        self._name = "Defines"
    
#[SkuIds] section parser class
class DscSkus(DscSection):
    def __init__(self, dscparser):
        super().__init__(dscparser)
        self.skus = {}
        self.parser = dscparser
        self._default = "skus"
    
#[LibraryClasses] section parser class. Handles subsections (e.g. LibraryClasses.IA32) as well.
class DscLibraryClasses(DscSection):
    def __init__(self, dscparser, subsection):
        super().__init__(dscparser)
        self._libclasses = {}
        self.parser = dscparser
        self.subsection = subsection
        self._default = "_libclasses"
    
    def sortedLibClasses(self):
        sortedClasses = collections.OrderedDict(sorted(self._libclasses.items())) #sort alphabetically
        sortedClasses = collections.OrderedDict(sorted(sortedClasses.items(), key=itemgetter(1))) #then sort by path
        return sortedClasses
    
#[Pcds*] section parser class. Subsection is e.g. "FixedAtBuild"
class DscPcds(DscSection):
    def __init__(self, dscparser, subsection):
        super().__init__(dscparser)
        self._pcds = {}
        self.parser = dscparser
        self.subsection = subsection
        self._default = "_pcds"        
    
#<LibraryClasses> option parser for components.
class DscComponentLibraryClasses(object):
    def __init__(self, dscparser):
        self.libclasses = []
        self.parser = dscparser

    def getLibrary(self, component, library):
        libInstance = next((v[1] for i, v in enumerate(self.libclasses) if v[0] == library), None)
        if (libInstance == None):
            libInstance = self.parser.resolveLibraryInstance(component, library)
        return libInstance

    def addLibrary(self, libname, libpath, source=None):
        self.libclasses.append((libname, libpath, source))
        
    def containsLibrary(self, library):
        libInstance = next((v[1] for i, v in enumerate(self.libclasses) if v[0] == library), None)
        return (libInstance != None)

    
#<Pcds*> option parser for components.
class DscComponentPcds(DscSection):
    def __init__(self, dscparser, subsection):
        self._pcds = {}
        self.parser = dscparser
        self.subsection = subsection
        self._default = "_pcds"

#<BuildOptions> option parser for components.
class DscComponentBuildOptions(object):
    def __init__(self, dscparser):
        self.buildappend = {}
        self.buildreplace = {}
        self.parser = dscparser

#Component parser.
#Parses the inf path,and then delegates parsing of options subsections to the option parsers above.
class DscComponent(DscSection):

    OptionTypes = {"LibraryClasses" : DscComponentLibraryClasses,
                   "Pcds"           : DscComponentPcds,
                   "BuildOptions"   : DscComponentBuildOptions}

    def __init__(self, dscparser, subsection):
        self.parser = dscparser
        self.componentPath = ""
        self._options = {}
        self._default = "_options"
        self.subsection = subsection
        self.basename = ""
        self.fileguid = ""
        self.moduleType = ""
        self.isLibrary = False
    
    def resolveLib(self, libname):
        if "LibraryClasses" not in self._options:
            self.Update("LibraryClasses",DscComponent.OptionTypes["LibraryClasses"](self.parser),self.parser.GetSource())            
        return self.GetRaw("LibraryClasses").getLibrary(self, libname)  
    

#[Components] section parser. Subsection is e.g. "X64".
class DscComponents(DscSection):
    def __init__(self, dscparser, subsection):
        super().__init__(dscparser)
        self._components = {}
        self.parser = dscparser
        self._default = "_components"
        self.subsection = subsection        
    
    def __contains__(self, key):        
        return key in self._components
    
    
#[BuildOptions] section parser.
class DscBuildOptions(DscSection):
    def __init__(self, dscparser):
        super().__init__(dscparser)
        self.buildappend = {}
        self.buildreplace = {}
        self.parser = dscparser

#Main DSC Object. Deletgates
class Dsc(object):

    SectionTypes = { "Defines"         : DscDefines, 
                     "SkuIds"          : DscSkus,
                     "LibraryClasses"  : DscLibraryClasses,
                     "Pcds"            : DscPcds,
                     "Components"      : DscComponents,
                     "BuildOptions"    : DscBuildOptions}

    def __init__(self):
        self.__sections = {}

    def __contains__(self, key):        
        return key in self.__sections

    def GetListOfSections(self):
        return list(self.__sections.keys())
    
    """Adds a section to the DSC"""
    def AddSection(self, section):        
        if (section not in self.__sections):
            if (section[0:4] == "Pcds"):
                elements = (section[0:4], section[4:])
            else:
                elements = section.split(".", 1)
            if (elements[0] in Dsc.SectionTypes):
                #Recognizable section - create an entry in self.Sections for it.
                if (len(elements) > 1):
                    #has subsections
                    self.__sections[section] = Dsc.SectionTypes[elements[0]](self, elements[1])
                else:
                    self.__sections[section] = Dsc.SectionTypes[elements[0]](self)
            else:
                #unrecognized section or line
                raise Exception("Unrecognized section trying to be added: %s" % section)
            #TODO if we have a components section we need to create the section in it?
        
    # changes a variable in a specific section with the history reasoning
    def UpdateOrCreateValue(self, section, key, value, history, level=DscScopeLevel.default):
        self.AddSection(section)
        self.__sections[section].Update(key,value,history)
        return self

    # Get the selected value from a specific section with the key
    # returns None if not found
    def GetValue(self, section, key): 
        #TODO return a value
        return None

    def _GetSectionKeys(self,section):
        if (section not in self.__sections):
            return []
        else:            
            return self.__sections[section].GetKeys()
            
    def _GetSection(self,section):
        if (section not in self.__sections):
            return None
        else:            
            return self.__sections[section]

        
    #Sorting routines to order sections per EDK spec for Write
    def subsectionOrder(subsection):
        if "common" in subsection:
            return 0
        return 1

    def sectionOrder(section):
        sectionOrder = { "Defines": 0,
                         "SkuIds": 1, 
                         "LibraryClasses" : 2,
                         "Pcds" : 3,
                         "Components" :4,
                         "BuildOptions" :5 }

        for key in sectionOrder:
            if (key in section):
                return sectionOrder[key]

        return len(sectionOrder)

    def sortSectionKeys(self):
        sectionList = sorted(self.__sections) #sort alphabetically first
        sectionList = sorted(sectionList, key=Dsc.subsectionOrder) #sort subsections
        sectionList = sorted(sectionList, key=Dsc.sectionOrder) #sort sections
        return sectionList

    def Write(self, stream):
        for section in self.sortSectionKeys():
            self.__sections[section].Write(stream)

##
# HELPER FUNCTIONS
##
def resolveGuid(value):
    ''' converts a guid specificed in one format to the format wanted by TianoCore
        3378D499-69AF-4862-A001-5189F68C617E -> {0x99, 0xD4, 0x78, 0x33, 0xAF, 0x69, 0x62, 0x48, 0xA0, 0x01, 0x51, 0x89, 0xF6, 0x8C, 0x61, 0x7E}
    '''
    if value == None:
        return None
    #3378 D499-69AF-4862-A001-5189 F68C 617E
    # {0x99, 0xD4, 0x78, 0x33, 0xAF, 0x69, 0x62, 0x48, 0xA0, 0x01, 0x51, 0x89, 0xF6, 0x8C, 0x61, 0x7E}
    match = re.match('\A[A-F\d]{8}-[A-F\d]{4}-[A-F\d]{4}-[A-F\d]{4}-[A-F\d]{12}$',str(value))
    if match == None:            
        return value
    
    value = re.sub('-','',match.group())
    # 0  1  2  3  4  5  6  7  8 09 10 11 12 13 14 15
    #33 78 D4 99 69 AF-48 62-A0 01-51 89 F6 8C 61 7E
    #99 D4 78 33 AF 69 62 48 A0 01 51 89 F6 8C 61 7E
    swapList = [(0,3), (1,2), (4,5), (6,7)]

    values = []
    for i in range(0,len(value),2):
        values.append("0x"+value[i:i+2])

    guid = values.copy()
    for start,end in swapList:
        guid[start] = values[end]
        guid[end] = values[start]
        
    guidStr = ", ".join(guid)
    guidStr = "{" + guidStr + "}"
    return guidStr
