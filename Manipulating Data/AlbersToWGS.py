import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

# Define the source WKT (your custom Albers projection)
albers_wkt = """
PROJCS["unknown",GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],
AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],
AUTHORITY["EPSG","4326"]],PROJECTION["Albers_Conic_Equal_Area"],PARAMETER["latitude_of_center",23],
PARAMETER["longitude_of_center",-96],PARAMETER["standard_parallel_1",29.5],PARAMETER["standard_parallel_2",45.5],
PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],
AXIS["Easting",EAST],AXIS["Northing",NORTH]]
"""

# Define the target CRS as WGS 84 (EPSG:4326)
targetcrs = 'EPSG:4326'  # WGS 84

# Input and output file paths
input_file = '/home/dibbo-roy/Wild-Fire-Mapping/DataImages/ForestFIreData.tif'  # Replace with your source file path
output_file = '/home/dibbo-roy/Wild-Fire-Mapping/DataImages/ForestFIreDataWGS.tif'  # Output file path for the reprojected file


# Function to reproject a raster to WGS 84
def reproject_to_wgs84(input_path, output_path, source_wkt, target_crs):
    with rasterio.open(input_path) as src:
        # Create source CRS from WKT
        src_crs = rasterio.crs.CRS.from_wkt(source_wkt)

        # Calculate the transform and metadata for the destination raster
        transform, width, height = calculate_default_transform(
            src_crs, target_crs, src.width, src.height, *src.bounds
        )
        # Update metadata for the destination raster
        kwargs = src.meta.copy()
        kwargs.update({
            'crs': target_crs,  # Set the new CRS to WGS 84
            'transform': transform,  # Set the new transform
            'width': width,  # New width
            'height': height  # New height
        })

        # Open the destination file and perform the reprojection
        with rasterio.open(output_path, 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):  # Reproject each band
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src_crs,
                    dst_transform=transform,
                    dst_crs=target_crs,
                    resampling=Resampling.nearest  # Choose resampling method
                )

    print(f"Reprojected file saved as {output_path}")

    # Call the function to reproject the raster
reproject_to_wgs84(input_file, output_file, albers_wkt, targetcrs)
