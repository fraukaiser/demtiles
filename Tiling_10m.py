#! /usr/bin/env python2
# -*- #################

#-------------------------------------------------------------------------------
# Name:        Tiling of High Resolution Data (10m)
# Purpose:
#
# Author:      Soraya Kaiser
#
# Last modified:    05.10.2016
# Copyright:   (c) Soraya Kaiser 2016
# Licence:     GNU Public License
#-------------------------------------------------------------------------------

import os, sys
import arcpy
from arcpy.sa import *

file_in = arcpy.GetParameterAsText(0)
value = arcpy.GetParameterAsText(1)

arcpy.CreateFolder_management(arcpy.env.scratchFolder, '1_proc_data')
path_out = arcpy.env.scratchFolder + '\\1_proc_data'
arcpy.env.workspace = path_out
arcpy.env.overwriteOutput = True

fname = file_in.rsplit('\\', 1)[1]
desc = arcpy.Describe(file_in)

arcpy.AddMessage("Calculation in 3 steps")
arcpy.AddMessage("Calculation of step 1: Tiling and Resampling according to chosen threshold")


#####
#### Check cell width
#####
cell = desc.meanCellWidth
width = desc.width
nd = desc.noDataValue
print cell, width, nd
arcpy.AddMessage("The spatial resolution of your dataset is %s meters. Your no data value is: %s" %(str(cell), str(nd)))

####
## Reduce data by resampling original dataset (10m) to a coarser resoultion (90m)
####

arcpy.Resample_management(file_in, "%s_90.tif" %(fname[:-4]), "90", "BILINEAR") # In desperate need of UTM!

#####
#### Fill sinks, Calculate Slope on dataset with coarse resolution
#####

arcpy.CheckOutExtension("Spatial")

demfill = Fill("%s_90.tif" %(fname[:-4]))
slope = arcpy.Slope_3d(demfill, "%s\\%s_slope.tif" %(path_out, fname[:-4]) ,"DEGREE")


#######
###### Tiling 2 by 2
#######

fout = fname[:-4] + '_'
arcpy.SplitRaster_management(slope, path_out, fout, "NUMBER_OF_TILES", "TIFF", "BILINEAR", "2 2", "#", "4", "PIXELS", "#", "#")
arcpy.Delete_management("%s_slope.tif" %(fname[:-4]))
arcpy.Delete_management("%s_90.tif" %(fname[:-4]))


######
#### Select first batch of tiles where slope steepness > 30 degrees. If TRUE: Resample to 30m resolution
######
high = list()
medium_low = list()

tiles = arcpy.ListFiles('*.tif')
for y in[60, 30, 10]:
        for i in tiles:
            np = arcpy.RasterToNumPyArray(i)
            if np.max() > int(value) :
                arcpy.Resample_management(i, "%s_%s.tif" %(str(i)[:-4], str(y)), y , "BILINEAR") # In desperate need of UTM!
		arcpy.AddMessage("Tile calculated")
            else:
                medium_low.append(i)
            arcpy.Delete_management(i)
            resampled = arcpy.ListFiles("*_%s.tif" %(str(y)))
            for i in resampled:
                fout = "%s_" %(str(i)[:-7])
                arcpy.SplitRaster_management(i, path_out, fout, "NUMBER_OF_TILES", "TIFF", "BILINEAR", "2 2", "#", "4", "PIXELS", "#", "#")
                arcpy.Delete_management(i)
            tiles = arcpy.ListFiles("*.tif")

tiles = arcpy.ListFiles("*.tif")
for i in tiles:
    np = arcpy.RasterToNumPyArray(i)
    if np.max() > int(value) :
        high.append(i)
    else:
        medium_low.append(i)

####
## Load Original DEM Data (spatial resolution: 10 m) and ExtractByMask
####


for i in high:
        outRaster = ExtractByMask(file_in, i)
        outRaster.save("%s\\dem%s.tif" %(path_out, str(i)[:-4]))
        arcpy.AddMessage("DEM saved")

####
## Load Original DEM Data, generate Slope and ExtractByMask
####

arcpy.Slope_3d(file_in, "o_slope.tif", "DEGREE")
for i in high:
        outRaster = ExtractByMask("o_slope.tif", i)
        outRaster.save("%s\\o%s.tif" % (path_out, str(i)[:-4]))



#######
###### Calculate Flow Accumulation using orginal DEM Data, prefix "dem"
#######

arcpy.AddMessage("Calculation of step 2: Calculating flow accumulation for tiles where slope > 35 degrees occur")
length = len(high)
count = 0

for i in high:
        count = count + 1
        flowdir = FlowDirection('dem%s.tif' %(str(i[:-4])))
        outFlowAccumulation = FlowAccumulation(flowdir)
        outFlowAccumulation.save("%s_facc.tif" %(i[:-4]))
        arcpy.AddMessage("Now Calculating flow accumulation %s of %s" %(str(count), str(length)))

#####
## Calculate LS with Raster Calculator: Power("flowacc"*[cell resolution]/22.1,0.5)*Power(Sin("slope"*0.01745))/0.09, 1.4)*1.5
#####
arcpy.AddMessage("Calculation of step 3: Calculate LS with Raster Calculator")
arcpy.env.workspace = path_out
facc_files = arcpy.ListFiles('*facc.tif')
count = 0
for i in facc_files:
        count = count + 1
        arcpy.AddMessage("Now Calculating LS %s of %s" %(str(count), str(length)))
        f1 = arcpy.Raster(i)                    # facc files derived from dem_tiles
        f2 = arcpy.Raster('o%s.tif' %(i[:-9]))   # slope files
        exp1 = ((f1*cell)/22.1)
        print exp1
        exp2 = ((Sin(f2*0.01745))/0.09)
        print exp2
        LS_fac = Power(exp1, 0.4) * Power(exp2, 1.0) * 1.4
        LS_fac.save("%s_ls.tif" %(i[:-9]))

####
## For use as a Toolbox, load results into TOC of .mxd file
####
arcpy.env.workspace = path_out
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
results = arcpy.ListFiles('*ls.tif')

for i in results:
	addLayer = arcpy.mapping.Layer("%s" %(str(i)))
	arcpy.mapping.AddLayer(df, addLayer, "BOTTOM")
