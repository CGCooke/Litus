''' Style Guide http://www.python.org/dev/peps/pep-0008/ '''

''' standard library imports '''
import math
import os
import pickle

''' related third party imports '''
from pyproj import Proj
import numpy as np
from matplotlib.mlab import griddata
from shapely.geometry import Polygon,Point
from shapely.prepared import prep

''' local application/library specific imports '''				
import visualization
import geoidReader
import geopos

def createLLHFile(parameters,fString):
	'''
	Rounding
	http://gis.stackexchange.com/questions/8650/how-to-measure-the-accuracy-of-latitude-and-longitude
	'''

	data = np.loadtxt('Data/Days/'+parameters.directory+'/'+fString,delimiter=' ')
	LLHFile = open('Data/Days/'+parameters.directory+'/'+fString[:-4]+'LLH.csv','w')

	
	if parameters.AUSGeoid09 ==True:
		offsetDict = geoidReader.loadOffsetDict()

	numPoints = data.shape[0]
	for i in range(0,numPoints):
		pointX,pointY,pointZ = data[i]
		pointLat,pointLon,pointHeight = geopos.XYZtoLLH(pointX,pointY,pointZ)

		if parameters.AUSGeoid09 ==True:
			offset=geoidReader.computePointOffset(offsetDict,(pointLat,pointLon))
			pointHeight -=offset
		#Rounding down to save on space and improve I/O
		LLHFile.write(str(round(pointLat,8))+','+str(round(pointLon,8))+','+str(round(pointHeight,4))+'\n')

	LLHFile.close()

'''
def loadBoundingPolygon(fString='Data/Common/polygon.txt'):
	f = open(fString)
	poly=[]
	for line in f.readlines():
		pointNum,Lon,Lat = line.split(',')
		poly.append((float(Lon),float(Lat)))
	f.close()
	return(poly)
'''

def createPointList(parameters):
	p = Proj(init=parameters.projection)
	
	poly = np.loadtxt('Data/Common/polygon.txt',delimiter=',', usecols=(1,2))
	poly = Polygon(poly)
	poly = prep(poly)
	runList=[]
	
	print('Converting XYZ to LLH')
	for fString in os.listdir('./Data/Days/'+parameters.directory):
		if '.txt' in fString:
			createLLHFile(parameters,fString)

	
	print('Filtering points')
	for fString in os.listdir('./Data/Days/'+parameters.directory):
		if 'LLH' in fString:
			f = open('./Data/Days/'+parameters.directory+'/'+fString)
			print('Reading in points')
			LatArray,LonArray,HeightArray = np.loadtxt(f, delimiter=',', usecols=(0,1,2), unpack=True)
			print(LatArray.size,' points before filtering')
			pointList=[]        
			for i in range(0,LatArray.size):
				Lat,Lon,Height = LatArray[i],LonArray[i],HeightArray[i]
				if (parameters.minCutHeight<Height<parameters.maxCutHeight):
					point = Point(Lon,Lat)
					if parameters.cutByPolygon==True:
						if poly.contains(point):
							x,y=p(Lon,Lat)
							pointList.append((x,y,Height))
					else:
						x,y=p(Lon,Lat)
						pointList.append((x,y,Height))
			g = open('./Data/Days/'+parameters.directory+'/'+fString[:-4]+'AMG.csv','w')
			for point in pointList:
				x,y,Height = point
				g.write(str(x)+','+str(y)+','+str(Height)+'\n')
			g.close()			
			print(len(pointList),' points after filtering')
			runList.append(pointList)
			f.close()
	return(runList)

def createGridSquares(runList,tileSize):
	'''
	Create a list of grid squares
	xSquare,ySquare are defined to be the minimums of tile
	'''
	gridSquareDict={}
	for run in runList:
		for point in run:
			xSquare = int((math.floor(point[0]/tileSize))*tileSize)
			ySquare = int((math.floor(point[1]/tileSize))*tileSize)
			gridSquareDict[(xSquare,ySquare)]=''

	return(gridSquareDict.keys())
	 
def interpolateTiles(tiles,runList,parameters,writeOut=True,visualize=True,kml=True):

	'''Spatially interpolate and display a tile '''
	for tile in tiles:

		
		interpolatedTileList=[]
		print(tile)
		for run in runList:
			print('Finding points in Tile')
			points = pointsInTile(run,tile,parameters.tileSize)
			print(len(points), ' points in tile')
			print('Interpolating')
			Interpolated = interpolatePoints(tile,points,parameters)
			print('Finished Interpolating')
			if Interpolated != None:
				interpolatedTileList.append(Interpolated)
	
		if len(interpolatedTileList)>=parameters.minRunsCoveringTile:
			if len(interpolatedTileList)==1:
				processedArray = interpolatedTileList[0]
			else:
				processedArray = np.mean(np.asarray(interpolatedTileList))

			if visualize==True:
				visualization.contourMap(processedArray,parameters.directory,tile)

			if writeOut ==True:
				f = open('Data/Days/'+parameters.directory+'/'+str(tile)+".bin", "wb" )
				pickle.dump(processedArray, f)
				f.close()

			if kml==True:
				visualization.writeKMLFile(tile,parameters.directory)
	
def pointsInTile(pointList,square,tileSize,boundary = 10):
	''' Find the points that lie in a grid square '''
	'''What is the difference between a grid square and a tile? '''
	
	xMin,yMin = square
	xMin = xMin - boundary
	yMin = yMin - boundary
	xMax = xMin + tileSize + boundary
	yMax = yMin + tileSize + boundary
	
	pointsInTileList=[]
	for point in pointList:
		x,y,h = point
		if (xMin<x and x<xMax) and ((yMin-boundary)<y and y<(yMax+boundary)):
			pointsInTileList.append(point)
	return(pointsInTileList)
	
def interpolatePoints(square,points,parameters):
	''' Actually perform the spatial interpolation '''
	min_x,min_y = square
	
	xList=[]
	yList=[]
	heightList=[]
	if len(points)>parameters.minPointsInTile:
		for point in points:
			X,Y,Height = point
			xList.append(X)
			yList.append(Y)
			heightList.append(Height)
		
		xArray = np.asarray(xList)
		yArray = np.asarray(yList)
		heightArray = np.asarray(heightList)

		xi = np.linspace(min_x, min_x+parameters.tileSize,parameters.indexesPerTile)
		yi = np.linspace(min_y, min_y+parameters.tileSize,parameters.indexesPerTile)
		
		try:
			zi = griddata(xArray, yArray, heightArray, xi, yi)
		except:
			zi = None
		return(zi)

def spatiallyInterpolateData(parameters):
	
	print('Creating Points List')
	runList = createPointList(parameters)
	
	'''
	print('Creating Grid Squares')
	tiles = createGridSquares(runList,parameters.tileSize)
	print(tiles)
	print('Interpolating Tiles')
	tiles = sorted(tiles)
	interpolateTiles(tiles,runList,parameters)
	'''
	