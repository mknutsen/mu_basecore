import logging
import io
import re
import os
import collections
from operator import itemgetter, attrgetter

from DscObject import DscValue,DscScopeLevel,DscSection

class FdfSection(DscSection):
    comment = ""
    def __init__(self):
        super().__init__()
        self._values = {}
        self._default = "_values"

    def GetKeyValues(self):
        #Gets the key value pairs-> section, key, value
        keyValues = list()
        for key in self:
            value = self.GetValue(key)
            keyValues.append((self._name,key,value))
        return keyValues


class FdfDefines(FdfSection):
    subsection = False
    def __init__(self):
        super().__init__()
        
        self._globals = {}
        self._default = "_globals"
        self._name = "Defines"

class FdfFD(FdfSection):
    comment = "FD Section# The [FD] Section is made up of the definition statements and a description of what goes into  the Flash Device Image.  Each FD section defines one flash \"device\" image.  A flash device image may be one of the following: Removable media bootable image (like a boot floppy image,) an Option ROM image (that would be \"flashed\" into an add-in\ card,) a System \"Flash\"  image (that would be burned into a system's flash) or an Update (\"Capsule\") image that will be used to update and existing system flash."
    def __init__(self, subsection = ""):
        super().__init__()
        self._name = "FD"
        self.subsection = subsection
        if self.subsection != "":
             self._name = self._name+"."+subsection

class FdfDV(FdfSection):
    def __init__(self, subsection = ""):
        super().__init__()
        self._name = "DV"
        self.subsection = subsection
        if self.subsection != "":
             self._name = self._name+"."+self.subsection

class FdfFV(FdfSection):
    comment = "FV Section#The FV section is used to define what components or modules are placed within a flash device file.  This section also defines order the components and modules are positioned within the image. The [FV] section consists of define statements, set statements and module statements."
    def __init__(self,subsection = ""):
        super().__init__()
        self._name = "FV"
        #TODO only if you're the first subsection to be printed, do you print this comment
        self.subsection = subsection
        if self.subsection != "":
             self._name = self._name+"."+self.subsection
    
class FdfCapsule(FdfSection):
    def __init__(self,subsection = ""):
        super().__init__()
        self._name = "Capsule"
        self.subsection = subsection
        if self.subsection != "":
             self._name = self._name+"."+self.subsection

class FdfFmpPayload(FdfSection):
    def __init__(self,subsection = ""):
        super().__init__()
        self._name = "FmpPayload"
        self.subsection = subsection
        if self.subsection != "":
             self._name = self._name+"."+self.subsection

class FdfRule(FdfSection):
    comment = "Rules are use with the [FV] section's module INF type to define how an FFS file is created for a given INF file. The following Rule are the default rules for the different module type. User can add the customized rules to define the content of the FFS file."
    def __init__(self,subsection = ""):
        super().__init__()
        self._name = "Rule"        
        self.subsection = subsection
        if self.subsection != "":
             self._name = self._name+"."+self.subsection

class FdfVTF(FdfSection):
    def __init__(self,subsection = ""):
        super().__init__()
        self._name = "VTF"
        self.subsection = subsection
        if self.subsection != "":
             self._name = self._name+"."+self.subsection

class FdfOptionRom(FdfSection):
    def __init__(self,subsection = ""):
        super().__init__()
        self._name = "OptionRoom"
        self.subsection = subsection
        if self.subsection != "":
             self._name = self._name+"."+self.subsection

