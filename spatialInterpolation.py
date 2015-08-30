''' Style Guide http://www.python.org/dev/peps/pep-0008/ '''

''' standard library imports '''
import math
import pickle

''' related third party imports '''
import numpy as np
from matplotlib.mlab import griddata
import matplotlib.pyplot as plt

''' local application/library specific imports '''				
import visualization

class processingParameters:
    def __init__(self,directory):
        
        '''The parameters used for processing LiDAR data'''
        self.directory = directory
        self.tileSize = 50
        self.resolution = 0.25
        self.indexesPerTile = self.tileSize/self.resolution
        self.minPointsInTile = 100
        self.minRunsCoveringTile = 1
        self.projection ='epsg:32756'

def createGridSquares(runList,tileSize):
	'''
	Create a list of grid squares
	xSquare,ySquare are defined to be the minimums of tile
	(North East corner)
	'''
	gridSquareDict={}
	for point in run:
		xSquare = int((math.floor(point[0]/tileSize))*tileSize)
		ySquare = int((math.floor(point[1]/tileSize))*tileSize)
		gridSquareDict[(xSquare,ySquare)]=''
	return(gridSquareDict.keys())
	
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
		if (xMin<x and x<xMax) and (yMin<y and y<yMax):
			pointsInTileList.append(point)
	pointsInTile = np.asarray(pointsInTileList)
	return(pointsInTile)
	
def interpolatePoints(square,points,parameters):
	''' Actually perform the spatial interpolation '''
	min_x,min_y = square
	if points.shape[0]>parameters.minPointsInTile:
		X,Y,Z = points[:,0],points[:,1],points[:,2]

		xi = np.linspace(min_x, min_x+parameters.tileSize,parameters.indexesPerTile)
		yi = np.linspace(min_y, min_y+parameters.tileSize,parameters.indexesPerTile)
		
		try:
			zi = griddata(X,Y,Z, xi, yi)
		except KeyError:
			zi = None
		return(zi)

def interpolateTiles(tiles,run,parameters,writeOut=True,visualize=True,kml=False):

	'''Spatially interpolate and display a tile '''
	for tile in tiles:
		interpolatedTileList=[]
	
		print('Finding points in Tile')
		points = pointsInTile(run,tile,parameters.tileSize)
		print(len(points), ' points in tile')
		
		print('Interpolating')
		Interpolated = interpolatePoints(tile,points,parameters)
		print('Finished Interpolating')
		plt.scatter(points[:,0],points[:,1],color='k',alpha=0.1,s=1)
		plt.savefig('Data/Days/'+parameters.directory+'/'+str(tile)+"Scatter.png")
		plt.close()

		if Interpolated != None:
			interpolatedTileList.append(Interpolated)
			plt.imshow(Interpolated)
			plt.savefig('Data/Days/'+parameters.directory+'/'+str(tile)+"Interpolated.png")
			plt.close()
			
			if visualize==True:
				visualization.contourMap(Interpolated,parameters.directory,tile)

			if writeOut ==True:
				f = open('Data/Days/'+parameters.directory+'/'+str(tile)+".bin", "wb" )
				pickle.dump(Interpolated, f)
				f.close()

			if kml==True:
				visualization.writeKMLFile(tile,parameters.directory)

parameters = processingParameters('Narrabeen1')
print('Creating Points List')
run = np.loadtxt('Data/Days/Narrabeen1/UTM.csv',delimiter=',',usecols=(0,1,2))

print('Creating Grid Squares')
tiles = createGridSquares(run,parameters.tileSize)

'''
proj = Proj(init=parameters.projection)
for tile in tiles:
	X,Y = tile 
	
	lon1,lat1 = proj(X,Y,inverse=True)
	lon2,lat2 = proj(X+100,Y+100,inverse=True)
	print(lon1,lat1,lon2,lat2)
'''

print('Interpolating Tiles')
tiles = sorted(tiles)
interpolateTiles(tiles,run,parameters)
