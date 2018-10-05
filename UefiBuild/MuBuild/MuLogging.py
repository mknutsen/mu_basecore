import logging
import sys
from datetime import datetime
from datetime import date
import os
import shutil

def clean_build_logs(ws):
     # Make sure that we have a clean environment.
    if os.path.isdir(os.path.join(ws, "Build", "BuildLogs")):
        shutil.rmtree(os.path.join(ws, "Build", "BuildLogs"))

def setup_logging(workspace, filename=None, loghandle = None):

    if loghandle is not None:
        stop_logging(loghandle)

    
    if filename is None:
        filename = "BUILDLOG_MASTER.txt"
    
    #setup logger
    logger = logging.getLogger('')
    logger.setLevel(logging.DEBUG)

    if len(logger.handlers) == 0:
        #Create the main console as logger
        formatter = logging.Formatter("%(levelname)s- %(message)s")
        console = logging.StreamHandler()
        console.setLevel(logging.WARNING)
        console.setFormatter(formatter)
        logger.addHandler(console)

    
    logfile = os.path.join(workspace, "Build", "BuildLogs", filename)
    if(not os.path.isdir(os.path.dirname(logfile))):
        os.makedirs(os.path.dirname(logfile))
    
    #Create master file logger
    fileformatter = logging.Formatter("%(levelname)s - %(message)s")
    filelogger = logging.FileHandler(filename=(logfile), mode='w')
    filelogger.setLevel(logging.DEBUG)
    filelogger.setFormatter(fileformatter)
    logger.addHandler(filelogger)
    logging.info("Log Started: " + datetime.strftime(datetime.now(), "%A, %B %d, %Y %I:%M%p" ))
    logging.info("Running Python version: " + str(sys.version_info))

    return logfile,filelogger

def stop_logging(loghandle):
    loghandle.close()
    logging.getLogger('').removeHandler(loghandle)


class Summary():
    def __init__(self):
        self.errors = list()
        self.warnings = list()
        self.results = list()
        self.layers = 0

    def print_status(self, workspace,loghandle = None):
        logging.critical("\n\n\n************************************************************************************************************************************\n" + \
                            "************************************************************************************************************************************\n" + \
                            "************************************************************************************************************************************\n\n")

        logfile,loghandle = setup_logging(workspace,"BUILDLOG_SUMMARY.txt", loghandle)

        logging.critical("\n_______________________RESULTS_______________________________\n")
        for layer in self.results:
            logging.critical("")
            for result in layer:
                logging.critical(result)

        logging.critical("\n_______________________ERRORS_______________________________\n")
        for layer in self.errors:
            logging.critical("")
            for error in layer:
                logging.critical("ERROR: " + error)

        logging.critical("\n_______________________WARNINGS_____________________________\n")
        for layer in self.warnings:
            logging.critical("")
            for warning in layer:
                logging.critical("WARNING: " + warning)

    def AddError(self, error, layer = 0):
        if len(self.errors) <= layer:
            self.AddLayer(layer)
        self.errors[layer].append(error)

    def AddWarning(self, warning, layer = 0):
        if len(self.warnings) <= layer:
            self.AddLayer(layer)
        self.warnings[layer].append(warning)

    def AddResult(self, result, layer = 0):
        if len(self.results) <= layer:
            self.AddLayer(layer)
        self.results[layer].append(result)

    def AddLayer(self, layer):
        self.layers = layer
        while len(self.results) <= layer:
            self.results.append(list())

        while len(self.errors) <= layer:
            self.errors.append(list())

        while len(self.warnings) <= layer:
            self.warnings.append(list())

    def NumLayers(self):
        return self.layers
