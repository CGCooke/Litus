import numpy as np
from optparse import OptionParser
from shapely.geometry import Polygon,Point
from shapely.prepared import prep

import time

def filter(options):
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

	poly = np.loadtxt('Data/Common/polygon.txt',delimiter=',', usecols=(1,2))
	poly = Polygon(poly)
	poly = prep(poly)
	
	minHeight = float(options.minHeight)
	maxHeight = float(options.maxHeight)
	numPoints = inputData.shape[0]

	for i in range(0,numPoints):
		pointLon,pointLat,pointHeight = lon[i],lat[i],height[i]
		point = Point(pointLon,pointLat)
		if minHeight < pointHeight < maxHeight:	
			if poly.contains(point):	
				#Rounding down to save on space and improve I/O
				outputData.write(str(round(pointLon,8))+','+str(round(pointLat,8))+','+str(round(pointHeight,4))+'\n')
	outputData.close()
	
	#Use np.savetxt('test.out', x, delimiter=',')
	print(int(time.time()-startTime),' seconds runtime')

if __name__ == '__main__':

	parser = OptionParser()
	parser.add_option('-i','--inputFilePath', action="store", dest="inputFileName",help="Path to the input file")
	parser.add_option('-o','--outputFilePath', action="store", dest="outputFileName",help="Path to the output file")
	parser.add_option('--minHeight', action="store",  dest='minHeight',help="Minimum height threshold for points")
	parser.add_option('--maxHeight', action="store",  dest='maxHeight',help="Maximum height threshold for points")
	parser.add_option('--polygon', dest='polyFilter',default=False, action='store_true',help="Path to the polygon csv file")


	(options, args) = parser.parse_args()
	filter(options)


