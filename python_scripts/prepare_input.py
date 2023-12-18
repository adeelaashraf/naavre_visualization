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

## Save the projection (ESPG) from the first file.
## All files will be repojected using this projection (if varying).
def get_files_with_extensions(directory_path, extensions):
    files = []
    for file_name in os.listdir(directory_path):
        if any(file_name.endswith(extension) for extension in extensions):
            files.append(os.path.join(directory_path, file_name))
    return files

## Convert each .tif to .png + calculate extents

def tif_to_png(tif_file, png_file, target_crs):
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


def prepare_input_for_application(geotiff_files_path, pngs_files_path, json_file_path, json_dict, extensions):
    geotiff_files_list = get_files_with_extensions(geotiff_files_path, extensions)

    print(geotiff_files_list)
    # Open the TIFF file using rasterio
    with rasterio.open(geotiff_files_list[0]) as src:
        target_crs = src.crs
        print(target_crs)
        json_dict["projection"] = int(target_crs.to_epsg())

    png_files_dict = {}

    for tif_file in geotiff_files_list:
        for extension in extensions:
            if tif_file.lower().endswith(extension.lower()):
                png_file = tif_file[:-(len(extension))] + ".png"
                break

        png_file = png_file.replace(geotiff_files_path, pngs_files_path)

        [min_x, min_y, max_x, max_y] = tif_to_png(tif_file, png_file, target_crs)
     
        nested_dict = {
            "file_name": png_file,
            "min_x": min_x,
            "min_y": min_y,
            "max_x": max_x,
            "max_y": max_y
        }
        png_files_dict[tif_file] = nested_dict

    json_dict["png_files"] = png_files_dict

    ## Add the version of the OpenLayers application.
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
