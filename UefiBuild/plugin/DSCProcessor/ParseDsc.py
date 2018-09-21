import logging
import io
import re
import os
import collections
from operator import itemgetter, attrgetter
from DscProcessor import EnumDscPluginScopeLevel


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
        self._defines = {}
        self._default = "_defines"
    
   
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

    def Update(self, key, value, history, scope=EnumDscPluginScopeLevel.default):
        store = getattr(self,self._default)
        if (key not in store):
            store[key] = DscValue(value,history, scope)
        else:
            store[key].set(value, history, scope)

    def Write(self, stream):
        for k in sorted(self._defines):
            stream.write("%s\n" % (self.GetHistory(k)))
            if (self.Get(k) is None):
                stream.write("#")    
            stream.write("    DEFINE %s = %s\n" % (k, self.Get(k)))

#[Defines] section parser class.
class DscDefines(DscSection):
    def __init__(self, dscparser):
        super().__init__(dscparser)
        self.parser = dscparser
        self.globals = {}
        self._default = "globals"

    def Parse(self):
        while(True):
            (eof, line) = self.parser.nextLine()
            if (eof):
                break
            
            #At this point we should have a define element. It's either a macro (prefixed with "DEFINE") or a variable.
            #treat them the same, but if it is a DEFINE, normalize the whitespace between the DEFINE and the variable name to a single space.
            tokens = line.split('=')
            key = " ".join(tokens[0].strip().split())
            value = tokens[1].strip()
            self.Update(key,value,self.parser.GetSource())

    def Write(self, stream):
        stream.write("[Defines]\n")
        #Global defines may be used in FDF, so print them here.
        super().Write(stream)
        for k in sorted(self.globals):
            stream.write("%s\n" % (self.GetHistory(k)))
            if (self.Get(k) is None):
                stream.write("#")
            stream.write("    %s = %s\n" % (k, self.Get(k)))
        stream.write("\n")

#[SkuIds] section parser class
class DscSkus(DscSection):
    def __init__(self, dscparser):
        super().__init__(dscparser)
        self.skus = {}
        self.parser = dscparser
        self._default = "skus"

    def Parse(self):
        while(True):
            (eof, line) = self.parser.nextLine()
            if (eof):
                break
            
            #At this point we should have a SKU elememt. Split on the pipe and store it. 
            tokens = line.split('|')
            key = tokens[0].strip()
            value = tokens[1].strip()
            self.Update(key,value,self.parser.GetSource())

    def Write(self, stream):
        stream.write("[SkuIds]\n")
        for k in self.skus:
            stream.write("%s\n" % (self.GetHistory(k)))
            if (self.Get(k) is None):
                stream.write("#")
            stream.write("    %s|%s\n" %(k, self.Get(k)))
        stream.write("\n")

#[LibraryClasses] section parser class. Handles subsections (e.g. LibraryClasses.IA32) as well.
class DscLibraryClasses(DscSection):
    def __init__(self, dscparser, subsection):
        super().__init__(dscparser)
        self._libclasses = {}
        self.parser = dscparser
        self.subsection = subsection
        self._default = "_libclasses"
    
    def Parse(self):
        while(True):
            (eof, line) = self.parser.nextLine()
            if (eof):
                break
            
            #At this point we should have a library class elememt. Split on the pipe and store it.
            tokens = line.split('|')
            key = tokens[0].strip()
            value = tokens[1].strip()
            self.Update(key,value,self.parser.GetSource())

    def sortedLibClasses(libclasses):
        sortedClasses = collections.OrderedDict(sorted(libclasses.items())) #sort alphabetically
        sortedClasses = collections.OrderedDict(sorted(sortedClasses.items(), key=itemgetter(1))) #then sort by path
        return sortedClasses
    
    def Write(self, stream):
        stream.write("[LibraryClasses.%s]\n" % self.subsection)
        if (len(self._libclasses) > 0):
            maxkeylen = max(len(k) for k in self._libclasses) + 1
            for k in DscLibraryClasses.sortedLibClasses(self._libclasses):
                formatStr = "    {:" + str(maxkeylen) +"}|{}\n"
                stream.write("%s\n" % (self.GetHistory(k)))
                if (self.Get(k) is None):
                    stream.write("#")
                stream.write(formatStr.format(k, self.Get(k)))
        stream.write("\n")