class FdfParser:
    def __init__(self,filename, thebuilder, fdf= None):
        self.filename = filename
        self.currentFileHandle = None
        self.currentLineNum = 0
        self.thebuilder = thebuilder
        self.sectionStartCharacters = "["
        self.filestack = []
        if fdf is None:
            fdf = Fdf()
        self.fdfObj = fdf

    def nextLine(self, eofOnSection=True):
        if (self.currentFileHandle == None or self.currentFileHandle.closed):
            raise "nextLine called but fdffile not open for parsing."
        eof = False
        line = ""
        while(eof == False and line == ""):
            fdfFilePointer = self.currentFileHandle.tell()
            line = self.currentFileHandle.readline()
            self.currentLineNum+=1
            #if line empty before sanitize, EOF
            eof = (line == "")

            #if eof and we still have open files to process, close the include file and resume where we left off in the previous file.
            if (eof and len(self.filestack) > 0):
                self.currentFileHandle.close()
                (self.currentLineNum, self.currentFileHandle) = self.filestack.pop()
                self.fdfFilePointer = self.currentFileHandle.tell()
                line = ""
                eof = False
                continue

            #Strip comments and leading/trailing whitespace
            line = line.split('#')[0].strip()
            #if line empty after sanitize, it's exclusively comments or whitespace and can be ignored.
            if (line == ""):
                continue
            
            #check to see if line is the start of a new section, if so, return EOF.
            if (line[0] in self.sectionStartCharacters and eofOnSection):
                #reset fp to start of line, so that next section header can be consumed
                self.currentFileHandle.seek(fdfFilePointer)
                self.currentLineNum -= 1
                line = ""
                eof = True

    
        return (eof, line)
    
    
    #return the current file and linenumber we are on
    def GetSource(self):
        return self.currentFileHandle.name+":"+str(self.currentLineNum)

    def Parse(self):
        status = 0
        self.currentFileHandle = open(self.filename)
        try:
            while(True):
                (eof, line) = self.nextLine(eofOnSection=False)
                if (eof):
                    break
                
                if not line[0] in self.sectionStartCharacters:
                    print("Unknown line: {0}".format(line))
                    continue
                    raise Exception("Invalid Section Start: {0}".format(line))
                    
                
                #at the top layer, assume section parsers will consume whole sections.
                #so every line we see should be a section declaration. 
                #assume format of the section is "[Section.sub.sub.etc]"
                section = line[1:-1] #strip the []
                self.fdfObj.AddSection(section)
                self.fdfObj.ParseSection(section,self)
                
        except Exception as exc:
            logging.critical("Error in %s line %d: %s" % (self.currentFileHandle.name, self.currentLineNum, exc))
            status = -1
            raise #uncomment to get a trace for debugging.
        
        #close the open files (should only be dsc here unless an exception occurs)
        for (line, file) in self.filestack:
            if (not file.closed):
                file.close()
        if (not self.currentFileHandle.closed):
            self.currentFileHandle.close()

        return self.fdfObj


class Fdf(object):
    SectionTypes = {
        "Defines"    : FdfDefines, 
        "FD"          : FdfFD,
        "DV"          : FdfDV,
        "FV"          : FdfFV,
        "Capsule"     : FdfCapsule,
        "FmpPayload"  : FdfFmpPayload,
        "Rule"        : FdfRule,
        "VTF"         : FdfVTF,
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
            if (elements[0] in Fdf.SectionTypes):
                #Recognizable section - create an entry in self.Sections for it.
                if (len(elements) > 1):
                    #has subsections
                    self.__sections[section] = Fdf.SectionTypes[elements[0]](elements[1])
                else:
                    self.__sections[section] = Fdf.SectionTypes[elements[0]]()
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

    #Sorting routines to order sections per EDK spec for Write
    def subsectionOrder(self,subsection):
        if "common" in subsection:
            return 0
        return 1

    def sortSectionKeys(self):
        sectionList = sorted(self.__sections) #sort alphabetically firsts
        sectionList = sorted(sectionList, key=self.subsectionOrder) #sort subsections
        sectionList = sorted(sectionList, key=self.sectionOrder) #sort sections
        return sectionList

    def Write(self, stream):
        previousSectionType = None
        stream.write("#==================================\n#\tAutogenerated FDF\n#==================================\n")
        for section in self.sortSectionKeys():
            currentSectionType = type(self.__sections[section])
            if previousSectionType is None or currentSectionType != previousSectionType:
                self.__sections[section].WriteComment(stream)
            
            self.__sections[section].Write(stream)
            previousSectionType = currentSectionType

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

    fdf.Write(sys.stdout)
    