import logging
import io
import re
import os
import collections
from operator import itemgetter, attrgetter
from ParseDsc import Dsc

from DscProcessor import EnumDscPluginScopeLevel

class DscManipulator(object):
    def __init__(self, baseDSC, source, scope=EnumDscPluginScopeLevel.default):
        self.__dsc = baseDSC
        self.__source = source
        self.__scope = scope

    def GetListOfSections(self):
        #TODO return a list of sections
        return list(self.__dsc.Sections.keys())
    
    """Adds a section to the DSC"""
    def AddOrGetSection(self, section, compSection = None):
        #TODO adds a new section
        if (section not in self.__dsc.Sections):
            if (section[0:4] == "Pcds"):
                elements = (section[0:4], section[4:])
            else:
                elements = section.split(".", 1)
            if (elements[0] in Dsc.SectionTypes):
                #Recognizable section - create an entry in self.Sections for it.
                if (len(elements) > 1):
                    #has subsections
                    self.__dsc.Sections[section] = Dsc.SectionTypes[elements[0]](self, elements[1])
                else:
                    self.__dsc.Sections[section] = Dsc.SectionTypes[elements[0]](self)
            else:
                #unrecognized section or line
                raise Exception("Unrecognized section trying to be added: %s" % section)
            #TODO if we have a components section we need to create the section in it?
        return self.GetSection(section, compSection)
    
    def GetSection(self, sectionName, compSection = None):
        #TODO check if 
        if (sectionName not in self.__dsc.Sections):
            return None
        else:
            return DscSectionManipulation(self, sectionName,self.__source, compSection)
        
    # changes a variable in a specific section with the history reasoning
    def UpdateOrCreateValue(self, section, key, value, history):
        #TODO: reason about scope
        sectionManip = self.AddOrGetSection(section)
        sectionManip.AddOrUpdate(key,value,self.__source+":"+history, self.__scope)
        return self

    # Get the selected value from a specific section with the key
    # returns None if not found
    def GetValue(self, section, key): 
        #TODO return a value
        return None

    def _GetSectionKeys(self,section):
        if (section not in self.__dsc.Sections):
            return []
        else:            
            return self.__dsc.Sections[section].GetKeys()
    def _GetSection(self,section):
        if (section not in self.__dsc.Sections):
            return None
        else:            
            return self.__dsc.Sections[section]

    #gets the scope that this manipulator acts on
    def _GetScope(self):
        return self.__scope


#this is what applies the manipulations
class DscSectionManipulation(object):
    def __init__(self, dscManipulator, section, history = "N/A", compSection = None):
        self.__dsc = dscManipulator
        self.__section = section
        self.__keys = self.__dsc._GetSectionKeys(self.__section)
        self.__history = history +":"
        self.__isComponent = section.startswith("Components")
        self.__compSection = compSection
    
    #filters the keys in this section
    def Filter(self, filterFunction):
        """ items are kept in if the filter function returns true"""
        self.__keys[:] = [x for x in self.__keys if filterFunction(x)]
        return self

    #filters the keys in this section
    def FilterContains(self, filterValue):
        """ items are kept in if the filter function returns true"""
        self.__keys[:] = [x for x in self.__keys if filterValue in x]
        return self

    def __GetSection(self):        
        section = self.__dsc._GetSection(self.__section)
        return section

    #filters the keys in this section but by value
    def FilterByValue(self, filterFunction):
        """ items are kept in if the filter function returns true"""
        #TODO figure out how this applies to components        
        section = self.__GetSection()
        self.__keys[:] = [x for x in self.__keys if filterFunction(section.Get(x))]
        return self

    # Returns a list of the current filtered Section
    def GetValues(self):
        result = []
        if self.__isComponent and self.__compSection is None:
            for key in self.__keys:
                section = self.__dsc._GetSection(self.__section).GetRaw(key)
                for key in section.GetKeys():
                    if key not in result:
                        result.append(key)            
        else:
            section = self.__GetSection()
            for key in self.__keys:
                result.append(section.Get(key))
        return result

    def HasKey(self,key):
        return key in self.__keys

    def FilterToKey(self,key):
        #TODO check if this is a regex
        self.__keys[:] = [key]
        return self

    def GetKeys(self):
        #returns the keys of the current filtered set
        return self.__keys.copy()

    def ToDict(self):
        # return a dictionary of the current filtered set
        result = {}
        section = self.__GetSection()
        for key in self.__keys:
            result[key] = section.Get(key)
        return result        

    def ResetFilters(self):
        self.__keys = self.__dsc._GetSectionKeys(self.__section)
        return self

    #remove the keys the we are currently filtered to
    def Remove(self, reason):
        section = self.__GetSection()
        for key in self.__keys:
            section.Update(key,None,self.__history+reason, self.__dsc._GetScope())
        return self

    # Applies a transformation a current set based on the filters    
    def Transform(self, transform, reason):
        """transform function must take in two arguments, the key and then the value"""
        section = self.__GetSection()
        for key in self.__keys:
            value = transform(key,section.Get(key))
            section.Update(key,value,self.__history+reason, self.__dsc._GetScope())
        return self

    def Set(self, value, reason):
        """transform function must take in two arguments, the key and then the value"""
        section = self.__GetSection()
        for key in self.__keys:            
            section.Update(key,value,self.__history+reason, self.__dsc._GetScope())
        return self

    # Attempts to add a new value to a particular section
    def AddOrUpdate(self, key, value, reason):
        #logging.critical("Added %s = %s to %s" % (key,value,self.__section))
        section = self.__GetSection().Update(key,value,self.__history+reason, self.__dsc._GetScope())
        return self

    def SetComponentSection(self, section):
        if not self.__isComponent:
            logging.critical("This section manipulator does not handle the component")
        else:
            self.__compSection = section
