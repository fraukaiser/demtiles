# Tile-Based Analysis of Digital Elevation Models
Tile-Based Analysis of Digital Elevation Models

Increased soil erosion worldwide results from human activities such as intensive agriculture or deforestation. Studies in the European Alps show that soil loss occurs especially in areas with steep slopes. Digital terrain models with a high spatial resolution provide the basis for an estimation of the soil erosion risk caused by steep topographies. Due to their size the analysis of these datasets often proves to be time and memory consuming.

By the implementation of a tile structure the digital terrain model is broken into several equal pieces (tiles). Tiles that are most likely to be susceptible to soil erosion due to their high slope steepness are selected and undergo a resampling to a finer resolution. As a result the initially large dataset is minimized by breaking the input into smaller pieces and providing a higher
resolution in only topographic relevant areas. Afterwards the LS factor of the Revised Universal Soil Loss Equation is calculated on the basis of the detected tiles.

# Requirements
You will need a version of ArcGIS 10.1 or higher and Python 2.7, which is a standard in the ArcGIS installation.

# Installation 

The Python script »tiling_highresolution.py« is written in ESRI's arcpy and can be used as a Toolbox in ArcMap. Open ArcCatalog, choose Toolboxes -> right click My Toolboxes -> new -> Toolbox (version 10.1/2). Right click on the new toolbox -> add -> script and select the downloaded »tiling_highresolution.py« under script file. The last step contains setting your input values. The first parameter can be named »Input File«/ »DEM« and needs to be of the type »Raster Dataset«. The second input parameter is the »threshold value" for which you want to conduct the analysis (e.g. show me only tiles in which at least one slope value exceeds 50 °). The type is double.  

To learn more about the setup of the toolbox please refer to http://desktop.arcgis.com/en/arcmap/latest/analyze/creating-tools/a-quick-tour-of-creating-tools-in-python.htm