#[Pcds*] section parser class. Subsection is e.g. "FixedAtBuild"
class DscPcds(DscSection):
    def __init__(self, dscparser, subsection):
        super().__init__(dscparser)
        self._pcds = {}
        self.parser = dscparser
        self.subsection = subsection
        self._default = "_pcds"
        
    def Parse(self):
        while (True):
            (eof, line) = self.parser.nextLine()
            if (eof):
                break
            
            #At this point we should have a PCD element.  Split on the pipe and store it.
            tokens = line.split('|')
            #self.pcds[tokens[0].strip()] = tokens[1].strip()
            key = tokens[0].strip()
            value = tokens[1].strip()
            self.Update(key,value,self.parser.GetSource())

    def Write(self, stream):
        stream.write("[Pcds%s]\n" % self.subsection)
        for k in sorted(self._pcds):
            stream.write("%s\n" % (self.GetHistory(k)))
            if (self.Get(k) is None):
                stream.write("#")
            stream.write("    %s|%s\n" % (k, self.Get(k)))
        stream.write("\n")

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

    def Parse(self):
        while(True):
            (eof, line) = self.parser.nextLine()
            if (eof):
                break
            
            #At this point we should have a library class elememt. Split on the pipe and store it.
            tokens = line.split('|')
            self.libclasses.append((tokens[0].strip(), tokens[1].strip(), "LibraryClass Override"))
    
    def Write(self, stream):
        stream.write("        <LibraryClasses>\n")
        maxKeyLength = max(len(k) for (k, v, s) in self.libclasses)
        for (k,v,s) in self.libclasses:
            if (s != None):
                stream.write("            #Source: %s\n" % (s))
            stream.write("            %-*s  |%s\n" % (maxKeyLength,k, v))

#<Pcds*> option parser for components.
class DscComponentPcds(DscSection):
    def __init__(self, dscparser, subsection):
        self._pcds = {}
        self.parser = dscparser
        self.subsection = subsection
        self._default = "_pcds"

    def Parse(self):
        while(True):
            (eof, line) = self.parser.nextLine()
            if (eof):
                break
            
            #At this point we should have a pcd elememt. Split on the pipe and store it.
            tokens = line.split('|')
            key = tokens[0].strip()
            value = tokens[1].strip()
            self.Update(key,value,self.parser.GetSource())
            #self.pcds[tokens[0].strip()] = tokens[1].strip()
    
    def Write(self, stream):
        stream.write("         <Pcds%s>\n" % self.subsection)
        for k in sorted(self._pcds):
            stream.write("%s\n" % (self.GetHistory(k)))
            if (self.Get(k) is None):
                stream.write("#")
            stream.write("            %s|%s\n" % (k, self.Get(k)))

