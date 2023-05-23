import geopandas as gpd
import shutil
import tempfile
import os
import zipfile
import glob

def unzip_files(zip_path, extract_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for member in zip_ref.namelist():
            filename = os.path.basename(member)
            if not filename:
                continue
            source = zip_ref.open(member)
            target = open(os.path.join(extract_path, filename), 'wb')
            with source, target:
                shutil.copyfileobj(source, target)

def spatial_analysis(At, i, buffer):
    # Create temporary directories
    At_temp_dir = tempfile.mkdtemp()
    i_temp_dir = tempfile.mkdtemp()
    
    # Extract the shapefiles to temporary directories
    unzip_files(At, At_temp_dir)
    At_files = glob.glob(os.path.join(At_temp_dir, "*.shp"))

    # Extract the i shapefiles to temporary i directory
    unzip_files(i, i_temp_dir)
    i_files = glob.glob(os.path.join(i_temp_dir, "*.shp"))
    
    # Read the shapefiles and transform to EPSG 3857
    At_gdf = gpd.read_file(os.path.join(At_temp_dir, At_files[0])).to_crs("EPSG:3857")
    i_gdf = gpd.read_file(os.path.join(i_temp_dir, i_files[0])).to_crs("EPSG:3857")
    
    # Identify which observations of 'i' are in 'At'
    i_within = i_gdf.within(At_gdf.unary_union)
    
    # Create a buffer of 'At' with the distance of 'buffer'
    At_gdf_buffer = At_gdf.buffer(buffer)
    
    # Identify which observations of 'i' are outside 'At' but inside the buffer
    i_within_buffer = i_gdf.within(At_gdf_buffer.unary_union) & ~i_within
    
    # Calculate the Euclidean distance between each observation of 'i' and the nearest border of the geometry of 'At'
    distances = []
    for index, row in i_gdf.iterrows():
        if i_within[index]:
            # If the observation is inside 'At', the distance is positive
            distances.append(At_gdf.distance(row.geometry).min())
        elif i_within_buffer[index]:
            # If the observation is outside 'At' but inside the buffer, the distance is negative  
            distances.append(-At_gdf.distance(row.geometry).min()) 
        else:
            # If the observation is outside the buffer, the distance is 0
            distances.append(0)
    
    # Add the distances to the 'i' dataframe
    i_gdf["distance_to_At"] = distances
    
    # Delete the temporary directories
    shutil.rmtree(At_temp_dir)
    shutil.rmtree(i_temp_dir)
    
    # Return the updated 'i' dataframe
    return [i_gdf, At_gdf, i_gdf]
