import argparse
import time
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

import download_files
import prepare_input

def main():
    # Define file paths and data types required
    geotiff_files_path = './geotiffs/'
    pngs_files_path = './pngs/'
    json_file_path = './data.json'
    json_dict = {}
    extensions = (".tif", ".TIF", ".tiff", "TIFF")

    # Create required directories and files if they do not exist
    download_files.create_directory_if_not_exists(geotiff_files_path)
    download_files.create_directory_if_not_exists(pngs_files_path)
    download_files.create_file_if_not_exists(json_file_path)

    # Fetch necessary credentials
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--hostname', action='store', type=str, required=True, dest='hostname')
    arg_parser.add_argument('--username', action='store', type=str, required=True, dest='username')
    arg_parser.add_argument('--password', action='store', type=str, required=True, dest='password')
    arg_parser.add_argument('--remote_file_path', action='store', type=str, required=True, dest='remote_file_path')
    arg_parser.add_argument('--num_files', action='store', type=str, required=True, dest='num_files')
    arg_parser.add_argument('--mode', action='store', type=str, required=True, dest='mode')
    args = arg_parser.parse_args()

    hostname = args.hostname
    username = args.username
    password = args.password
    remote_file_path = args.remote_file_path
    num_files_str = args.num_files
    mode = args.mode

    #Time the execution of download_files function in milliseconds
    start_time_download = time.time()
    download_files.download_using_credentials(hostname, username, password, remote_file_path, num_files_str, mode, extensions, geotiff_files_path)
    end_time_download = time.time()
    elapsed_time_download = (end_time_download - start_time_download) * 1000  # Convert to milliseconds
    print("download_files execution time: {} milliseconds".format(elapsed_time_download))

    # Time the execution of prepare_input function in milliseconds
    start_time_prepare_input = time.time()
    prepare_input.prepare_input_for_application(geotiff_files_path, pngs_files_path, json_file_path, json_dict, extensions)
    end_time_prepare_input = time.time()
    elapsed_time_prepare_input = (end_time_prepare_input - start_time_prepare_input) * 1000  # Convert to milliseconds
    print("prepare_input execution time: {} milliseconds".format(elapsed_time_prepare_input))

if __name__ == "__main__":
    main()

