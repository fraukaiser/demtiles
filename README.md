# Tile-Based Analysis of Digital Elevation Models
Tile-Based Analysis of Digital Elevation Models

Increased soil erosion worldwide results from human activities such as intensive agricul-
ture or deforestation. Studies in the European Alps show that soil loss occurs especially
in areas with steep slopes. Digital terrain models with a high spatial resolution provide
the basis for an estimation of the soil erosion risk caused by steep topographies. Due to
their size the analysis of these datasets often proves to be time and memory consuming.

The tool provides the concept and implementation of a web-based way to evaluate
the topography of a given area dependent on it’s relevance to soil erosion. The software
program being used is arcpy. 

By the implementation of a tile structure the digital terrain model is broken into several equal pieces (tiles). Tiles
that are most likely to be susceptible to soil erosion due to their high slope steepness are
selected and undergo a resampling to a finer resolution. As a result the initially large
dataset is minimized by breaking the input into smaller pieces and providing a higher
resolution in only topographic relevant areas. Afterwards the LS factor of the Revised
Universal Soil Loss Equation is calculated on the basis of the detected tiles.
