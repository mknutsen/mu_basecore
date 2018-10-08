import logging
import io
import re
import os
import collections
from operator import itemgetter, attrgetter


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

    def Renamed(self,oldValue,history):
        self._revisions += 1
        self._value.insert(0,self._value[0]) # put the new value at the front of the array
        self._history.insert(0,"Renamed Key from %s = %s" % (oldValue,history))
        self._scope.insert(0,self._scope[0])
        
    def set(self, newValue, history, scope):

        if (newValue != self._value[0] and self._scope[0] == scope):
            logging.warn("Same scope level conflict of %s for value %s from %s" % (scope, newValue, history))
        
        if (self._scope[0] <= scope):
            self._revisions += 1
            self._value.insert(0,newValue) # put the new value at the front of the array
            self._history.insert(0,history)
            self._scope.insert(0,scope)

        elif (newValue != self._value[0] and self._scope[0] > scope):
            self._revisions += 1
            self._value.insert(1,newValue) # put the new value at the front of the array            
            self._history.insert(1,"Ignored: %s" % (history))
            self._scope.insert(1,scope)
            logging.debug("Ignoring this input %s vs %s" % (newValue, self._value[0]))

    def __str__(self):
        return self._value[0]    

    def Get(self):
        return self._value[0]

    def _GetAllValues(self):
        return list(self._value)

    # get the history for this DSC value
    def History(self):
        def _ConvertHistory(index):
            return " # Revision:%s from %s: scope=%s" %(self._value[index],self._history[index], self._scope[index])
        def _ConvertHistorySingle(index):
            return " # From: %s: scope=%s" %(self._history[index], self._scope[index])
        if len(self._value) == 1:
            historyList = list(map(_ConvertHistorySingle, range(len(self._value))))
        else:
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
    def __init__(self):        
        self._default = "_defines"
        self._defines = {}
        self._name = "DEFAULT_NAME"
        self._seperator = "="
        self._indent = " "
        self._comment = ""
    
    def __iter__(self):
        store = getattr(self,self._default)
        return iter(store)
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
    
    def UpdateDefine(self, key, value, history, scope=DscScopeLevel.default):
        store = self._defines
        if (key not in store):
            store[key] = DscValue(value,history, scope)
        else:
            store[key].set(value, history, scope)

    def Rename(self, key1, key2, history):
        store = getattr(self,self._default)
        if (key1 not in store):
            return None
        else:
            store[key2] = store[key1]
            del store[key1]
            store[key2].Renamed(key1,history)

    def WriteDefines(self,stream):
        #Global defines may be used in FDF, so print them here.
        for k in sorted(self._defines):
            stream.write("%s%s\n" % (self._indent,self.GetHistory(k)))
            if (self.Get(k) is None):
                stream.write("#")    
            stream.write("%sDEFINE %s = %s\n" % (self._indent, k, self.Get(k)))

    def Parse(self,parser):
        while(True):
            (eof, line) = parser.nextLine()
            if (eof):
                break
            #At this point we should have a define element. It's either a macro (prefixed with "DEFINE") or a variable.
            #treat them the same, but if it is a DEFINE, normalize the whitespace between the DEFINE and the variable name to a single space.
            
            tokens = line.split(self._seperator)
            if line.startswith("DEFINE "):
                tokens = line[6:].split(self._seperator)
                
            if len(tokens) != 2:
                logging.critical("ERROR IN DSC PARSER at {0}: Unknown line {1}".format(parser.GetSource(),line) )
            else:
                key = " ".join(tokens[0].strip().split())
                value = tokens[1].strip()
                if line.startswith("DEFINE "):
                    self.UpdateDefine(key,value,parser.GetSource())
                else:
                    self.Update(key,value,parser.GetSource())
                    

    def WriteName(self,stream):
        stream.write("%s[%s]\n" % (self._indent,self._name))

    def WriteComment(self,stream):
        _comment = type(self).comment.strip()
        if len(_comment) == 0:
            return
        stream.write("################################################################################\n")
        commentLines = _comment.split("#")
        commentIndex = 0
        for comment in commentLines:
            commentIndex += 1
            if len(comment) > 78:
                breakPoint = 78
                # walk until we find a break in a word
                while comment[breakPoint] != " " and breakPoint > 50:
                    breakPoint -= 1
                comment2 = comment[breakPoint:]
                comment = comment[0:breakPoint]
                commentLines.insert(commentIndex,comment2)
                
            stream.write("# %s\n" % comment)
            
        
        stream.write("################################################################################\n")

    def Write(self, stream):
        
        self.WriteName(stream)
        store = getattr(self,self._default)
        self.WriteDefines(stream)
        for k in sorted(self.GetKeys()):
            stream.write("%s %s\n" % (self._indent,self.GetHistory(k)))
            if k == "NULL":
                for value in store[k]._GetAllValues(): 
                    stream.write("%s %s%s%s\n" % (self._indent,k, self._seperator,value))
            else:            
                if (self.Get(k) is None):
                    stream.write("#")
                stream.write("%s %s%s%s\n" % (self._indent,k, self._seperator,self.Get(k)))
        stream.write("\n")

