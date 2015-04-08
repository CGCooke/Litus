import numpy as np
import pyproj
from optparse import OptionParser

import time

def createLLHFile(options):
	'''
	Rounding
	http://gis.stackexchange.com/questions/8650/how-to-measure-the-accuracy-of-latitude-and-longitude
	'''

	startTime = time.time()
	XYZdata = np.loadtxt(options.inputFileName,delimiter=' ',usecols=(0,1,2))
	LLHFile = open(options.outputFileName,'w')

	X=XYZdata[:,0]
	Y=XYZdata[:,1]
	Z=XYZdata[:,2]

	ecef = pyproj.Proj(proj='geocent',  ellps='WGS84', datum='WGS84')
	wgs84 = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
	lon,lat, height = pyproj.transform(ecef,wgs84, X,Y,Z)
	
	numPoints = XYZdata.shape[0]
	for i in range(0,numPoints):
		pointLon,pointLat,pointHeight = lon[i],lat[i],height[i]
		LLHFile.write(str(round(pointLon,8))+','+str(round(pointLat,8))+','+str(round(pointHeight,4))+'\n')
	LLHFile.close()
	
	print(int(time.time()-startTime),' seconds runtime')

if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option('-i','--inputFileName', action="store", dest="inputFileName")
	parser.add_option('-o','--outputFileName', action="store", dest="outputFileName")
	(options, args) = parser.parse_args()
	createLLHFile(options)