#<BuildOptions> option parser for components.
class DscComponentBuildOptions(object):
    def __init__(self, dscparser):
        self.buildappend = {}
        self.buildreplace = {}
        self.parser = dscparser

    
    def Parse(self):
        while(True):
            (eof, line) = self.parser.nextLine()
            if (eof):
                break
            
            buildopt = line.split(maxsplit=2)
            if (buildopt[1] == "="):
                if (buildopt[0] in self.buildappend):
                    self.buildappend[buildopt[0]] += " " + buildopt[2]
                else:
                    self.buildappend[buildopt[0]] = buildopt[2]
            else:
                self.buildreplace[buildopt[0]] = buildopt[2]

    def Write(self, stream):
        stream.write("        <BuildOptions>\n")
        for k in sorted(self.buildappend):
            stream.write("            %s=%s\n" % (k, self.buildappend[k]))
        for k in sorted(self.buildreplace):
            stream.write("            %s==%s\n" % (k, self.buildreplace[k]))

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
   
    
    def parseComponentFile(self):
        infFile = self.parser.resolvePath(self.componentPath.split("{")[0])
        try:
            with open(infFile) as inf:
                line = inf.readline()
                while(line != ""):
                    if ("BASE_NAME" in line):
                        self.basename = line.split("=")[1].strip().split(" ")[0].strip()
                    if ("FILE_GUID" in line):
                        self.fileguid = line.split("=")[1].strip().split(" ")[0].strip()
                    if ("MODULE_TYPE" in line):
                        self.moduleType = line.split("=")[1].strip().split(" ")[0].strip()
                    if ("LIBRARY_CLASS" in line):
                        self.isLibrary = True
                    line = inf.readline()
            if (not self.isLibrary):
                self.parseLibraries(infFile, "This component INF")
        except IOError as e:
            logging.critical("Unable to open file %s" % infFile)

    def parseLibraries(self, infFile, source):
        newLibInfs = []
        with open(infFile) as inf:
            line = inf.readline()
            while(line != ""):
                if ("[LibraryClasses]" in line):
                    line = inf.readline()
                    while (line != "" and "[" not in line):
                        libname = line.strip().split(" ")[0]
                        if (libname == "" or libname[0] == "#"):
                            line = inf.readline()
                            continue
                        if "LibraryClasses" not in self._options:
                            self.Update("LibraryClasses", DscComponent.OptionTypes["LibraryClasses"](self.parser), self.parser.GetSource())
                        if (not self.GetRaw("LibraryClasses").containsLibrary(libname)):
                            libinf = self.resolveLib(libname)
                            self.GetRaw("LibraryClasses").addLibrary(libname, libinf, source)
                            newLibInfs.append(libinf)
                        line = inf.readline()
                    break
                line = inf.readline()
        #recursively process any newly added library instances for more library dependencies.
        for libinf in newLibInfs:
            self.parseLibraries(self.parser.resolvePath(libinf), "Implied by lib instance: " + libinf)

    def Parse(self):
        #Grab the component path
        (eof, line) = self.parser.nextLine()
        if (eof):
            return False
        
        self.componentPath = line
        
        #if "{" exists, we need extended parsing.
        if (line[-1] == "{"):
            self.componentPath = line[:-1].strip() #remove the { from the component name
            while(True):
                (eof, line) = self.parser.nextLine()
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
                        self.Update(option, DscComponent.OptionTypes[option](self.parser), self.parser.GetSource())
                    #Pcds are weird. Handle them special.
                    elif (option[0:4] in DscComponent.OptionTypes):
                        self.Update(option, DscComponent.OptionTypes[option[0:4]](self.parser, option[4:]), self.parser.GetSource())
                    else:
                        #unrecognized section or line
                        raise Exception("Unrecognized section or line in DSC Component: %s" % line)
                
                #If we get here, we have a parser for this option. Switch the end of section marker, then use it!
                self.parser.setSectionChars("<}")
                self.GetRaw(option).Parse()
                self.parser.clearSectionChars()
        return True
        
    def Write(self, stream):
        stream.write("    %s" % self.componentPath)
        if (len(self._options) != 0):
            stream.write(" {\n")
            for k in sorted(self._options):
                self.GetRaw(k).Write(stream)
            stream.write("    }")
        stream.write("\n")

#[Components] section parser. Subsection is e.g. "X64".
class DscComponents(DscSection):
    def __init__(self, dscparser, subsection):
        super().__init__(dscparser)
        self._components = {}
        self.parser = dscparser
        self._default = "_components"
        self.subsection = subsection
        
    def Parse(self):
        while(True):
            component = DscComponent(self.parser, self.subsection)
            if (component.Parse()):
                self.Update(component.componentPath,component,self.parser.GetSource())
            else:
                break
    
    def Write(self, stream):
        stream.write("[Components.%s]\n" % self.subsection)
        prevPkg = ""
        for componentKey in sorted(self._components):
            component = self.GetRaw(componentKey)
            #Group by package (first element of path).
            if (prevPkg != "" and prevPkg != re.split("[\\\/]", component.componentPath)[0]):
                stream.write("\n")
            prevPkg = re.split("[\\|\/]", component.componentPath)[0]
            component.Write(stream)
        stream.write("\n")

#[BuildOptions] section parser.
class DscBuildOptions(DscSection):
    def __init__(self, dscparser):
        super().__init__(dscparser)
        self.buildappend = {}
        self.buildreplace = {}
        self.parser = dscparser
    
    def Parse(self):
        while(True):
            (eof, line) = self.parser.nextLine()
            if (eof):
                break
            
            buildopt = line.split(maxsplit=2)
            if (buildopt[1] == "="):
                if (buildopt[0] in self.buildappend):
                    self.buildappend[buildopt[0]] += " " + buildopt[2]
                else:
                    self.buildappend[buildopt[0]] = buildopt[2]
            else:
                self.buildreplace[buildopt[0]] = buildopt[2]

    def Write(self, stream):
        stream.write("[BuildOptions]\n")
        for k in sorted(self.buildappend):
            stream.write("    %s=%s\n" % (k, self.buildappend[k]))
        for k in sorted(self.buildreplace):
            stream.write("    %s==%s\n" % (k, self.buildreplace[k]))

