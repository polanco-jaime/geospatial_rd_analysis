
# `spatial_analysis` function

## Description
The `spatial_analysis` function is a Python function that performs a spatial analysis between two geospatial datasets: a polygon shapefile (`At`) and a point shapefile (`i`). This function was created with the intention of facilitating the work of economic researchers who intend to use geographic discontinuous regressions. This is why the geography `At` represents the treated area, while `i` represents the geography of individuals.


The function reads in the shapefiles, transforms them to the EPSG 4326 CRS, identifies which points in the `i` dataset are within the `At` polygon, creates a buffer around the `At` polygon based on a user-defined distance (`buffer`), identifies which points in the `i` dataset are within this buffer but outside of the `At` polygon, calculates the Euclidean distance between each point in the `i` dataset and the nearest border of the `At` polygon (positive if inside, negative if outside), and returns a geopandas dataframe with the updated `i` dataset.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/polanco-jaime/geospatial_rd_analysis/blob/main/spatial_analysis_function.ipynb)

## Installation
To use the `spatial_analysis` function, you will need to have Python and the following Python packages installed: geopandas, shutil, tempfile, os, zipfile, and glob.

To install the required packages, you can use the following command:

```
pip install geopandas shutil tempfile os zipfile glob
```

## Usage
To use the `spatial_analysis` function, you need to provide the function with three inputs: the file path to the `At` shapefile, the file path to the `i` shapefile, and the buffer distance (in the same units as the CRS of the input shapefiles).

Here's an example of how to use the `spatial_analysis` function:

### Running from local or colab:"
```
"""Running from local:"""
!pip install git+https://github.com/polanco-jaime/geospatial_rd_analysis.git
from geospatial_rd_analysis.rd_distance import *

path = './path/'
results =  spatial_analysis(At = path+"folder/at.zip", i= path+"path+"folder/i.zip", buffer=10000)

```

 

The `results` variable will contain a geopandas dataframe with the updated `i` dataset, including a new column called "distance_to_At" that contains the Euclidean distances between each point in the `i` dataset and the nearest border of the `At` polygon (positive if inside, negative if outside).

Note that the `At` and `i` shapefiles should be zipped shapefiles (i.e., the .shp, .shx, .dbf, and .prj files should be contained within a single .zip file).