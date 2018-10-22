## @file DependencyCheck.py
# Simple Project Mu Build Plugin to support
# checking package dependencies for all INFs
# in a given package.
##
# Copyright (c) 2018, Microsoft Corporation
#
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
##
### 
import logging
from PluginManager import IMuBuildPlugin
import os
import time
import re

from Uefi.EdkII.Parsers.InfParser import *

class CLinterCheck(IMuBuildPlugin):

    @staticmethod
    def LoadFileStripComments(path):
        multiLineComment = False
        singleLineCommentRegex = re.compile(r"//.*")
        multiLineStartCommentRegex = re.compile(r"/\*.*$") # /*
        multiLineEndCommentRegex = re.compile(r".*\*/")  # */
        justWhiteSpaceRegex = re.compile(r"\w*$")
        lineNum = 0
        out = list()
        
        with open(path, 'r') as f:
            #read in the lines
            lines = f.readlines()
            #foreach line
            for a in lines:
                lineNum += 1
                
                
                #Check for multi-line comments
                if multiLineComment is False:
                    if r"/*" in a:
                        a = multiLineStartCommentRegex.sub(" ",a)
                        multiLineComment = True
                else:
                    if r"*/" in a:
                        a = multiLineEndCommentRegex.sub(" ",a)
                        multiLineComment = False
                    else:
                        continue
                #check of single line comments
                if r"//" in a:
                    a = singleLineCommentRegex.sub(" ",a)
                a = a.rstrip()
                # append both the line and the linenumber to our list of code 
                if a is "":
                    continue
                out.append((a,lineNum))
            return out
        
        return None
    
    def CheckCFile(self,source):
        file = CLinterCheck.LoadFileStripComments(source)
        errors = list()
        #check ifs
        for line,lineNum in file:
            if "if" in line and not "{" in line:
                errors.append((source,lineNum,"If and { not same line"))
                #logging.warning("{0}: {1}".format(lineNum,line))
        return errors

    def CheckHFile(self,source):
        return list()

    def GetTestName(self, packagename, environment):
        return ("MuBuild C Linter " + packagename, "MuBuild.CLinter." + packagename)

    #   - package is the edk2 path to package.  This means workspace/packagepath relative.  
    #   - edk2path object configured with workspace and packages path
    #   - any additional command line args
    #   - RepoConfig Object (dict) for the build
    #   - PkgConfig Object (dict) for the pkg
    #   - EnvConfig Object 
    #   - Plugin Manager Instance
    #   - Plugin Helper Obj Instance
    #   - testcase Object used for outputing junit results
    def RunBuildPlugin(self, packagename, Edk2pathObj, args, repoconfig, pkgconfig, environment, PLM, PLMHelper, tc):
        overall_status = 0
        
        #Get current platform
        abs_pkg_path = Edk2pathObj.GetAbsolutePathOnThisSytemFromEdk2RelativePath(packagename)

        #Get INF Files
        INFFiles = self.WalkDirectoryForExtension([".inf"], abs_pkg_path)
        INFFiles = [x.lower() for x in INFFiles]
        INFFiles = [Edk2pathObj.GetEdk2RelativePathFromAbsolutePath(x) for x in INFFiles]  #make edk2relative path so can compare with Ignore List

        # Remove ignored INFs
        if "IgnoreInf" in pkgconfig:
            for a in pkgconfig["IgnoreInf"]:
                a = a.lower().replace(os.sep, "/")
                try:
                    INFFiles.remove(a)
                    tc.LogStdOut("IgnoreInf {0}".format(a))
                except:
                    logging.info("DependencyConfig.IgnoreInf -> {0} not found in filesystem.  Invalid ignore file".format(a))
                    tc.LogStdError("DependencyConfig.IgnoreInf -> {0} not found in filesystem.  Invalid ignore file".format(a))

        sourcesToCheck = list()
        #For each INF file
        for file in INFFiles:
            ip = InfParser()
            ip.SetBaseAbsPath(Edk2pathObj.WorkspacePath).SetPackagePaths(Edk2pathObj.PackagePathList).ParseFile(file)
            
            for s in ip.Sources:
                sourcePath = os.path.join(os.path.dirname(ip.Path),s)
                if not os.path.isfile(sourcePath) :
                    logging.warning("Unknown source file: {0} in {1}. Checked at {2}".format(s,file,sourcePath))
                elif sourcePath not in sourcesToCheck:
                    sourcesToCheck.append(sourcePath)
        
        
        for source in sourcesToCheck:
            if source.endswith(".c"):
                result = self.CheckCFile(source)
            if source.endswith(".h"):
                result = self.CheckHFile(source)
            
            for error in result:
                overall_status += 1
                logging.error(error)

            #figure out how to handle the result
        
        # If XML object exists, add results
        if overall_status is not 0:
            tc.SetFailed("Failed with {0} errors".format(overall_status), "DEPENDENCYCHECK_FAILED")
        else:
            tc.SetSuccess()
        return overall_status
    
    def ValidateConfig(self, config, name):
       return True