class DscComponentSection(DscSection):
    def __init__(self):        
        super().__init__()
        self._indent = "\t\t"

    def WriteName(self, stream):
        stream.write("%s<%s>\n" % (self._indent,self._name))

#[Defines] section parser class.
class DscDefines(DscSection):
    def __init__(self):
        super().__init__()
        self._globals = {}
        self._default = "_globals"
        self._name = "Defines"
    
#[SkuIds] section parser class
class DscSkus(DscSection):
    def __init__(self):
        super().__init__()
        self._skus = {}
        self._default = "_skus"
        self._name = "Skus"
    
#[LibraryClasses] section parser class. Handles subsections (e.g. LibraryClasses.IA32) as well.
class DscLibraryClasses(DscSection):
    def __init__(self, subsection=""):
        super().__init__()
        self._libclasses = {}
        self.subsection = subsection
        self._default = "_libclasses"
        self._name = "LibraryClasses"
        if self.subsection != "":
             self._name = self._name+"."+self.subsection
        self._seperator = "|"
    
    def sortedLibClasses(self):
        sortedClasses = collections.OrderedDict(sorted(self._libclasses.items())) #sort alphabetically
        sortedClasses = collections.OrderedDict(sorted(sortedClasses.items(), key=itemgetter(1))) #then sort by path
        return sortedClasses
    
#[Pcds*] section parser class. Subsection is e.g. "FixedAtBuild"
class DscPcds(DscSection):
    def __init__(self, subsection):
        super().__init__()
        self._pcds = {}
        self.subsection = subsection
        self._default = "_pcds"
        self._name = "Pcds"+subsection
        self._seperator = "|"
    
#<LibraryClasses> option parser for components.
class DscComponentLibraryClasses(DscComponentSection):
    def __init__(self):
        self.libclasses = []
        self._libs = {}
        super().__init__()
        self._name = "LibraryClasses"
        self._default = "_libs"
        self._seperator = "|"

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
class DscComponentPcds(DscComponentSection):
    def __init__(self, subsection):
        super().__init__()
        self._pcds = {}
        self.subsection = subsection
        self._default = "_pcds"
        self._name = "Pcds"+subsection
        self._seperator = "|"

#<BuildOptions> option parser for components.
class DscComponentBuildOptions(DscComponentSection):
    def __init__(self):
        super().__init__()
        self._options = {}
        self._name = "BuildOptions"
        self._default = "_options"

class DscComponentDefines(DscComponentSection):
    def __init__(self):
        super().__init__()
        self._overrides = {}
        self._name = "Defines"
        self._default = "_overrides"


