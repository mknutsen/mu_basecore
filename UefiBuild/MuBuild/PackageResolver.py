import os
import logging
import subprocess

##
# Walks until it finds a .dependencies and generates a list of packages we need to find
# returns an empty array if it can't find anything
##
def generate_modules_dependencies(module, workspace):

    modules = []
    
    currentDir = module
    if os.path.isfile(currentDir):
        currentDir = os.path.dirname(currentDir)

    # make sure we add the module that we are currently in
    #TODO: use git toplevel instead?
    #WARNING: this uses the assumption that it will be named SM_ something
    findSMRoot = currentDir

    while not os.path.basename(findSMRoot).startswith("SM_"):
        findSMRoot = os.path.dirname(findSMRoot)
        #logging.critical("Scanning for git folder: %s"%os.path.basename(findSMRoot)[0:2])
        if os.path.dirname(findSMRoot) == findSMRoot:
           break
    
    if not os.path.dirname(findSMRoot) == findSMRoot:
        modules.append(findSMRoot)

    while not os.path.isfile(os.path.join(currentDir,".depends")):
        currentDir = os.path.dirname(currentDir)
        #logging.critical("Scanning Dependency file: %s"%currentDir)
        if os.path.dirname(currentDir) == currentDir:
            return modules
    
    #we have our currentDir -> read in the dependencies
    logging.info("Loading Module Dependency file: %s"%currentDir)

    dependencies = read_dependency_file(os.path.join(currentDir,".depends"))

    #find the folder of each module that our dependency file specified
    for module in dependencies:
        path = find_module(workspace,module["name"],module["url"])
        if path is None:
            logging.info("Unable to find: %s. Cloning " % module)
            path = clone_module(workspace,module["name"],module["url"], module["branch"], module["commit"])
        if path is None:
            logging.critical("Unable to find: %s. Cloning failed " % module)
        else:#we found the path
            modules.append(path)
    return modules

##
# reads the .depends files. An example of the file format
#[Common/SM_MU_TIANO_PLUS]
#	url = https://github.com/Microsoft/mu_tiano_plus.git
#    branch = release/20180529
#    commit = 5d4a51b4a8d20e5ff1f75adeb969697b1cc201cb
##
def read_dependency_file(file):
    
    try:
        file = open(file,'r')
        line = file.readline()
        modules = []        
        while not line == "":
            line = line.strip()
            if line[0] == '[':                
                modules.insert(0,{"name":line[1:-1]})
            elif "=" in line:
                defines = line.split("=")
                key = defines[0].strip()
                value = defines[1].strip()
                modules[0][key] = value #insert into the 
            else:
                logging.warn("Malformatted line in dependency file: %s" % line )
            line = file.readline() #read in a new file
        
        return modules
    except IOError as e:
        logging.critical("Unable to open file %s" % infFile)
        return []

##
# finds the module requested from the workspace- we assume that it is here at some point
def find_module(ws,module, url):
    currentDir = ws
    if os.path.isfile(currentDir):
        currentDir = os.path.dirname(currentDir)
    for Root, Dirs, Files in os.walk(ws):
        #don't walk - just look in workspace
        #look for the directory module if we don't find it, we clone it
        for directory in Dirs: 
            #todo read the git information in the directory we find and make sure it matches the URL we find
            if directory == module:
                return os.path.join(Root,directory)
            #logging.info(os.path.join(Root,directory))

    return None

def clone_module(ws,module, url, branch, commit):
    tempdir = os.path.join(ws,TEMP_MODULE_DIR)
    if not os.path.isdir(tempdir):
        os.mkdir(tempdir)
    dest = os.path.join(tempdir,module)
    
    #make sure we get the commit if 
    # use run command
    cmd = "git clone --depth 1 --shallow-submodules --recurse-submodules -b %s %s %s " % (branch, url, dest)
    logging.info("Cloning into %s" % dest)
    p = subprocess.Popen(cmd, shell=True)
    p.wait()
    return dest

