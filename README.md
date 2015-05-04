# Litus
UNSW Aviation Lidar Pipeline

Generally  the first step in the processing chain is to convert the .las files into text files.
A very useful utility in this regard is [las2txt](http://www.liblas.org/utilities/las2txt.html). 

## Installation

### Pre-Requisites
Litus has a number of pre-requisites. These can be satisfied in two easy steps by installing the following packages : 
* Anaconda
* Pyproj

[Anaconda] (https://store.continuum.io/cshop/anaconda/) is a free distribution of Python that contains over 270 packages that are commonly used for science & engineering applications. 

A thorough overview of how to install Anaconda can be found [here](https://store.continuum.io/static/img/Anaconda-Quickstart.pdf).

Once Anaconda has been successfully installed, we can install [Pyproj](https://pypi.python.org/pypi/pyproj). Pyproj is used by the software to convert between the different coordinate systems used.

Pyproj can be installed by typing the following command in ther terminal : 'pip install pyproj'

## Using Scripts
Each of the scripts can be run independently, or as part of a processing pipeline. Pipeline.py provides an example of how this can be achieved. For quick help using any of the scripts, call the scrip using the '-h' or '--help' option.
For example 'python XYZ2LLH.py --help'. As a matter of convention, all coordinates are specified in x,y,z order (Longitude, Latitude, Height). 

### XYZ2LLH.py
XYZ2LLH converts points from ECEF (X,Y,Z) to WGS84 (Longitude,Latitude,Height).

Options:
* -h, --help            : Display documentation
* -i , --inputFilePath  : Path to the input file
* -o , --outputFilePath : Path to the output file

An example usage of the script is as follows: 'python XYZ2LLH.py -i Data/Days/Narrabeen1/150319_030412.txt -o Data/Days/Narrabeen1/XYZ2LLH.csv'

### Filter.py

Options:
* -h, --help            : Display documentation
* -i , --inputFilePath  : Path to the input file
* -o , --outputFilePath : Path to the output file
* --minHeight           : Minimum height threshold for points
* --maxHeight           : Maximum height threshold for points
* --polygon             : Path to the polygon csv file  

An example usage of the script is as follows: 'python Filter.py -i Data/Days/Narrabeen1/XYZ2LLH.csv -o Data/Days/Narrabeen1/Filtered.csv --minHeight 13.211 --maxHeight 43.211 --polygon Data/Common/polygon.csv'
  
### Reproject.py

* -h, --help : show this help message and exit
* -i, --inputFilePath : Path to the input file
* -o, --outputFilePath : Path to the output file
* --epsgCode : EPSG code of the transform to use. For example,'epsg:32756' is the code for UTM zone 56 South.

An example usage of the script is as follows: 'python Reproject.py -i Data/Days/Narrabeen1/Filtered.csv -o Data/Days/Narrabeen1/UTM.csv --epsgCode epsg:32756'
