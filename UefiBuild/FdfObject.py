import logging
import io
import re
import os
import collections
from operator import itemgetter, attrgetter

from DscObject import DscValue,DscScopeLevel,DscSection

class FdfSection(DscSection):
    subsection = False
    def __init__(self):
        super().__init__()

    def GetKeyValues(self):
        #Gets the key value pairs-> section, key, value
        keyValues = list()
        for key in self:
            value = self.GetValue(key)
            keyValues.append((self._name,key,value))
        return keyValues


class FdfDefines(FdfSection):
    def __init__(self):
        super().__init__()
        self._name = "Defines"

class FdfFD(FdfSection):
    def __init__(self, subsection = ""):
        super().__init__()
        self._name = "FD"
        if self.subsection != "":
             self._name = self._name+"."+self.subsection

class FdfDV(FdfSection):
    subsection = True
    def __init__(self, subsection = ""):
        super().__init__()
        self._name = "DV"
        if self.subsection != "":
             self._name = self._name+"."+self.subsection

class FdfFV(FdfSection):
    def __init__(self):
        super().__init__()
    
class FdfCapsule(FdfSection):
    def __init__(self):
        super().__init__()

class FdfVF(FdfSection):
    def __init__(self):
        super().__init__()

class FdfRule(FdfSection):
    def __init__(self):
        super().__init__()

class FdfOptionRom(FdfSection):
    def __init__(self):
        super().__init__()

class Fdf(object):
    SectionTypes = {
        "Defines"    : FdfDefines, 
        "FD"          : FdfFD,
        "DV"          : FdfDV,
        "FV"          : FdfFV,
        "Capsule"     : FdfCapsule,
        "VF"          : FdfVF,
        "Rule"        : FdfRule,
        "OptionRom"   : FdfOptionRom
        }

    def __init__(self):
        self.__sections = {}

    def __contains__(self, key):        
        return key in self.__sections

    def __iter__(self):
        return iter(self.__sections)

    def GetListOfSections(self):
        return list(self.__sections.keys())
    
    """Adds a section to the DSC"""
    def AddSection(self, section):
        if (section not in self.__sections):
            elements = section.split(".", 1)
            if (elements[0] in Dsc.SectionTypes):
                #Recognizable section - create an entry in self.Sections for it.
                if (len(elements) > 1):
                    #has subsections
                    self.__sections[section] = Dsc.SectionTypes[elements[0]](elements[1])
                else:
                    self.__sections[section] = Dsc.SectionTypes[elements[0]]()
            else:
                #unrecognized section or line
                raise Exception("Unrecognized section trying to be added: %s" % section)
        
    # changes a variable in a specific section with the history reasoning
    def UpdateOrCreateValue(self, section, key, value, history, level=DscScopeLevel.default):
        self.AddSection(section)
        self.__sections[section].Update(key,value,history)
        return self

    # Get the selected value from a specific section with the key
    # returns None if not found
    def GetValue(self, section, key): 
        #TODO return a value
        self.AddSection(section)
        return self.__sections[section].GetRaw(key)

    def _GetSectionTypeKeyValues(self,sectionType):
        keyValues = []
        for section in self.__sections:
            if section.startswith(sectionType):
                newKeys = self.__sections[section].GetKeyValues()
                keyValues.extend(newKeys)
        return keyValues
        
            
    def _GetSection(self,section):
        if (section not in self.__sections):
            return None
        else:            
            return self.__sections[section]

    def sectionOrder(self,section):
        sectionOrder = { 
            "Defines"    : 0, 
            "FD"          : 1,
            "DV"          : 2,
            "FV"          : 3,
            "Capsule"     : 4,
            "VF"          : 5,
            "Rule"        : 6,
            "OptionRom"   : 7
        }

        for key in sectionOrder:
            if (key in section):
                return sectionOrder[key]

        return len(sectionOrder)

    def sortSectionKeys(self):
        sectionList = sorted(self.__sections) #sort alphabetically first
        #sectionList = sorted(sectionList, key=self.subsectionOrder) #sort subsections
        sectionList = sorted(sectionList, key=self.sectionOrder) #sort sections
        return sectionList

    def Write(self, stream):
        for section in self.sortSectionKeys():
            self.__sections[section].Write(stream)

    def Parse(self, dscfilename, thebuilder):
        parser = FdfParser(dscfilename, thebuilder, self)
        return parser.Parse()

    def ParseSection(self, section, parser):
        self.__sections[section].Parse(parser)

#
# Main driver of Project Mu Builds
#
if __name__ == '__main__':
    import sys,os    
    if len(sys.argv) != 2:
        raise Exception("You need at least two arguments")
    fdf_filename = os.path.abspath(sys.argv[1])
    if not os.path.isfile(fdf_filename):
        print(fdf_filename)
        raise Exception("This is not a real file")
    
    fdf = Fdf()

    fdf.Parse(fdf_filename,None)
    