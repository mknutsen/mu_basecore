# Project MU's Self Describing Build Enviornment

## &#x1F539; Copyright
Copyright (c) 2017, Microsoft Corporation

All rights reserved. Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

## About

This document will walkthrough the layout of a "typical" project Mu repo.
Previously, the paths to critical files and build tools have been hard-coded into the primary build scripts (such as [PlatformBuild.py`](#platformbuildpy) If code was to be added or moved, all build scripts for all projects had to be updated to find the new code and consume it. Furthermore, the old build system required that all binaries, executables, artifacts, and other miscellaneous files be carried in the source tree somewhere. Since moving to Git, this cost has become increasingly burdensome to the point where some of the larger repos are almost unwieldly. 

The new Self Describing Environment system, along with the new Plugin behavior, aims to remedy some of these problems, while preserving flexibility and agility for further project growth. 

## Components of the SDE (Self-Describing Environment) 

The Self-Describing Environment is assembled by a combination of scripts and descriptor files. The scripts locate the descriptor files and configure the environment in a number of different ways (eg. PATH, PYTHONPATH, Shell Variables, Build Variables, external dependencies, etc.). Currently, there are two kinds of descriptor files that can be found in the Core UEFI tree: Path Environment descriptors (path_env) and External Dependency descriptors (ext_dep). Both of these files are simple JSON files containing fields that are used to configure the SDE. They have some overlapping features, but are used for very different purposes. 

### path_env Descriptors

The path_env descriptor is used, primarily, to update the path. This way the build system can locate required tools and scripts. It can also update build vars that can be referenced from the primary build script [PlatformBuild.py](#platformbuildpy) to locate things like binary artifacts that will be included in certain build steps (eg. OPROM binaries). 

The path_env descriptor works by taking the path containing the descriptor and applying it to the environment as specified by the fields of the descriptor. For example, the file `MU_BASECORE/BaseTools/BinWrappers/PosixLike/posix_path_env.json` contains:
```
{
  "scope": "global-nix",
  "flags": ["set_path"]
}
```
which adds `MU_BASECORE/BaseTools/BinWrappers/PosixLike/posix_path_env.json` to the environment path. path_env descriptors are located by the environment configuration scripts by searching the Workspace for files ending in "*_path_env.json". It does not matter what the first part of the file is called, so long as the end is correct. By convention, the first part of the file name should be descriptive enough to differentiate a given descriptor from another descriptor, should it show up in a "find in files" list or something. 

#### The following path_env fields are required: 

##### scope

Identifies which build environments this descriptor contributes to, and what level of precedence it should take within that environment. 

##### flags

We'll see that flags are common to both path_env and ext_dep descriptors, but they are required for path_env (and only optional for ext_dep). This is because it doesn’t make any sense to create a path_env descriptor without specifying what part of the environment should be updated. 

Currently supported flags are: 

- set_shell_var - Sets a shell var (a var that exists in the command-line environment via "set" or "os.environ" or "env") 
- set_build_var - Sets a build var (a var that exists internally to the build system that is retrieved with with env.GetValue()) 
- set_path - Inserts this path to the front of PATH. 
- set_pypath - Inserts this path to the front of PYTHONPATH. Also adds it to sys.path. 
- append_build_var - (In Testing) Either creates a new build var or appends this value to the end of an existing build var. 

#### The following path_env fields are optional or conditional: 

##### var_name

If either the "set_shell_var" or "set_build_var" are in the flags, this field will be required. It defines the name of the var being set. 

##### id

Part of the Override System, this field defines the name that this file will be referred to as by any override_id fields. 

##### override_id

This file will override any descriptor files found in lower lexical order or scope order. Files are traversed in directory order (depth first) and then scope order (highest to lowest). Overrides are only applied forward in the traversal, not backwards. 

### ext_dep Descriptors

ext_dep Descriptors (or External Dependency Descriptors) are used to identify tools or data that are required for building or interacting with the UEFI, but aren't included in any of the source repos. This might include executable utilities, binary artifacts, documentation (eg. CHM files), pre-built drivers, and other files that are too cumbersome or don't make sense to keep within the Git source repo. 

ext_dep descriptors behave a lot like path_env descriptors with one big difference: they will attempt to download, copy, or otherwise import whatever data the descriptor identifies. Currently, Nuget is the only supported data syndication service, but others may follow, including: HTTP, FTP, Network Share, others. When processed as part of an 'update' or 'setup' routine, the ext_dep descriptor will direct the SDE to check for whether the dependency has been downloaded already and whether it's the correct version. If not, the SDE will attempt to download the version of the dependency indicated in the descriptor from the source indicated in the descriptor. 

ext_dep descriptors have the same fields as path_env; the only difference is that flags is optional in the ext_dep descriptor. They are also located in the workspace using the same logic (ie. any files that end in "*_ext_dep.json" will be included, presuming they fall within the current scope. 

Additionally, ext_dep descriptors have the following required fields: 

    type - This indicates which engine should be used to process the dependency files. Currently, on "nuget" is supported. 

    name - This is the name that will be used when looking up the package in the syndication service. It is also the name of the directory that will contain the files, once downloaded. 

    source - This is the path within the syndication service. For nuget, this path will be the URL of the nuget feed. 

    version - This is the version of the dependency. These versions are searched as strings and are exact. If the requested version is not found, an error will be produced in the update process. 

## Build Scripts

This section describes most of the relevant script and module files for driving the Self Describing Environment and the common Core UEFI Build System. It also includes brief descriptions of some platform components to delineate the differences between the old system and the new. 

### `PlatformBuild.py`

[PlatformBuild.py](#platformbuildpy) serves as the primary entry point to the build process for a given platform and is largely used as the configuration hub for the build. It's the location where a platform defines: 

- Its Workspace (root of the codebase). 
- The top-level Git submodules consumed by this platform (enabling a minimum checkout for individual builds). 
- The SDE scopes utilized, and their hierarchical ordering. 
- The UEFI Module Packages to search for drivers, libraries, and other UEFI code. 

This file is still the entry point to the build process, but rather than dispatching the worker directly, it calls into [CommonBuildEntry.p`](#commonbuildentrypy) to maximize code reuse. 

The purpose of this bifurcation is twofold:
1) it is required by the bootstrapping process to ensure that namespaces are loaded in a logical order without making assumptions about what is or is not available and without causing potential runtime errors with circular definitions, and to a lesser extent
2) provides the separation of configuration from business logic, since configuration is the most likely thing needing customization between platforms. 

