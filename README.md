# Litus
UNSW Aviation Lidar Pipeline

Generally  the first step in the processing chain is to convert the .las files into text files.
A very usefull utility in this regard is [las2txt](http://www.liblas.org/utilities/las2txt.html). 

## Installation

### Pre-Requisites.
Litus has a number of pre-requisites. These can be satisfied in two easy steps by installing the following packages : 
* Anaconda
* Pyproj

[Anaconda] (https://store.continuum.io/cshop/anaconda/) is a free distribution of Python that contains over 270 packages that are commonly used for science & engineering applications. 

A thorough overview of how to install Anaconda can be found [here](https://store.continuum.io/static/img/Anaconda-Quickstart.pdf).

Once Anaconda has been successfully installed, we can install [Pyproj](https://pypi.python.org/pypi/pyproj). Pyproj is used by the software to convert between the different coordinate systems used.

Pyproj can be installed by typing the following command in ther terminal : 'pip install pyproj'
