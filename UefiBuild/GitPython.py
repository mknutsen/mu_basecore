# this attemps to replicate some of the interface of gitpython
import os
import logging
import subprocess
from UtilityFunctions import RunCmd

class GitCommand(object):


class Repo(Object):

    def __init__(self,path=None, gitCommand=GitCommand(),bare=False):
        self._path = path
        self.active_branch = None
        self.bare = bare
        self.head = None
        self._update_from_git()
        

    @classmethod
    class init(path=None,mkdir=True,odbt=GitCommand(), **kwargs):
        newRepo = Repo(path)

        return newRepo

    # Updates the .git file
    def _update_from_git(self):

    @classmethod
    def clone_from(url, to_path, progress=None, env=None, **kwargs):
        tempdir = os.path.join(ws,TEMP_MODULE_DIR)
        if not os.path.isdir(tempdir):
            os.mkdir(tempdir)
        dest = os.path.join(tempdir,module)
        
        #make sure we get the commit if 
        # use run command from utilities
        cmd = "git clone --depth 1 --shallow-submodules --recurse-submodules -b %s %s %s " % (branch, url, dest)
        logging.info("Cloning into %s" % dest)
        p = subprocess.Popen(cmd, shell=True)
        p.wait()
        return dest
