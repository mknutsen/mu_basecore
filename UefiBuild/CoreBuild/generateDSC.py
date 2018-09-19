##
# Generates the DSC based on a particular JSON file
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
        
        for key in jsonData:
            matchkey = key.lower().strip()
            if matchkey == "defines":
                for defineKey in jsonData[key]:
                    value = jsonData[key][defineKey]
                    self._dsc.UpdateOrCreateValue("Defines",defineKey,value,jsonFile)        

    def write(self,outputFile):
        ## writes the output file
        logging.critical("Generating the file")
        with open(outputFile, 'w') as f:  
            self._dsc.Write(f)