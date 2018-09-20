##
# Generates the DSC based on a particular JSON file
#TODO move into DSCObject?
##
import logging
import os, sys
import json
from DscObject import Dsc

class JsonToDSCGenerator:
    def __init__(self, jsonFile):
        logging.critical("Loading the JSON file %s", jsonFile)
        #jsonData = None
        with open(jsonFile, 'r') as f:
            lines = f.readlines()
            out = ""
            for a in lines:
                a = a.partition("//")[0]
                a = a.rstrip()
                out += a
            jsonData = json.loads(out)

        logging.critical(jsonData)
        self._dsc = Dsc()
        
        #turn the JSON data into the DSC
        for key in jsonData:
            matchkey = key.lower().strip()
            if matchkey == "defines":
                for defineKey in jsonData[key]:
                    value = jsonData[key][defineKey]
                    self._dsc.UpdateOrCreateValue("Defines",defineKey,value,jsonFile)
        
        # walk the directory looking for infs
        infDir = os.path.dirname(jsonFile)
        logging.critical("Walking %s for inf Files" % infDir)
        for Root, Dirs, Files in os.walk(infDir):
            for File in Files:
                if File.lower().endswith('.inf'):
                    #TODO read inf
                    logging.info("Found inf: %s" % File)

        

    def write(self,outputFile):
        ## writes the output file
        logging.critical("Generating the file")
        with open(outputFile, 'w') as f:  
            #TODO: generate hash code of MD5's so we can determine if we need to rewrite this? But then we already generated it?
            #TODO: how do we invalidate the previous temp.dsc?
            self._dsc.Write(f)