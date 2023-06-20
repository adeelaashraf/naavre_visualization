from webdav3.client import Client
from configparser import ConfigParser
import glob
import os
import json
import rasterio
from rasterio import warp
import tifffile as tiff
from PIL import Image
import numpy as np
from dotenv import load_dotenv

## 1. Create necessary directories and file if not existing yet.
def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory '{directory}' created.")
    else:
        print(f"Directory '{directory}' already exists.")

def create_if_not_exists(filename):
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

geotiff_files_path = './geotiffs/'
pngs_files_path = './pngs/'
json_file_path = './data.json'
json_dict = {}

create_directory_if_not_exists(geotiff_files_path)
create_directory_if_not_exists(pngs_files_path)
create_if_not_exists(json_file_path)

## 2. Retrieve files using the input arguments (saved to config.ini)
# Read the configuration file
config = ConfigParser()
config.read('configs/config.ini')

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
client.download(remote_path=remote_file_path, local_path=geotiff_files_path)

## 3. Save the projection (ESPG) from the first file.
## All files will be repojected using this projection (if varying).
geotiff_files_list = glob.glob(geotiff_files_path + '/**/*.tif', recursive=True)
# Open the TIFF file using rasterio
with rasterio.open(geotiff_files_list[0]) as src:
    target_crs = src.crs
    print(target_crs)
    json_dict["projection"] = int(target_crs.to_epsg())

## 4. Convert each .tif to .png + calculate extents

def tif_to_png(tif_file, png_file):
    # Open the input TIFF file
    with rasterio.open(tif_file) as src:
        # Read the source dataset and its metadata
        src_data = src.read(1)
        src_transform = src.transform
        src_crs = src.crs

        # Handle NaN and infinite values
        src_data = np.nan_to_num(src_data, nan=0, posinf=0, neginf=0)

        # Convert data type to UInt16
        src_data = (src_data * 65535).astype(np.uint16)


        # Get the extent of the source dataset
        src_extent = src.bounds

        # Reproject the extent to the target projection
        min_x, min_y, max_x, max_y = warp.transform_bounds(
            src_crs, target_crs, *src_extent
        )

        # Print the extent in the target projection
        print("Extent in target projection:")
        print("min_x:", min_x)
        print("min_y:", min_y)
        print("max_x:", max_x)
        print("max_y:", max_y)

        # Create a new dataset in the target projection and save as PNG
        with rasterio.open(
            png_file,
            "w",
            driver="PNG",
            height=src_data.shape[0],
            width=src_data.shape[1],
            count=1,
            dtype=src_data.dtype,
            crs=target_crs,
            transform=src_transform,
        ) as dst:
            # Write the reprojected data to the output PNG file
            dst.write(src_data, 1)

    return(min_x, min_y, max_x, max_y)

png_files_dict = {}

for tif_file in geotiff_files_list:
    png_file= tif_file.replace(".tif", ".png")
    png_file = png_file.replace(geotiff_files_path, pngs_files_path)

    [min_x, min_y, max_x, max_y] = tif_to_png(tif_file, png_file)
 
    nested_dict = {
        "file_name": png_file,
        "min_x": min_x,
        "min_y": min_y,
        "max_x": max_x,
        "max_y": max_y
    }
    png_files_dict[tif_file] = nested_dict

json_dict["png_files"] = png_files_dict

## 5. Add the version of the OpenLayers application.
# This is done using this script as accessing .env from the browser is not possible.

# Load environment variables from .env file
load_dotenv()
version = os.getenv('APP_VERSION')

version_dict = {
    'version': version,
}

json_dict["version"] = version

## 6. Lastly save all data to data.json
with open(json_file_path, 'w') as json_file:
    json.dump(json_dict, json_file, indent=4)