Command line arguments can be used here to set environment variables that are used during the build process. A couple helpful ones are:
- `BLD_*_BUILD_ALL_UNIT_TESTS`
    - Builds all unit tests listed in the `unit_test.partial.dsc`
- `BUILD_REPORTING=TRUE BUILD_REPORTING_TYPE="PCD"`
    - Creates a detailed build report indicating which modules were built and what PCD settings were used at compilation time
- `TOOL_CHAIN_TAG=GCC5`
    - Set the tool chain tag
- `--clean`
    - Deletes the Build and Conf folder before building
- `--skipbuild`
    - Skips build process and just runs postbuild
- `--setup`
    - Runs first time setup
- `--update`
    - Sets up submodules back to what was configured in git. 

### `PlatformBuildWorker.py`

With little exception, [PlatformBuildWorker.py](#platformbuildworkerpy) contains the platform-specific business logic for a given build and contains all of the hooks or overrides that are unique to a given build. 

### `CommonBuildEntry.py`

This file is a common calling interface from [PlatformBuild.py](#platformbuildpy) to [PlatformBuildWorker.py](#platformbuildworkerpy) and ensures that there is a consistent way to initialize the SDE with each build and to provide common code for "Setup", "Update", and "Build" command line arguments. It also provides shared code for about half of what used to be duplicated in the [PlatformBuild.py](#platformbuildpy) startup/main routine. 

### `UefiBuild.py`

This is the common object for the actual build process, and contains hooks to add platform-specific functionality while maintaining a consistent configuration. This will end up calling the TianoCore/EDK2 build commands that you may be used to.

### `EnvironmentDescriptorFiles.py`

This module contains business logic and validation code for dealing with the descriptor files as JSON objects. It contains code (and error checking) for loading the files, reading their contents into a standard internal representation, and running a limited set of sanitization and validation functions to identify any mistakes as early as possible and provide as much information as possible. 

For convenience, this module also contains the class code for PathEnv descriptor objects, but that's because the class code is so small felt silly to create another file. 

### `ExternalDependencies.py`

This module contains code for managing external dependencies. ExternalDependency objects are created with the data from ext_dep descriptors and are subclassed according to the "type" field in the descriptor. Currently, the only valid subclass is "nuget". 

These objects contain the code for fetching, validating, updating, and cleaning dependency objects and metadata. When referenced from the SDE itself, they can also update paths and other build/shell vars in the build environment. 

### `SelfDescribingEnvironment.py`

This is the proverbial "heart of the beast". It contains most of the business logic for locating, compiling, sorting, filtering, and assembling the SDE files and the environment itself. There are class methods and helper functions to do things like: 

- Locate all the relevant files in the workspace. 
- Sort the files lexically and by scope. 
- Filter the files based on overrides. 
- Assemble the environment (eg. PATH, PYTHONPATH, vars, etc.). 
- Validate all dependencies. 
- Update all dependencies. 

Many of these routines will leverage logic specific to individual sub-modules (Python, not Git), but the collective logic is located here. 

### `ShellEnvironment.py`

This module publishes singletons for managing the "environment" (as it's traditionally conceived). The primary interface "ShellEnvironment" facilitates setting PATH, PYPATH, Build Vars, and Shell Vars. The secondary interface replicates the legacy Build Vars interface, but does so as a singleton. 

### `ConfMgmt.py`

Populates the /Conf folder automatically if the folder is empty.

By default, populates from `MU_BASECORE\BaseTools\Conf\*.template.ms`

To change Conf directory, add `CONF_TEMPLATE_DIR` in [PlatformBuildWorker.py](#platformbuildworkerpy) 

## Working with the SDE (Common Behaviors)

### Understanding Scope 

A critical concept in the SDE system is that of "scope". Each project can define its own scope, and scope is integral to the distributed and shared nature of the SDE. Project scopes are linearly hierarchical and can have an arbitrary number of entries. Only descriptors matching one or more of the scope entries will be included in the SDE during initialization. Furthermore, higher scopes will take precedence when setting paths and assigning values to vars. An example project scope might be: 

("my_platform", "tablet_family", "silicon_reference") 

In this example, "my_platform" is the highest priority in the scope. Any descriptor files found in the entire workspace that have this scope will not only be included in the SDE, they will take precedence over any of the lesser scopes. "tablet_family" and "silicon_reference" scopes will also be used, in that order. Additionally, all projects inherit the "global" scope, but it takes the lowest precedence. 

### Understanding Overrides 

If the ordering provided by the scoping system isn't flexible enough, there is an explicit override system that can be used if necessary. Any descriptors with the "id" field set may be explicitly overridden by a descriptor with a matching "override_id". In this case, rather than overriding any noticeable effect (eg. a path from a higher scope will appear in PATH before an path from a lower scope, or a var with a higher scope will be set on top of a var with a lower scope), the descriptor with the "override_id" field set will force the corresponding descriptor not to be loaded at all. 

Not that when processing these overrides, scope order and lexical file order are still honored. An override is not applied retroactively so, for example, a descriptor from the "global" scope will not be able to override one from a platform scope. This is intentional. 

### Setting Up 

The SDE includes modifications to the [PlatformBuild.py](#platformbuildpy) script that make it easier to start working with any platform. Since the SDE knows how to fetch its own dependencies, and since all these dependencies are described by the platform itself, the build scripts can now perform the minimal steps to enable building any given platform, including: 

- Synchronizing all required submodules. 
- Downloading all source (and only the source actually used by the platform). 
- Configuring all paths. 
- Downloading all binaries. 

To leverage this setup behavior, simply run the [PlatformBuild.py](#platformbuildpy) script corresponding to the platform you want to build with the "--SETUP" argument. This argument will cause the platform to configure itself, and display any errors encountered. 

    NOTE:
    --SETUP should only be required once per build machine, per platform being built. It is not necessary to run it regularly. Only when setting up a new personal workstation or starting to work with a platform that you haven't used yet. 
    The --SETUP feature does not actually build the platform. A normal [PlatformBuild.py](#platformbuildpy) must still be performed. 
    The --SETUP feature will NOT change branches in any submodule that already exists locally, or that has local changes. This is to prevent accidental loss of work. If you would like the script to try making changes even in these cases, use the "--FORCE" argument. 
    The --SETUP feature does not yet install dev singing certs. Those steps must still be performed manually. 


### Building 

Building still works as it always has and all prior arguments can still be passed to the [PlatformBuild.py](#platformbuildpy) script. The only special arguments are "--SETUP" and "--UPDATE" (described below), which will trigger new behaviors. Note that the current state of the SDE is always printed in the DEBUG level of the build log. 


### Updating Dependencies 

Prior to any build, the SDE will attempt to validate the external dependencies that currently exist on the local machine against the versions that are specified in the code. If the code is updated (perhaps by a pull request to the branch you're working on), it is possible that the dependencies will have to be refreshed. If this is the case, you will see a message prompting you to do so when you run [PlatformBuild.py](#platformbuildpy) to build your platform. To perform this update, simply run the [PlatformBuild.py](#platformbuildpy) script with the --UPDATE argument. Any dependencies that match their current versions will be skipped and only out-of-date dependencies will be refreshed. 

### Adding Paths 

### Adding Dependencies 

## Build System - Plugins 

To support a core build system that allows extensibility a plugin system has been incorporated.    The idea is by using plugins the core build system can be shared with external parties and functionality specific to any business unit or partner can be hidden.  Any platform that needs that functionality would also have the build plugin that provides it.  This plugin system currently allows two different types of plugins to be authored which allows for two distinct design paradigms. 

#### IUefiBuildPlugin 

These plugins can provide pre and post build steps.  It is expected numerous plugins of these type would be loaded and then their pre and post build functions would be called during execution of those steps.  The idea here is to allow for custom, self-contained build functionality to be added without required uefi build changes or inline code modifications.  A couple of easy examples are: 

##### Flatten PDB

For MsCoreUefi builds we simplify the PDB path and assume all pdbs are in a single directory.  So a post build plugin walks the code tree, locates the PDBs, and then copies to single directory for use with debugger.  I don't expect every UEFI system out there to want this behavior so this is a perfect example of functionality that can be added without direct changes.  

##### FD usage report

Previously this required in-line changes to uefi build but with plugins now it can be added to the post build step and a report can be generated.   All this can be done without changing UEFI build.   

#### IUefiHelperPlugin 

These plugins allow for registering helper routines.  These helper routines provide critical functionality for a platform build process but are not needed to be directly imported by uefi build.  By having individual function registration routines and plugins (python files) can be split up and shared across product lines, silicon, business units, etc all while being transparently imported into the build environment and available to a product build.  This really is less about plugin design and more about keeping the uefi build and platform builder python files minimal and getting the desired code reuse.   

### Writing a Plugin 

See UDK `UefiBuild\PluginManager.py` for the interface definition and required functions for each type of plugin.    

For IUefiBuildPlugin type the plugin will simply be called during the pre and post build steps after the platform builder object runs its step.  The UefiBuilder object will be passed during the call and therefore the environment dictionary is available within the plugin.   These plugins should be authored to be independent and the platform build or uefi build should not have any dependency on the plugin.  The plugin can depend on variables within the environment dictionary but should be otherwise independent / isolated code.   

For IUefiHelperPlugin type the plugin will simply register functions with the helper object so that other parts of the platform build can use the functions.  It is acceptable for platform build to know/need the helper functions but it is not acceptable for UEFI build super class to depend upon it.  I expect most of these plugins will be at a layer lower than the UDK as this is really to isolate business unit logic while still allowing code reuse.   Look at the HelperFunctions object to see how a plugin registers its functions.   

### Using Plugins 

Using plugins should be easy but it depends on what type of plugin.  For the IUefiBuildPlugin type (pre/post build) there is nothing the UEFI build must do besides make sure the plugin is in your workspace and scoped to an active scope.  For Helper plugins basically the uefi builder Helper member will contain the registered functions as methods on the object.  Therefore calling any function is as simple of using self.Helper.<your func name here>.  It is by design that the parameters and calling contract is not defined.  It is expected that the caller and plugin know about each other and are really just using the plugin system to make inclusion and code sharing easy.   