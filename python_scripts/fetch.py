from webdav3.client import Client
from configparser import ConfigParser
import glob
import os
import json
import rasterio


## 1. Retrieve files
# Read the configuration file
config = ConfigParser()
config.read('config.ini')

# Retrieve credential options and remote file path from the configuration file
webdav_hostname = config.get('WebDAV', 'webdav_hostname')
webdav_login = config.get('WebDAV', 'webdav_login')
webdav_password = config.get('WebDAV', 'webdav_password')
remote_file_path = config.get('WebDAV', 'remote_file_path')

# Create a client instance
options = {
    'webdav_hostname': webdav_hostname,
    'webdav_login': webdav_login,
    'webdav_password': webdav_password
}
client = Client(options)

local_file_path = './geotiffs/'
output_file_path = 'data.json'

# Download the file from the remote server
client.download(remote_path=remote_file_path, local_path=local_file_path)

## 2. Calculate extens files
def calculate_extents(directory):
    file_list = glob.glob(directory + '/**/*.tif', recursive=True)
    min_x = float('inf')
    min_y = float('inf')
    max_x = float('-inf')
    max_y = float('-inf')
    
    for file_path in file_list:
        with rasterio.open(file_path) as dataset:
            bounds = dataset.bounds
            min_x = min(min_x, bounds.left)
            min_y = min(min_y, bounds.bottom)
            max_x = max(max_x, bounds.right)
            max_y = max(max_y, bounds.top)

    return min_x, min_y, max_x, max_y

min_x, min_y, max_x, max_y = calculate_extents(local_file_path)
print("Minimum Extents:", min_x, min_y)
print("Maximum Extents:", max_x, max_y)

json_dict = {}
## 3. Save to data.json
json_dict['file_names'] = glob.glob(local_file_path + '/**/*.tif', recursive=True)
json_dict['min_x'] = min_x
json_dict['min_y'] = min_y
json_dict['max_x'] = max_x
json_dict['max_y'] = max_y

with open(output_file_path, 'w') as json_file:
    json.dump(json_dict, json_file)
