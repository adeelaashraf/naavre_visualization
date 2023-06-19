import tifffile as tiff
from PIL import Image
import rasterio
from rasterio.warp import calculate_default_transform, reproject
import numpy

def tif_to_png(tif_path, png_path):
    try:
        # Read the TIFF file using tifffile
        tif_data = tiff.imread(tif_path)

        # Convert the floating-point image to a suitable mode (e.g., uint8)
        tif_data = (tif_data * 255).astype('uint8')

        # Create an Image object using the TIFF data
        im = Image.fromarray(tif_data)

        # Save as PNG
        im.save(png_path, "PNG")
        print(f"Successfully converted {tif_path} to {png_path}")
    except Exception as e:
        print(f"Failed to convert {tif_path} to {png_path}. Error: {e}")

# Specify the paths to the input .tif file and output .png file
tif_file = "geotiffs/geotiff_TILE_000_BAND_perc_95_normalized_height.tif"
png_file = "pngs/geotiff_TILE_000_BAND_perc_95_normalized_height.png"

# Convert .tif to .png
tif_to_png(tif_file, png_file)

    
# Open the TIFF file using rasterio
with rasterio.open(tif_file) as src:
    target_crs = src.crs
    # Read the data and get the metadata
    tif_data = src.read(1)
    transform, width, height = calculate_default_transform(src.crs, target_crs, src.width, src.height, *src.bounds)

    # Reproject the image to the target CRS
    reprojected_data = numpy.empty((height, width), dtype=tif_data.dtype)
    reproject(source=tif_data, destination=reprojected_data, src_transform=src.transform, src_crs=src.crs,
              dst_transform=transform, dst_crs=target_crs)

# Convert the reprojected image to a suitable mode (e.g., uint8)
reprojected_data = (reprojected_data * 255).astype('uint8')
