# Litus
UNSW Aviation Lidar Pipeline

## Overview of Litus

Litus currently contains 3 program, they are :
* XYZ2LLH.py : Convert data from ECEF coordinates to Longitude,Latitude,Height
* Filter.py : Filter points by height and using a polygon
* Reproject.py : Convert points from Longitude,Latitude,Height to another coordinate system.

A fourth program:
* las2txt.exe : Convert data from .las format to .csv format

## Internal processing
The RIEGL VQ-480i measures range and angle data,
which is combined with a position and attitude data
from the GPS-IMU RTK package. The end product
is a .las file containing a list of geo-referenced LiDAR
returns. The coordinate system used is ECEF, and
each point has an associated return intensity, time of
capture, as well as if it was the first, second ... nth
return from a pulse.

## Installation

Generally  the first step in the processing chain is to convert the .las files into text files.
A very useful utility in this regard is [las2txt](http://www.liblas.org/utilities/las2txt.html). 

### Pre-Requisites
Litus has a number of pre-requisites. These can be satisfied in two easy steps by installing the following packages : 
* Anaconda
* Pyproj

[Anaconda] (https://store.continuum.io/cshop/anaconda/) is a free distribution of Python that contains over 270 packages that are commonly used for science & engineering applications. 

A thorough overview of how to install Anaconda can be found [here](https://store.continuum.io/static/img/Anaconda-Quickstart.pdf).

Once Anaconda has been successfully installed, we can install [Pyproj](https://pypi.python.org/pypi/pyproj). Pyproj is used by the software to convert between the different coordinate systems used.

Pyproj can be installed by typing the following command in ther terminal : 'pip install pyproj'

## Using las2txt  

The .las file created contains the position in space of
each LiDAR return , as well as its time and the intensity
of the returning pulse. This data is held in format
which is not immediately accessible to end users. 

The command 'las2txt.exe -i *las -parse xyz -sep comma' can be
used to batch process files. The command instructs
las2text to take any .las files as input, and for each
input file to output a file containing the X,Y,Z 
coordinates, one to a line. The X,Y,Z Coordinates are in
the ECEF coordinate system.

More information about las2txt can be found [here](http://www.cs.unc.edu/~isenburg/lastools/download/las2txt_README.txt).

## Using Python Scripts
Each of the scripts can be run independently, or as part of a processing pipeline. Pipeline.py provides an example of how this can be achieved. For quick help using any of the scripts, call the scrip using the '-h' or '--help' option.
For example 'python XYZ2LLH.py --help'. As a matter of convention, all coordinates are specified in x,y,z order (Longitude, Latitude, Height). 

### XYZ2LLH.py
XYZ2LLH.py converts points from ECEF (X,Y,Z) to WGS84 (Longitude,Latitude,Height).

Options:
* -h, --help            : Display documentation
* -i , --inputFilePath  : Path to the input file
* -o , --outputFilePath : Path to the output file

An example usage of the script is as follows:  
'python XYZ2LLH.py -i Data/Days/Narrabeen1/150319_030412.txt -o Data/Days/Narrabeen1/XYZ2LLH.csv'

### Filter.py
Filter.py filters points according to their spatial location.
The filtration occours in two stages :  
* Points that don't lie between the min height and max height. 
* Points that don't lie inside a polygon (if provided).

If a polygon is provided, it must be a CSV file with the following format: "point number, x , y".

IE :  
  1,151.3042614701,-33.7336336437  
  2,151.3038041164,-33.7336926571  
  3,151.3033320093,-33.7336631504  
  4,151.3028599022,-33.7334418502  
  5,151.3022992750,-33.7328664696  
  6,151.3016796344,-33.7320845422  
  
Options:
* -h, --help            : Display documentation
* -i , --inputFilePath  : Path to the input file
* -o , --outputFilePath : Path to the output file
* --minHeight           : Minimum height threshold for points
* --maxHeight           : Maximum height threshold for points
* --polygon             : Path to the polygon csv file  

An example usage of the script is as follows:  
'python Filter.py -i Data/Days/Narrabeen1/XYZ2LLH.csv -o Data/Days/Narrabeen1/Filtered.csv --minHeight 13.211 --maxHeight 43.211 --polygon Data/Common/polygon.csv'
  
### Reproject.py
Reproject projects points from one projection to annother. Simultaniously, it converts the height from the WGS84 elisoidal height to the Australian Height Geoid using the AusGeoid09 [AusGeoid09](http://www.ga.gov.au/ausgeonews/ausgeonews201003/ausgeoid.jsp) model. This script is typically used to convert points from WGS84 to either the [GDA94](http://www.ga.gov.au/scientific-topics/positioning-navigation/geodesy/geodetic-datums/gda) or [UTM](http://en.wikipedia.org/wiki/Universal_Transverse_Mercator_coordinate_system) coordinate system. The advantage of using the UTM or GDA94 coordinate system is that the axis are orthoganal, and distances are in meters, rather than degrees. 

* -h, --help : show this help message and exit
* -i, --inputFilePath : Path to the input file
* -o, --outputFilePath : Path to the output file
* --epsgCode : EPSG code of the transform to use. For example,'epsg:32756' is the code for UTM zone 56 South.

An example usage of the script is as follows:  
  'python Reproject.py -i Data/Days/Narrabeen1/Filtered.csv -o Data/Days/Narrabeen1/UTM.csv --epsgCode epsg:32756'
