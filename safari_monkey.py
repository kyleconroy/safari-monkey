#!/usr/bin/python

# ustoextz 
# Convert user scripts from userscripts.org into Safari extesions

import sys
import logging
import urllib2
import re
import plistlib
import os

# Set logging level
# logging.basicConfig(level=logging.DEBUG)

# Check for the correct number of command line arguments
if len(sys.argv) is not 2:
    print("Usage: ustoextz http://userscripts.org/scripts/show/NNNNN")
    sys.exit(1)

# Get the user script url
url = sys.argv[1]

# Find the user script id and generate the source url
match = re.search("\d+", url)

if not match:
    logging.error("Unable to extract script id from provided url %s" % url)
    sys.exit(1)

script_id = match.group(0)

# Create a bundle identifer from the script name
bundle = "org.userscripts.script%s" % script_id

# Create the filename
filename = "script%s.js" % script_id

# Create the directory name
directory = "script%s.safariextension" % script_id

# Create the script url
script_url = "http://userscripts.org/scripts/source/%s.user.js" % script_id

# Pull the script from userscripts.org
try:
    script = urllib2.urlopen(script_url)
    script = script.read()
except:
    logging.error("Unable to open url: %s" % script_url)
    sys.exit(1)

# Find and return user script parameters
def extract(param, required=True):
    match = re.search("%s (.*)" % param, script)
    
    if not match and required:
        logging.error("Could not find %s in script source" % param)
        sys.exit(1)

    return match.group(1).strip()

# Find and return user script parameters which
# allow for multiple values
def extract_list(param, required=True):
    matches = re.findall("%s (.*)" % param, script)

    if not matches and required:
        logging.error("Could not find %s in script source" % param)
        sys.exit(1)
    
    return map(lambda x: x.strip(), matches)

# Extract name, description of extension
name = extract("@name")
desc = extract("@description")[:99]
white_list = extract_list("@include")

# DEBUG FOR NOW
logging.debug(name)
logging.debug(desc)
logging.debug(white_list)


logging.debug(bundle)

# Create the plist dictionary
pl = {
    "CFBundleDisplayName": name,
    "CFBundleIdentifier": bundle,
    "Author": "ustoextz Python Script",
    "Description": desc,
    "Website": script_url,
    "CFBundleInfoDictionaryVersion": "6.0",
    "ExtensionInfoDictionaryVersion": "1.0",
    "CFBundleShortVersionString": "1.0",
    "CFBundleVersion": "1",
    "Chrome": {},
    "Permissions": {
        "Website Access": { "Level": "All" },
        },
    "Content": {
        "Scripts": { "End": [filename] },
        "Whitelist": white_list,
        },
    }

# Get paths
path = os.path.abspath(os.path.dirname(__file__))
directory = os.path.join(path, directory)
infodest = os.path.join(directory, "Info.plist")
filedest = os.path.join(directory, filename)


# Create the extension directory
try:
    os.mkdir(directory)
except:
    logging.info("Cannot make the extension directory, assuming it exists")

# Create the info plist
plistlib.writePlist(pl, infodest)

# Create the user script
f = open(filedest, 'w')
f.write(script)
f.close()





