from webdav3.client import Client
from configparser import ConfigParser

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

# Download the file from the remote server
local_file_path = './geotiffs/'
client.download(remote_path=remote_file_path, local_path=local_file_path)