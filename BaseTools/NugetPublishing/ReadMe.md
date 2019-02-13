# NugetPublishing

Tool to help create and publish nuget packages for Project Mu resources

## Usage

See NugetPublishing.py -h  

## OPTIONAL: Separation by OS/bit/architecture

Before the path to the NuGet package contents is published, the Python environment can look inside at several subfolders and decide which one to use based on the Host OS, highest order bit available, and the architecture of the processor. To do so, add "separated" to your flags like so:

```
"flags": ["separated"],
```

If this flag is present, the environment will make a list possible subfolders that would be acceptable for the host machine.
For this example, a 64 bit Windows machine with an x86 processor was used:

1. Windows-x86-64
2. Windows-x86
3. Windows-64
4. x86-64
5. Windows
6. x86
7. 64

The environment will look for these folders, following this order, and select the first one it finds. If none are found, the flag will be ignored.

## Authentication

For publishing most service providers require authentication.  The **--ApiKey** parameter allows the caller to supply a unique key for authorization.  There are numerous ways to authenticate. 
For example
* Azure Dev Ops:
  * VSTS credential manager.  In an interactive session a dialog will popup for the user to login
  * Tokens can also be used as the API key.  Go to your account page to generate a token that can push packages
* NuGet.org
  * Must use an API key.  Go to your account page and generate a key.  

## Example: Creating new config file for first use

```yaml
{
    "name": "Name of your package",
    "author_string": "Let users know who to be mad at when it doesn't work",
    "server_url": "https://api.nuget.org/v3/index.json",  # This is just URL of the NuGet server you are using, not the URL of the project itself
    "project_url": "Link to a website that provides more information about the project",
    "license_url": "Link to a license describing the ownership of the contents",
    "description_string": "This is where you describe what your NuGet feed does",
    "copyright_string": "Copyright 2019"
}
```

## Example: Publishing new version of tool

Using an existing config file publish a new iasl.exe.  See the example file **iasl.config.json**
1. Download version from acpica.org
2. Unzip 
3. Make a new folder (for my example I will call it "new")
4. Copy the assets to publish into this new folder (in this case just iasl.exe)
5. Run the iasl.exe -v command to see the version.
6. Open cmd prompt in the NugetPublishing dir
7. Pack and push (here is my example command. )
  ```cmd
  NugetPublishing.py --Operation PackAndPush --ConfigFilePath iasl.config.json --Version 20180209.0.0 --InputFolderPath "C:\temp\iasl-win-20180209\new"  --ApiKey <your key here>
  ```

