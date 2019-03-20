import yapsy.UefiBuildPluginTypes as UefiBuildPluginTypes
import logging
import shutil
import os

class FlattenPdbs(UefiBuildPluginTypes.IUefiBuildPlugin):

    def do_post_build(self, thebuilder):
        #Path to Build output
        BuildPath = thebuilder.env.GetValue("BUILD_OUTPUT_BASE")
        #Path to where the PDBs will be stored
        PDBpath = os.path.join(BuildPath, "PDB")

        IgnorePdbs = ['vc1']  #make lower case

        try:
            if not os.path.isdir(PDBpath):
                os.mkdir(PDBpath)
        except:
            logging.critical("Error making PDB directory")

        logging.critical("Copying PDBs to flat directory")
        for dirpath, dirnames, filenames in os.walk(BuildPath):
            if PDBpath in dirpath:
                continue
            for filename in filenames:
                fnl = filename.strip().lower()
                if(fnl.endswith(".pdb")):
                    if(any(e for e in IgnorePdbs if e in fnl)):
                        # too much info. logging.debug("Flatten PDB - Ignore Pdb: %s" % filename)
                        pass
                    else:
                        shutil.copy(os.path.join(dirpath, filename), os.path.join(PDBpath, filename))
        return 0