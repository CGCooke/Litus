import numpy as np
from pyproj import Proj
from optparse import OptionParser
import time

import geoidReader

def reproject(options):
	'''
	Rounding
	http://gis.stackexchange.com/questions/8650/how-to-measure-the-accuracy-of-latitude-and-longitude
	'''

	startTime = time.time()
	inputData = np.loadtxt(options.inputFileName,delimiter=',',usecols=(0,1,2))
	outputData = open(options.outputFileName,'w')

	lon=inputData[:,0]
	lat=inputData[:,1]
	height=inputData[:,2]

	offsetDict = geoidReader.loadOffsetDict()

	proj = Proj(init=options.epsgCode)
	X, Y = proj(lon,lat)
	
	numPoints = inputData.shape[0]
	for i in range(0,numPoints):
		pointX,pointY,pointHeight,pointLon,pointLat  = X[i],Y[i],height[i],lon[i],lat[i]
		offset=geoidReader.computePointOffset(offsetDict,(pointLon,pointLat))
		pointHeight -=offset

		#Rounding down to save on space and improve I/O
		outputData.write(str(round(pointX,4))+','+str(round(pointY,4))+','+str(round(pointHeight,4))+'\n')
	outputData.close()
	
	print(int(time.time()-startTime),' seconds runtime')

if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option('-i','--inputFileName', action="store", dest="inputFileName")
	parser.add_option('-o','--outputFileName', action="store", dest="outputFileName")
	parser.add_option('--epsgCode', action="store", dest="epsgCode")
	
	(options, args) = parser.parse_args()
	reproject(options)


