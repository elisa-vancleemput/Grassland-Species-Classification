#!/usr/bin/env python

# Import python modules
import os
from glob import glob
from osgeo import gdal
from rsgislib.segmentation import segutils


# Create a list of rasters
rasterList = glob("*.tif")
# Delete all images of the plots and leav only the ones from the calibration samples
rasterList = [x for x in rasterList if "plot" not in x]  

# Create folders to store results if thay do no exist
if not os.path.exists("clumps"):
    os.makedirs("clumps")

if not os.path.exists("shp"):
    os.makedirs("shp")


##################### Perform Segmentation #####################

for i in range(len(rasterList)):
    
    # The input image for the segmentation
    inputImage = rasterList[i]
    # The output segments (clumps) image
    clumpsFile = "clumps/"+rasterList[i][:-4]+"_Clump.kea"
        # The output clump means image (for visualsation)
    meanImage = "clumps/"+rasterList[i][:-4]+"_Segments.kea" 
    # The output shapefile
    shapeOut = "shp/"+rasterList[i][:-4]+".shp"

    # run segmentation
    segutils.runShepherdSegmentation(inputImage, clumpsFile,
                    meanImage, numClusters=100, minPxls=1)

    # run polygonization
    gdal.Polygonize(clumpsFile, None, shapeOut, -1, [], callback=None)