#Main DSC parser. Deletgates parsing to section parsers.
class Dsc(object):

    SectionTypes = { "Defines"         : DscDefines, 
                     "SkuIds"          : DscSkus,
                     "LibraryClasses"  : DscLibraryClasses,
                     "Pcds"            : DscPcds,
                     "Components"      : DscComponents,
                     "BuildOptions"    : DscBuildOptions}

    def __init__(self, dscfilename, thebuilder):
        self.dscfilename = dscfilename
        self.dscfh = None
        self.dscfp = None
        self.dscline = 0
        self.thebuilder = thebuilder
        self.Sections = {}
        self.eofOnSectionChars = "["
        self.filestack = []
        self.conditionalstack = []

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
        if ("LibraryClasses."+component.subsection+"."+component.moduleType in self.Sections):
            libraryInst = self.Sections["LibraryClasses."+component.subsection+"."+component.moduleType].Get(library)
            if (libraryInst != None):
                return libraryInst

        if ("LibraryClasses."+component.subsection in self.Sections):
            libraryInst = self.Sections["LibraryClasses."+component.subsection].Get(library)
            if (libraryInst != None):
                return libraryInst
        if ("LibraryClasses.common" in self.Sections):
            libraryInst = self.Sections["LibraryClasses.common"].Get(library)
            if (libraryInst != None):
                return libraryInst

        raise Exception("Can't find " + library + "referenced in " + component.componentPath + " in LibraryClasses")
        #return ""

    #check for exceptional variables. There are a few places where resolving a variable in the DSC that's intended for consumption elsewhere causes problems.
    #TODO: there's got to be a better way to deal with this.
    def checkVariableExceptions(varname):
        if ("MICROSOFT_WORKAROUND" in varname):
            return (True, None)
        return (False, None)
    

    def resolveVariable(self, varname):
        value = None
        #Check for special variables
        (requiresException, value) = Dsc.checkVariableExceptions(varname)
        if (requiresException):
            return value
        
        #Convert variable $(FOO) to value of environment var FOO. Consult section defines, then global defines, then pcds, then builder as last resort.
        value = self.currentSection.Get(varname[2:-1])
        if (value == None):
            for section in self.Sections:
                if (section.startswith("Pcds") and value == None):
                    value = self.Sections[section].Get(varname)
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
    def doOp(op, valuestack):
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
                    Dsc.doOp(opstack.pop(), valstack)
                opstack.pop()
                continue

            #handle operators.
            if (token in operators):
                #pop higher-precedence operators off the stack and process them until we find an op of lower or equal precedence.
                while(len(opstack) > 0 and operators[opstack[-1]]>=operators[token]):
                    Dsc.doOp(opstack.pop(), valstack)
                opstack.append(token)
                continue
            
            #if we get here, we have a token we don't really recognize. just assume the token is a string value without quotes.
            valstack.append(token)

        #all tokens have been processed; now just drain the opstack
        while(len(opstack) > 0):
            Dsc.doOp(opstack.pop(), valstack)

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
                logging.info(line)
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
                self.currentSection.Update(macro[0].strip(), macro[1].strip(), self.GetSource())
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
                if (section not in self.Sections):
                    #self.Sections doesn't have this section yet.
                    #Split on the first "." to get the main section and subsections. Handle Pcds special, 'cause they are weird.
                    if (section[0:4] == "Pcds"):
                        elements = (section[0:4], section[4:])
                    else:
                        elements = section.split(".", 1)
                    if (elements[0] in Dsc.SectionTypes):
                        #Recognizable section - create an entry in self.Sections for it.
                        if (len(elements) > 1):
                            #has subsections
                            self.Sections[section] = Dsc.SectionTypes[elements[0]](self, elements[1])
                        else:
                            self.Sections[section] = Dsc.SectionTypes[elements[0]](self)
                    else:
                        #unrecognized section or line
                        raise Exception("Unrecognized section or line in DSC: %s" % line)
                
                #If we get here, we have a parser for this section. Use it!
                self.currentSection = self.Sections[section]
                self.currentSection.Parse()
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

        for componentSection in self.Sections:
            if componentSection.startswith("Component"):
                for componentKey in self.Sections[componentSection]._components:
                    component = self.Sections[componentSection].GetRaw(componentKey)
                    component.parseComponentFile()

        return status

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

    def sortSectionKeys(sections):
        sectionList = sorted(sections) #sort alphabetically first
        sectionList = sorted(sectionList, key=Dsc.subsectionOrder) #sort subsections
        sectionList = sorted(sectionList, key=Dsc.sectionOrder) #sort sections
        return sectionList

    def Write(self, stream):
        for section in Dsc.sortSectionKeys(self.Sections):
            self.Sections[section].Write(stream)

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
