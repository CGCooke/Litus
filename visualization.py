''' Style Guide http://www.python.org/dev/peps/pep-0008/ '''

''' standard library imports '''

''' related third party imports ''' 
from pylab import *
import matplotlib as mpl
import matplotlib.pyplot as plt
from pyproj import Proj
import math
''' local application/library specific imports '''				

def calculate_initial_compass_bearing(pointA, pointB):
	"""
	Calculates the bearing between two points.
 
	The formulae used is the following:
		θ = atan2(sin(Δlong).cos(lat2),
				  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
 
	:Parameters:
	  - `pointA: The tuple representing the latitude/longitude for the
		first point. Latitude and longitude must be in decimal degrees
	  - `pointB: The tuple representing the latitude/longitude for the
		second point. Latitude and longitude must be in decimal degrees
 
	:Returns:
	  The bearing in degrees
 
	:Returns Type:
	  float
	"""
	if (type(pointA) != tuple) or (type(pointB) != tuple):
		raise TypeError("Only tuples are supported as arguments")
 
	lat1 = math.radians(pointA[0])
	lat2 = math.radians(pointB[0])
 
	diffLong = math.radians(pointB[1] - pointA[1])
 
	x = math.sin(diffLong) * math.cos(lat2)
	y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
			* math.cos(lat2) * math.cos(diffLong))
 
	initial_bearing = math.atan2(x, y)
 
	# Now we have the initial bearing but math.atan2 return values
	# from -180° to + 180° which is not what we want for a compass bearing
	# The solution is to normalize the initial bearing as shown below
	initial_bearing = math.degrees(initial_bearing)
	compass_bearing = (initial_bearing + 360) % 360
 
	return compass_bearing

def generateJasonColormap():
	''' Generate the colorscheme the Jason likes '''
	waterEnd = 0.07
	swashEnd = 0.2
	sandEnd = 0.5

	waterR = 0
	waterG = 0
	waterB = 1

	swashR =1
	swashG =1
	swashB =1

	sandR = 255/255.0
	sandG = 229/255.0
	sandB = 0/255.0

	scrubR =83/255.0
	scrubG =214/255.0
	scrubB =0/255.0
	sandGradient =1

	cdict = {'red': ((0.0, waterR, waterR),
	(waterEnd, waterR, waterR),
	(swashEnd, swashR, swashR),
	(swashEnd,sandR*sandGradient, sandR*sandGradient),
	(sandEnd, sandR, sandR),
	(1.0, scrubR, scrubR)),
	 
	'green': ((0.0, waterG, waterG),
	(waterEnd, waterG, waterG),
	(swashEnd, swashG, swashG),
	(swashEnd, sandG*sandGradient, sandG*sandGradient),
	(sandEnd, sandG, sandG),
	(1.0, scrubG, scrubG)),

	'blue': ((0.0, waterB, waterB),
	(waterEnd, waterB, waterB),
	(swashEnd, swashB, swashB),
	(swashEnd, sandB*sandGradient, sandB*sandGradient),
	(sandEnd, sandB, sandB),
	(1.0, scrubB, scrubB))}
	  
	my_cmap = matplotlib.colors.LinearSegmentedColormap('my_colormap',cdict,256)
	return(my_cmap)

def contourMap(meanArray,directory,square,date='1st January 1900',minCutHeight=-1,maxCutHeight=20,dpi=300,contourInterval=0.25):
	''' Display the tile as a contour map using matplotlib '''
	
	my_cmap = generateJasonColormap()
	fig = plt.figure()
	maxCutHeight = 250
	levels = np.arange(minCutHeight,maxCutHeight, contourInterval)
	format = 'KML'

	if format =='KML':
		''' Making a KML Plot '''
		fig.set_size_inches(10, 10)
		ax = plt.Axes(fig, [0., 0., 1., 1.])
		ax.set_axis_off()
		fig.add_axes(ax)

		plt.contour(meanArray, levels,linewidths=0.2,colors='k')
		
		levels = np.arange(minCutHeight,10, contourInterval)
		plt.contourf(meanArray, levels,cmap = my_cmap)

	else:
		''' Making a plot with a colorbar for a paper '''
		ax = fig.add_subplot(111)
		levels = np.arange(minCutHeight,maxCutHeight, contourInterval)
		plt.contour(meanArray, levels,linewidths=0.2,colors='k')
		
		levels = np.arange(minCutHeight,10, contourInterval)
		plt.contourf(meanArray, levels,cmap = my_cmap)
		
		plt.colorbar()
		plt.xlabel('East (m)')
		plt.ylabel('North (m)')
		date =directory
		plt.title(date)

		ax.set_yticklabels([0,25,50,75,100,125,150,175,200])
		ax.set_xticklabels([0,25,50,75,100,125,150,175,200])        

	plt.savefig('Data/Days/'+directory+'/'+str(square)+'height.png',dpi =dpi)
	plt.close()

def imagePlot(meanArray,directory,square,date='1st January 1900'):
	fig = plt.figure()
	fig.set_size_inches(10, 10)
	ax = plt.Axes(fig, [0., 0., 1., 1.])
	ax.set_axis_off()
	fig.add_axes(ax)
	plt.imshow(np.flipud(meanArray),cmap='gray')
	plt.savefig('Data/Days/'+directory+'/'+str(square)+'height.png',dpi =dpi)
	plt.close()
	
def writeKMLFile(square,directory):
	p = Proj(proj='utm',zone=56,ellps='WGS84')
	
	ulx,uly = square[0],square[1]+100
	llx,lly = square[0],square[1]
	urx,ury = square[0]+100,square[1]+100
	lrx,lry = square[0]+100,square[1]

	ulLon,ulLat = p(ulx,uly,inverse=True)
	llLon,llLat = p(llx,lly,inverse=True)
	urLon,urLat = p(urx,ury,inverse=True)
	lrLon,lyLat = p(lrx,lry,inverse=True)

	lat1 = ulLat
	lat2 = urLat
	lon1 = ulLon
	lon2 = urLon

	rotation = -1*(calculate_initial_compass_bearing((lat1,lon1),(lat2,lon2))-90)
	
	longitudes = sorted([ulLon,llLon,urLon,lrLon])
	latitudes = sorted([ulLat,llLat,urLat,lyLat])

	eastLon = longitudes[2]
	westLon = longitudes[0]
	northLat = latitudes[2]	
	southLat = latitudes[0]


	f = open('Data/Days/'+directory+'/'+str(square)+'.kml','w')
	f.write('''<?xml version="1.0" encoding="UTF-8"?>\n''')
	f.write('''<kml xmlns="http://www.opengis.net/kml/2.2">\n''')
	f.write('''<GroundOverlay>\n''')
	f.write('<name>'+str(square)+'.kml'+'</name>\n')
	f.write('''<color>fff000022</color>\n''')  
	f.write('''<drawOrder>1</drawOrder>\n''')
	f.write('<Icon>')      
	f.write('<href>'+str(square)+'height.png'+'</href>')
	f.write('</Icon>')
	f.write('<LatLonBox>\n')
	f.write('<north>'+str(northLat)+'</north>\n')      
	f.write('<south>'+str(southLat)+'</south>\n')      
	f.write('<east>'+str(eastLon)+'</east>\n')      
	f.write('<west>'+str(westLon)+'</west>\n')
	f.write('<rotation>'+str(rotation)+'</rotation>\n')
	f.write('''</LatLonBox>\n''')
	f.write('''</GroundOverlay>\n''')
	f.write('''</kml>''')
	f.close()