#Component parser.
#Parses the inf path,and then delegates parsing of options subsections to the option parsers above.
class DscComponent(DscSection):

    OptionTypes = {"LibraryClasses" : DscComponentLibraryClasses,
                   "Pcds"           : DscComponentPcds,
                   "BuildOptions"   : DscComponentBuildOptions,
                   "Defines"        : DscComponentDefines,
                   }

    def __init__(self, subsection):
        super().__init__()
        self.componentPath = ""
        self._options = {}
        self._default = "_options"
        self.subsection = subsection
        self.basename = ""
        self.fileguid = ""
        self.moduleType = ""
        self.isLibrary = False
        
    
    def resolveLib(self, libname):
        #if "LibraryClasses" not in self._options:
            #self.Update("LibraryClasses",DscComponent.OptionTypes["LibraryClasses"](self.parser),self.parser.GetSource())            
        return self.GetRaw("LibraryClasses").getLibrary(self, libname)

    def Parse(self, parser):
        while(True):
            (eof, line) = parser.nextLine()
            if (eof):
                return False
            #if "}", done with extended parsing
            if (line[0] == "}"):
                break
            #should be a options section header
            #assume format of the header is "<Option>"
            option = line[1:-1] #strip the <>
            if (option not in self._options):
                #self.option doesn't have this option clause yet
                if (option in DscComponent.OptionTypes):
                    #Recognizable option - create an entry in self.options for it.
                    component = DscComponent.OptionTypes[option]()
                    self.Update(option, component, parser.GetSource())
                #Pcds are weird. Handle them special.
                elif (option[0:4] in DscComponent.OptionTypes):
                    component = DscComponent.OptionTypes[option[0:4]](option[4:])
                    self.Update(option, component, parser.GetSource())
                else:
                    #unrecognized section or line
                    raise Exception("Unrecognized section or line in DSC Component: %s" % line)

            #If we get here, we have a parser for this option. Switch the end of section marker, then use it!
            parser.setSectionChars("<}")
            self.GetRaw(option).Parse(parser)
            parser.clearSectionChars()

    def Write(self, stream):        
        self.WriteDefines(stream)
        for k in sorted(self.GetKeys()):
            stream.write("%s\n" % (self.GetHistory(k)))
            value = self.GetRaw(k)
            if value:
                value.Write(stream)
        stream.write("\n")   
    
    

#[Components] section parser. Subsection is e.g. "X64".
class DscComponents(DscSection):
    def __init__(self, subsection = ""):
        super().__init__()
        self._components = {}
        self._default = "_components"
        self.subsection = subsection
        self._name = "Components"
        if self.subsection != "":
             self._name = "Components."+self.subsection

    def Parse(self, parser):
        while(True):            
             #Grab the component path
            (eof, line) = parser.nextLine()
            if (eof):                
                return False
            component = None
            componentPath = line
            if (line[-1] == "{"):
                component = DscComponent(self.subsection)
                componentPath = line[:-1].strip() #remove the { from the component name            
                component.Parse(parser)
            self.Update(componentPath,component, parser.GetSource())

    def Write(self, stream):
        self.WriteName(stream)
        self.WriteDefines(stream)
        for k in sorted(self.GetKeys()):
            stream.write("%s %s\n" % (self._indent,self.GetHistory(k)))
            stream.write("%s %s" % (self._indent,k))
            value = self.GetRaw(k)
            if value:
                stream.write("{\n")
                value.Write(stream)
                stream.write("}\n")
            else:
                stream.write("\n")
        stream.write("\n")   
    
    
#[BuildOptions] section parser.
class DscBuildOptions(DscSection):
    def __init__(self):
        super().__init__()
        self.buildappend = {}
        self.buildreplace = {}
        self._default = "_options"
        self._name = "BuildOptions"
        self._options = {}

