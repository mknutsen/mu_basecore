from Uefi.EdkII.Parsers.BaseParser import HashFileParser
import os


AllPhases = ["SEC", "PEIM", "PEI_CORE", "DXE_DRIVER", "DXE_CORE", "DXE_RUNTIME_DRIVER", "UEFI_DRIVER", "SMM_CORE", "DXE_SMM_DRIVER", "UEFI_APPLICATION"]

class InfParser(HashFileParser):

    def __init__(self):
        HashFileParser.__init__(self, 'ModuleInfParser')
        self.Lines = []
        self.Parsed = False
        self.Dict = {}
        self.LibraryClass = ""
        self.SupportedPhases = []
        self.PackagesUsed = []
        self.LibrariesUsed = []
        self.ProtocolsUsed = []
        self.GuidsUsed = []
        self.PpisUsed = []
        self.PcdsUsed = []
        self.Path = ""

    def ParseFile(self, filepath):
        self.Logger.debug("Parsing file: %s" % filepath)
        if(not os.path.isabs(filepath)):
            fp = self.FindPath(filepath)
        else:
            fp = filepath
        self.Path = fp
        f = open(fp, "r")
        self.Lines = f.readlines()
        f.close()
        InDefinesSection = False
        InPackagesSection = False
        InLibraryClassSection = False
        InProtocolsSection = False
        InGuidsSection = False
        InPpiSection = False
        InPcdSection = False

        for l in self.Lines:
            l = self.StripComment(l)

            if(l == None or len(l) < 1):
                continue

            if InDefinesSection:
                if l.strip()[0] == '[':
                    InDefinesSection = False
                else:
                    if l.count("=") == 1:
                        tokens = l.split('=', 1)
                        self.Dict[tokens[0].strip()] = tokens[1].strip()
                        #
                        # Parse Library class and phases in special manor
                        #
                        if(tokens[0].strip().lower() == "library_class"):
                            self.LibraryClass = tokens[1].partition("|")[0].strip()
                            self.Logger.debug("Library class found")
                            if(len(tokens[1].partition("|")[2].strip()) < 1):
                                self.SupportedPhases = AllPhases
                            elif(tokens[1].partition("|")[2].strip().lower() == "base"):
                                 self.SupportedPhases = AllPhases
                            else:
                                self.SupportedPhases = tokens[1].partition("|")[2].strip().split()

                        self.Logger.debug("Key,values found:  %s = %s"%(tokens[0].strip(), tokens[1].strip()))

                        continue

            elif InPackagesSection:
                if l.strip()[0] == '[':
                   InPackagesSection = False
                else:
                   self.PackagesUsed.append(l.partition("|")[0].strip())
                   continue

            elif InLibraryClassSection:
                if l.strip()[0] == '[':
                   InLibraryClassSection = False
                else:
                   self.LibrariesUsed.append(l.partition("|")[0].strip())
                   continue

            elif InProtocolsSection:
                if l.strip()[0] == '[':
                   InProtocolsSection = False
                else:
                   self.ProtocolsUsed.append(l.partition("|")[0].strip())
                   continue

            elif InGuidsSection:
                if l.strip()[0] == '[':
                   InGuidsSection = False
                else:
                   self.GuidsUsed.append(l.partition("|")[0].strip())
                   continue

            elif InPcdSection:
                if l.strip()[0] == '[':
                   InPcdSection = False
                else:
                   self.PcdsUsed.append(l.partition("|")[0].strip())
                   continue

            elif InPpiSection:
                if l.strip()[0] == '[':
                   InPpiSection = False
                else:
                   self.PpisUsed.append(l.partition("|")[0].strip())
                   continue
            # check for different sections
            if l.strip().lower().startswith('[defines'):
                InDefinesSection = True

            elif l.strip().lower().startswith('[packages'):
                InPackagesSection = True

            elif l.strip().lower().startswith('[libraryclasses'):
                InLibraryClassSection = True

            elif l.strip().lower().startswith('[protocols'):
                InProtocolsSection = True

            elif l.strip().lower().startswith('[ppis'):
                InPpiSection = True

            elif l.strip().lower().startswith('[guids'):
                InGuidsSection = True

            elif l.strip().lower().startswith('[pcd') or l.strip().lower().startswith('[patchpcd') or l.strip().lower().startswith('[fixedpcd') or l.strip().lower().startswith('[featurepcd'):
                InPcdSection = True

        self.Parsed = True