#-------------------------------------------------------------------------------
# Name:        TopoToolbox Module
# Purpose:
#
# Author:      Soraya Kaiser
#
# Created:     30.07.2016
# Copyright:   (c) Soraya Kaiser 2016
# Licence:     GNU Public License
#-------------------------------------------------------------------------------

from mlab.releases import latest_release as matlab
import sys, os

# pass file_in and path_out as a string, with single quotes only!

def topotoolbox(file_in, path_out):
    fname = file_in.rsplit('\\', 1)[1]
    DEM = matlab.GRIDobj(file_in)
    FD = matlab.FLOWobj(DEM)
    Facc = matlab.flowacc(FD) # creates GRIDobj
    file_out = path_out + '\\' + fname[:-4] + '_facc.tif'
    matlab.GRIDobj2geotiff(Facc, file_out)

topotoolbox(sys.argv[1], sys.argv[2])