class DscParser:
    def __init__(self,dscfilename, thebuilder, dsc):
        self.dscfilename = dscfilename
        self.dscfh = None
        self.dscfp = None
        self.dscline = 0
        self.thebuilder = thebuilder
        self.eofOnSectionChars = "["
        self.filestack = []
        self.conditionalstack = []
        self.dsc = dsc

     #Given a path, use thebuilder.mws.join to resolve it to a system file path
    def resolvePath(self, path):        
        return self.thebuilder.mws.join(self.thebuilder.ws, path)

    #Given a regex match object, get the varname from it and use thebuilder.env to resolve it.
    def resolveVariableRe(self, match):
        value = self.resolveVariable(match.group())
        if (value == None):
            value = match.group() #if the variable could not be resolved, leave it as the variable name.
        return value
     #Given a component and a library, resolve it to the library inf that satisfies this instance.
    def resolveLibraryInstance(self, component, library):
        libclasses = []
        if ("LibraryClasses."+component.subsection+"."+component.moduleType in self.dsc):
            libraryInst = self.dsc.GetValue("LibraryClasses."+component.subsection+"."+component.moduleType,library)
            if (libraryInst != None):
                return libraryInst

        if ("LibraryClasses."+component.subsection in self.dsc):
            libraryInst = self.dsc.GetValue("LibraryClasses."+component.subsection,library)
            if (libraryInst != None):
                return libraryInst
        if ("LibraryClasses.common" in self.dsc):
            libraryInst = self.dsc.GetValue("LibraryClasses.common",library)
            if (libraryInst != None):
                return libraryInst

        raise Exception("Can't find " + library + "referenced in " + component.componentPath + " in LibraryClasses")
        #return ""

    #check for exceptional variables. There are a few places where resolving a variable in the DSC that's intended for consumption elsewhere causes problems.
    #TODO: there's got to be a better way to deal with this.
    def checkVariableExceptions(self,varname):
        if ("MICROSOFT_WORKAROUND" in varname):
            return (True, None)
        return (False, None)
    

    def resolveVariable(self, varname):
        value = None
        #Check for special variables
        (requiresException, value) = self.checkVariableExceptions(varname)
        if (requiresException):
            return value
        
        #Convert variable $(FOO) to value of environment var FOO. Consult section defines, then global defines, then pcds, then builder as last resort.
        value = self.dsc.GetValue(self.currentSection,varname[2:-1])
        if (value == None):
            for section in self.dsc:
                if (section.startswith("Pcds") and value == None):
                    value = self.dsc.GetValue(section,varname)
                if (value != None):
                    logging.info("Resolved as PCD value")

        if (value == None):            
            value = self.thebuilder.env.GetBuildValue(varname[2:-1])
            if (value != None):
                logging.info("Resolved as build value")

        if (value == None):            
            value = self.thebuilder.env.GetValue(varname[2:-1])
            if (value != None):
                logging.info("Resolved as env value")
        
        
        logging.info("Var %s resolved as %s" % (varname,value))
        return resolveGuid(value)

   
    #
    # Expression handling. Parse expressions using the Shunting Yard algorithm:
    # https://en.wikipedia.org/wiki/Shunting-yard_algorithm
    #
    
    #doOp - given the operation and value stack, perform the operation and push the result on the value stack
    #TODO: implement all the operators; right now only those present in our DSCs are implemented.
    def doOp(self, op, valuestack):
        if (op == "==" or op == "!="):
            val1 = valuestack.pop()
            val2 = valuestack.pop()
            if ((isinstance(val1, str) and isinstance(val2, str)) or
                (isinstance(val1, int) and isinstance(val2, int))):
                if (op == "=="):
                    valuestack.append(int(val1==val2))
                else:
                    valuestack.append(int(val1!=val2))
                return
            valuestack.append(0)
            return
        raise Exception("Unsupported op: %s! You should add support in DscPreProcessor.Dsc.doOp()." % op)

    #Evaluate the expression
    def evaluateConditional(self, line):
        #Do the easy ones first
        if (line.startswith("!ifdef")):
            #Spec allows both $(FOO) and FOO here. Need to handle both. If either found, then return true
            val = self.resolveVariable(line.split(maxsplit=1)[1])
            if (val == None):
                #add $() and check again
                val = self.resolveVariable("$(" + line.split(maxsplit=1)[1]+")")
            return (val != None) 

        if (line.startswith("!ifndef")):
            val = self.resolveVariable(line.split(maxsplit=1)[1])
            if (val == None):
                #add $() and check again
                val = self.resolveVariable("$(" + line.split(maxsplit=1)[1]+")")
            return (val == None)
        
        #now handle the ones that actually require expression parsing.
        #following lists operators and precedence defined in EDKII DSC spec.
        operators = {"or"  : 0, "||" : 0,
                     "and" : 1, "&&" : 1,
                     "|"   : 2,
                     "xor" : 3, "^"  : 3,
                     "&"   : 4,
                     "eq"  : 5, "==" : 5, "ne" : 5, "!=" : 5, "in" : 5,
                     "<="  : 6, "le" : 6, "<"  : 6, "lt" : 6, ">=" : 6, "ge" : 6, ">" : 6, "gt" : 6,
                     "+"   : 7, "-"  : 7,
                     "not" : 8, "!"  : 8}

        valstack = []
        opstack = []
        #This routine assumes that everything is nicely space-delimited. DSC spec generally requires this
        #though it has some ambiguity around parentheses. May need to go through and add spaces on either side of
        #"(" and ")" (whene they are not part of a variable specifier) if this is actually a problem.
        for token in line.split():
            #value cases (token is not an operator or paren)
            #attempt to resolve variable. Could be $() or PCD. 
            val = self.resolveVariable(token)
            #if val is none, but is a $() macro, push 0 on stack and proceed to next token.
            if (val == None and token[0] == "$"):
                valstack.append(0)
                continue
            
            #if variable resolves, use it instead of the token.
            if (val != None):
                token = val

            if (token[0] == "\""):
                valstack.append(token[1:-1])
                continue
            if (token.lstrip('-').replace('.','',1).isdigit()):
                valstack.append(float(token))
                continue
            if (token.lower() == "true"):
                valstack.append(1)
                continue
            if (token.lower() == "false"):
                valstack.append(0)
                continue

            #operator cases (token is an operator or a left paren)
            #handle left paren - push it on the stack
            if (token[0] == "("):
                opstack.append("(")
                continue

            #handle right paren - pop and process ops off the opstack until we find the left paren.
            if (token[0] == ")"):
                while (opstack[-1] != "("):
                    self.doOp(opstack.pop(), valstack)
                opstack.pop()
                continue

            #handle operators.
            if (token in operators):
                #pop higher-precedence operators off the stack and process them until we find an op of lower or equal precedence.
                while(len(opstack) > 0 and operators[opstack[-1]]>=operators[token]):
                    self.doOp(opstack.pop(), valstack)
                opstack.append(token)
                continue
            
            #if we get here, we have a token we don't really recognize. just assume the token is a string value without quotes.
            valstack.append(token)

        #all tokens have been processed; now just drain the opstack
        while(len(opstack) > 0):
            self.doOp(opstack.pop(), valstack)

        if (valstack.pop() == 0):
            return False

        return True

    #Handle conditions. Keep track of nested conditions with a stack. If the current conditional flag
    #at the top of the stack is false, it means the line will be ignored (unless it is another conditional)
    def handleConditional(self, line):
        #endif means we can remove the top conditional from the stack.
        if (line.startswith("!endif")):
            self.conditionalstack.pop()
            return
        #else means that we invert the top conditional on the stack.
        if (line.startswith("!else")):
            condition = not self.conditionalstack.pop()
        
        #if means evaluate the condition and push the result on the stack.
        if (line.startswith("!if")):
            condition = self.evaluateConditional(line)

        self.conditionalstack.append(condition)

    #This routine allows elements of the parsing algorithm to change the "end of section" identifier.
    def setSectionChars(self, chars):
        self.eofOnSectionChars = chars
    
    #This routine sets the end of section identifier back to the default.
    def clearSectionChars(self):
        self.eofOnSectionChars = "["

        #
    # Parser core: this routine reads the next line from the file, sanitizes it, and handles
    # any special stuff (like conditionals and includes)
    def nextLine(self, eofOnSection=True):
        if (self.dscfh == None or self.dscfh.closed):
            raise "nextLine called but dscfile not open for parsing."
        eof = False
        line = ""
        while(eof == False and line == ""):
            dscfp = self.dscfh.tell()
            line = self.dscfh.readline()
            self.dscline+=1
            #if line empty before sanitize, EOF
            eof = (line == "")
            
            #if eof and we still have open files to process, close the include file and resume where we left off in the previous file.
            if (eof and len(self.filestack) > 0):
                self.dscfh.close()
                (self.dscline, self.dscfh) = self.filestack.pop()
                self.dscfp = self.dscfh.tell()
                line = ""
                eof = False
                continue

            #Strip comments and leading/trailing whitespace
            line = line.split('#')[0].strip()
            #if line empty after sanitize, it's exclusively comments or whitespace and can be ignored.
            if (line == ""):
                continue

            #handle conditionals.
            if (line[0] == '!' and not line.startswith("!include")):
                self.handleConditional(line)
                line = ""
                continue

            #if current top of conditional stack is false, ignore non-conditional lines
            if (len(self.conditionalstack) > 0 and self.conditionalstack[-1] == False):
                line = ""
                continue

            #resolve variables
            line = re.sub('\$\(.*?\)', self.resolveVariableRe, line)

            #if !include, push the current file on the filestack, and open the new file to continue processing.
            if (line.startswith("!include")):
                try: 
                    self.filestack.append((self.dscline, self.dscfh))
                    self.dscfh = open(self.resolvePath(line.split()[1]))
                    self.dscline = 0
                    self.dscfp = self.dscfh.tell()
                    line = ""
                except IOError as e:
                    logging.critical('Unable to open file %s ' % line.split()[1])
                    (self.dscline, self.dscfh) = self.filestack.pop()
                    self.dscfp = self.dscfh.tell()
                    line = ""
                continue

            #handle DEFINE macros. 
            #TODO: These could occur anywhere (e.g. in component option subsections), but this only scopes
            #down to section level. 
            if (line.startswith("DEFINE")):
                macro = line[6:].split("=")
                self.dsc.UpdateOrCreateValue(self.currentSection,macro[0].strip(), macro[1].strip(), self.GetSource())
                line = ""
                continue

            #check to see if line is the start of a new section, if so, return EOF.
            if (line[0] in self.eofOnSectionChars and eofOnSection):
                #reset fp to start of line, so that next section header can be consumed
                self.dscfh.seek(dscfp)
                self.dscline -= 1
                line = ""
                eof = True
            
        return (eof, line)
    ##
    #return the current file and linenumber we are on
    ##
    def GetSource(self):
        return self.dscfilename+":"+str(self.dscline)

    def Parse(self):
        status = 0
        self.dscfh = open(self.dscfilename)
        try:
            while(True):
                (eof, line) = self.nextLine(eofOnSection=False)
                if (eof):
                    break

                #at the top layer, assume section parsers will consume whole sections.
                #so every line we see should be a section declaration. 
                #assume format of the section is "[Section.sub.sub.etc]"
                section = line[1:-1] #strip the []
                self.dsc.AddSection(section)
                
                #If we get here, we have a parser for this section. Use it!
                self.currentSection = section
                self.dsc.ParseSection(self.currentSection,self)
                #figure out how to parse it?
        except Exception as exc:
            logging.critical("Error in %s line %d: %s" % (self.dscfh.name, self.dscline, exc))
            status = -1
            raise #uncomment to get a trace for debugging.
        
        #close the open files (should only be dsc here unless an exception occurs)
        for (line, file) in self.filestack:
            if (not file.closed):
                file.close()
        if (not self.dscfh.closed):
            self.dscfh.close()

        '''for componentSection in self.dsc.GetListOfSections():
            if componentSection.startswith("Component"):
                for componentKey in self.Sections[componentSection]._components:
                    component = self.Sections[componentSection].GetRaw(componentKey)
                    component.parseComponentFile()'''

        return status

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

    def __iter__(self):
        return iter(self.__sections)

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
                    self.__sections[section] = Dsc.SectionTypes[elements[0]](elements[1])
                else:
                    self.__sections[section] = Dsc.SectionTypes[elements[0]]()
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
        self.AddSection(section)
        return self.__sections[section].GetRaw(key)

    def _GetSectionKeys(self,section):
        if (section not in self.__sections):
            return []
        else:            
            return self.__sections[section].GetKeys()

    def _GetSectionTypeKeyValues(self,sectionType):
        keyValues = []
        for section in self.__sections:
            if section.startswith(sectionType):
                if section.startswith("Components"):
                    sectionKeys = self._GetSectionKeys(section)
                    for key in sectionKeys:
                        module = self.GetValue(section,key)
                        if module is None:
                            keyValues.append((section,key,None,None,None))
                        else:
                            for subsection in module:
                                subSectionValue = module.GetRaw(subsection)
                                for subSectionKey in subSectionValue:
                                    value = str(subSectionValue.GetRaw(subSectionKey))
                                    keyValues.append((section,key,subsection,subSectionKey,value))
                
                else:
                    sectionKeys = self._GetSectionKeys(section)
                    for key in sectionKeys:
                        value = str(self.GetValue(section,key))
                        keyValues.append((section,key,value))
        return keyValues
        
            
    def _GetSection(self,section):
        if (section not in self.__sections):
            return None
        else:            
            return self.__sections[section]

        
    #Sorting routines to order sections per EDK spec for Write
    def subsectionOrder(self,subsection):
        if "common" in subsection:
            return 0
        return 1

    def sectionOrder(self,section):
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
        sectionList = sorted(sectionList, key=self.subsectionOrder) #sort subsections
        sectionList = sorted(sectionList, key=self.sectionOrder) #sort sections
        return sectionList

    def Write(self, stream):
        for section in self.sortSectionKeys():
            self.__sections[section].Write(stream)

    def Parse(self, dscfilename, thebuilder):
        parser = DscParser(dscfilename, thebuilder, self)
        return parser.Parse()

    def ParseSection(self, section, parser):
        self.__sections[section].Parse(parser)

