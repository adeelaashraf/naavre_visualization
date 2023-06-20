from webdav3.client import Client
from configparser import ConfigParser
import glob
import os
import json
import rasterio


## 1. Retrieve files
# Read the configuration file
config = ConfigParser()
config.read('config_webdav.ini')

# Retrieve credential options and remote file path from the configuration file
webdav_hostname = config.get('WebDAV', 'webdav_hostname')
webdav_login = config.get('WebDAV', 'webdav_login')
webdav_password = config.get('WebDAV', 'webdav_password')


# Create a client instance
options = {
    'webdav_hostname': webdav_hostname,
    'webdav_login': webdav_login,
    'webdav_password': webdav_password
}
client = Client(options)

# List the contents of the home directory
files = client.list("/")
for file in files:
    print(file["path"])
