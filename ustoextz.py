#!/usr/bin/python

# ustoextz 
# Convert user scripts from userscripts.org into Safari extesions

import sys
import logging
import urllib2
import re
from xml.dom.minidom import Document

# Set logging level
logging.basicConfig(level=logging.DEBUG)

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
desc = extract("@description")
white_list = extract_list("@include")

# DEBUG FOR NOW
logging.debug(name)
logging.debug(desc)
logging.debug(white_list)

# Create a bundle identifer from the script name
bundle = "org.userscripts.%s" % script_id

# Create the filename
filename = "script_%s.js" % script_id

logging.debug(bundle)

# First, some helpers to make this suck a little less
def node(tag, value):
    element = info.createElement(tag)
    text = info.createTextNode(value)
    element.appendChild(text)
    return element

# Let's start 
doctype = '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">'

info = Document()

plist = info.createElement("plist")
plist.setAttribute("version", "1.0")

d = info.createElement("dict")

# Add the name of the script
d.appendChild(node("key", "CFBundleDisplayName"))
d.appendChild(node("string", name))

# Add the author of the script
d.appendChild(node("key", "Author"))
d.appendChild(node("string", "ustoextz Python Script"))

# Add the desciption of the script
d.appendChild(node("key", "Description"))
d.appendChild(node("string", desc))

# Add the website of the script
d.appendChild(node("key", "Website"))
d.appendChild(node("string", script_url))

# This is a default value the extension needs
d.appendChild(node("key", "CFBundleInfoDictionaryVersion"))
d.appendChild(node("string", "6.0"))
d.appendChild(node("key", "ExtensionInfoDictionaryVersion"))
d.appendChild(node("string", "1.0"))

# Add the script version
d.appendChild(node("key", "CFBundleShortVersionString"))
d.appendChild(node("string", "1.0"))
d.appendChild(node("key", "CFBundleVersion"))
d.appendChild(node("string", "1"))

# I really don't know what this setting does
d.appendChild(node("key", "Chrome"))
d.appendChild(info.createElement("dict"))

# Create the permissions dictionary
l = info.createElement('dict')
l.appendChild(node("key", "Level"))
l.appendChild(node("string", "All"))

p = info.createElement('dict')
p.appendChild(node("key", "Website Access"))
p.appendChild(l)

d.appendChild(node("key", "Permissions"))
d.appendChild(p)

# Create the Content node
d.appendChild(node("key", "Content"))
content_dict = info.createElement("dict")

# Create the scripts section
scripts_array = info.createElement("array")
scripts_array.appendChild(node("string", filename))

scripts_dict = info.createElement("dict")
scripts_dict.appendChild(node("key", "End"))
scripts_dict.appendChild(scripts_array)

content_dict.appendChild(node("key", "Scripts"))
content_dict.appendChild(scripts_dict)

# Create the whitelist section
white_array = info.createElement("array")

for w in white_list:
    white_array.appendChild(node("string", w))

content_dict.appendChild(node("key", "Whitelist"))
content_dict.appendChild(white_array)

d.appendChild(content_dict)

# Append the final nodes to the document
plist.appendChild(d)
info.appendChild(plist)

# Thank god, the XML is over
print info.toxml()