###
## Manipulators
###

class DSCSectionManipulator(object):
    def __init__(self, baseDSC, section, source):
        self._dsc = baseDSC
        self._section = section
        self._source = source
        self._keyFilters = []
        self._sectionFilters = []
        self._valueFilters = []
    # the data for a section is
    # 0 => component subsection (PcdsFixedAtBuild.IPF)
    # 1 => Key (gEfiMdePkgTokenSpaceGuid.PcdIoBlockBaseAddressForIpf)
    # 2 => Value (0x0ffffc000000)
    
    def KeyFilter(self, filterFunc):
        self._keyFilters.append(filterFunc)
        return self
    
    def ValueFilter(self, filterFunc):
        self._valueFilters.append(filterFunc)
        return self
    
    def SectionFilter(self, filterFunc):
        self._sectionFilters.append(filterFunc)
        return self

    def Reset(self):
        self.ClearFilters()

    def ClearFilters(self):
        self._keyFilters = []
        self._valueFilters = []
        self._sectionFilters = []

    def _GetSectKeyValues(self):
        keyValues = self._dsc._GetSectionTypeKeyValues(self._section)
        return keyValues

    def _FilterSectKeys(self):
        keyValues = self._GetSectKeyValues()
        # run the section filters
        keyValues = self._RunSectionFilters(keyValues)
        #Run the key filters
        keyValues = self._RunKeyFilters(keyValues)
        # run the value filters
        keyValues = self._RunValueFilters(keyValues)

        return keyValues
    
    def _RunKeyFilters(self,keyValues):
        # run the key filters        
       return self._RunFilter(self._keyFilters,keyValues,1)

    def _RunSectionFilters(self,keyValues):
        # run the key filters
       return self._RunFilter(self._sectionFilters,keyValues,0)
    
    def _RunValueFilters(self,keyValues):
        # run the key filters        
        return self._RunFilter(self._valueFilters,keyValues,2)

    def GetKeys(self):
        keys = self._FilterSectKeys()
        return [key[1] for key in keys]

    def MapKeys(self, mapFunc, reason="MapKeys"):
        keys = self._FilterSectKeys()
        #TODO filter down to just the unique combos of 0 and 1
        for data in keys:
            dscSection = self._dsc._GetSection(data[0])
            newKey = mapFunc(data[1])
            dscSection.Rename(data[1],newKey,reason)

        return self

    def MapValues(self, mapFunc, reason="MapValues"):
        keys = self._FilterSectKeys()
        for data in keys:
            dscSection = self._dsc._GetSection(data[0])
            newValue = mapFunc(data[2])
            dscSection.Update(data[1],newValue,reason)

        return self

    def _RunFilter(self, filterList, keyValues, tupleIndex):
        for KeyFilter in filterList:
            index = tupleIndex
            if isinstance(KeyFilter, str):
                keyValues[:] = [x for x in keyValues if str(x[index]) == KeyFilter or str(x[index]).startswith(KeyFilter)]
                
            else:
                #keyValues[:] = [x for x in keyValues if KeyFilter(x[0])]
                keyValues[:] = [x for x in keyValues if KeyFilter(x[index])]

        return keyValues



