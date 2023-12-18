import argparse
import glob
import json
import numpy as np
import os
import rasterio
from rasterio import warp
import requests
from PIL import Image
import tifffile as tiff
from webdav3.client import Client
from configparser import ConfigParser
from dotenv import load_dotenv

## Create necessary directories and file if not existing yet.
def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory '{directory}' created.")
    else:
        print(f"Directory '{directory}' already exists.")

def create_file_if_not_exists(filename):
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory '{directory}' created.")

    if not os.path.isfile(filename):
        with open(filename, "w") as file:
            file.write("")  # Write an empty string to create the file
        print(f"File '{filename}' created.")
    else:
        print(f"File '{filename}' already exists.")


def download_using_credentials(hostname,username, password, remote_file_path, num_files_str, mode, extensions, geotiff_files_path):
    try:
        if mode == "webdav":
            # For now only support webdav
            options = {
                'webdav_hostname': hostname,
                'webdav_login': username,
                'webdav_password': password
            }
            client = Client(options)

            # Check if NUM_FILES is an integer
            try:
                num_files = int(num_files_str)
            except ValueError:
                print("Error: NUM_FILES must be an integer.")
                exit(1)

            # Retrieve a list of remote files first
            remote_files = client.list(remote_path=remote_file_path)
            print(remote_files)

            # Filter the files in the list based on the specified extensions
            filtered_files = [file for file in remote_files if file.endswith(extensions)]

            # If NUM_FILES is not positive or larger than the list of filtered files, download all filtered files
            if num_files <= 0 or num_files > len(filtered_files):
                num_files = len(filtered_files)

            # Download only the filtered files
            for file in filtered_files[:num_files]:
                client.download(remote_path=os.path.join(remote_file_path, file), local_path=os.path.join(geotiff_files_path, file))
        elif mode == "macaroon":
            # Macaroon = password, remote_file_path = full file path (including hostname) to a single file
            # Multiple files in one directory is not supported for macaroons
            # Save the downloaded file
            macaroon_filename = remote_file_path.split('/')[-1]
            file_path = os.path.join(geotiff_files_path, macaroon_filename)
            headers = {'Authorization': f'Bearer {password}'}

            try:
                response = requests.get(remote_file_path, headers=headers)

                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    with open(file_path, 'wb') as file:
                        file.write(response.content)
                    print(f"File downloaded and saved to: {file_path}")
                else:
                    print(f"Request failed with status code: {response.status_code}")
                    print(response.text)

            except requests.exceptions.RequestException as e:
                print(f"Error occurred during the request: {e}")
    except TypeError:
        print("Mode {mode} is not recognized. Available modes: webdav, macaroon")
        exit(1)
