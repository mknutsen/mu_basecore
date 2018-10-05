import logging

class Summary():
    def __init__(self):
        self.errors = list()
        self.warnings = list()
        self.results = list()
        self.layers = 0

    def print_status(self, loghandle = None):
        logging.critical("\n\n\n************************************************************************************************************************************\n" + \
                            "************************************************************************************************************************************\n" + \
                            "************************************************************************************************************************************\n\n")

        logfile,loghandle = setup_logging("BUILDLOG_SUMMARY.txt", loghandle)

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