class DSCDefinesSectionManipulator(DSCSectionManipulator):
    def __init__(self, baseDSC, source):
        super().__init__(baseDSC,"Defines", source)

class DSCComponentSectionManipulator(DSCSectionManipulator):
    def __init__(self, baseDSC, section, source):
        super().__init__(baseDSC,section, source)
        self._infFilters = []
        self._subsectionFilters = []

    # the data for a compoenent section is
    # 0 => Section component subsection (Components.x64)
    # 1 => Module (MdeModulePkg/Universal/ResetSystemRuntimeDxe/ResetSystemRuntimeDxe.inf)
    # 2 => SubSection (<LibraryClasses>)
    # 3 => Key (ResetSystemLib)
    # 4 => Value (MdeModulePkg/Library/BaseResetSystemLibNull/BaseResetSystemLibNull.inf)
    
    def _FilterSectKeys(self):
        keyValues = super()._FilterSectKeys() 
        keyValues = self._RunSubSectionFilters(keyValues)
        keyValues = self._RunModuleFilters(keyValues)        
        return keyValues
  
    def _RunValueFilters(self,keyValues):
        # run the key filters        
        return self._RunFilter(self._valueFilters,keyValues,2)

    def _RunModuleFilters(self, keyValues):
        # run the key filters
        return self._RunFilter(self._infFilters,keyValues,1)

    def _RunSubSectionFilters(self,keyValues):
        # run the key filters
        return self._RunFilter(self._subsectionFilters,keyValues,2)

    def _RunKeyFilters(self,keyValues):
        # run the key filters        
        return self._RunFilter(self._keyFilters,keyValues,3)
    
    def _RunValueFilters(self,keyValues):
        # run the key filters        
        return self._RunFilter(self._valueFilters,keyValues,4)

    def ModuleFilter(self, filterFunc):
        self._infFilters.append(filterFunc)
        return self

    def MapModules(self, mapFunc, reason="MapKeys"):        
        super().MapKeys(mapFunc,reason)
        return self
    
    def MapKeys(self, mapFunc, reason="MapKeys"):
        keys = self._FilterSectKeys()
        for data in keys:
            if data[3] is None:
                continue
            dscSection = self._dsc._GetSection(data[0])
            dscSection = dscSection.GetRaw(data[1])
            dscSection = dscSection.GetRaw(data[2])
            newKey = mapFunc(data[3])
            dscSection.Rename(data[3],newKey,reason)

        return self

    def MapValues(self, mapFunc, reason="MapKeys"):
        keys = self._FilterSectKeys()
        for data in keys:
            if data[3] is None:
                continue
            dscSection = self._dsc._GetSection(data[0])
            dscSection = dscSection.GetRaw(data[1])
            dscSection = dscSection.GetRaw(data[2])
            newValue = mapFunc(data[4])
            dscSection.Update(data[3],newValue,reason)

        return self
        
    def SubsectionFilter(self, filterFunc):
        self._subsectionFilters.append(filterFunc)
        return self

    def ClearFilters(self):
        super().ClearFilters()
        self._infFilters = []
        self._subsectionFilters = []

        

class DscManipulator(object):
    def __init__(self, baseDSC, source, scope=DscScopeLevel.default):
        self.__dsc = baseDSC
        self.__source = source
        self.__scope = scope
    
        self.defines = self.GetSection("Defines")
        self.skuids = self.GetSection("SkuIds")
        self.libraryclasses = self.GetSection("LibraryClasses")
        self.pcds = self.GetSection("Pcds")
        self.components = self.GetSection("Components")
        self.buildoptions = self.GetSection("BuildOptions")

    # Gets a list of all the current selection
    def GetListOfSections(self):
        return list(self.__dsc.Sections.keys())

    # This will get the section Type
    def GetSection(self,section):
        if section.startswith("Components"):
            return DSCComponentSectionManipulator(self.__dsc,section,self.__source)
        if section.startswith("Defines"):
            return DSCDefinesSectionManipulator(self.__dsc,self.__source)
        else:
            return DSCSectionManipulator(self.__dsc,section,self.__source)

        raise Exception("Unrecognized section trying to be requested: %s" % section)
        return None

    #Gets a section and then returns it the section type
    def AddOrGetSection(self, section):
        self.__dsc.AddSection(section)
        return self.GetSection(section)

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
