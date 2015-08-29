''' Style Guide http://www.python.org/dev/peps/pep-0008/ '''


''' standard library imports '''
import math

''' related third party imports ''' 
import numpy as np
import pyproj

''' local application/library specific imports '''

''' Constants '''
A = 6378137.0
INVFLat = 298.257223563
F = 1.0/INVFLat
ESQUARED = (2.0*F - F**2)
ONE_MINUS_ESQUARED = 1.0 - ESQUARED

def loadIntrinsicParameters(fString = 'Data/Common/t.txt'):
	'''
	This function loads the intrinsic paremeters from file
	and returns them as 3 numpy matricies
	'''

	File = open(fString, "r")
	data= File.read().split()
	File.close()
   
	matrix = np.zeros((3,5))
   
	for r in range(3):
		for c in range(5):
			matrix[r][c] = float(data[c+r*5])
			
	Tne = matrix[:,0:3]
	
	#INS-lidar translation
	ins_lidar = matrix[:,3:4]
	
	#INS-GPS translation
	ins_gps = matrix[:,4:5]
	
	Tne = np.matrix(Tne)
	ins_lidar = np.matrix(ins_lidar)
	ins_gps = np.matrix(ins_gps)
	return(Tne,ins_lidar,ins_gps)

def buildCbnMatrix(Roll,Pitch,Yaw):
	'''
	# direct assignment
	# body frame
	# x == direction of travel
	# y == to the right
	# z == down
	
	# Three rotations to transform the point
	# vector from the body coordinate system
	# to the navigation coordinate system.
	#-----------------------------------------
	#/*
	#Cbn = [ cosd(Yaw)*cosd(Pitch) (cosd(Yaw)*sind(Pitch)*sind(Roll)-sind(Yaw)*cosd(Roll)) (cosd(Yaw)*sind(Pitch)*cosd(Roll)+sind(Yaw)*sind(Roll))
	#		sind(Yaw)*cosd(Pitch) (sind(Yaw)*sind(Pitch)*sind(Roll)+cosd(Yaw)*cosd(Roll)) (sind(Yaw)*sind(Pitch)*cosd(Roll)-cosd(Yaw)*sind(Roll))
	#		-sind(Pitch)            cosd(Pitch)*sind(Roll)                                  cosd(Pitch)*cosd(Roll)]
	#*/
	'''
	
	#Cbn = np.matrix(np.zeros((3,3))) # body to nav frame rotation matrix
	Cbn = np.zeros((3,3)) # body to nav frame rotation matrix

	Roll = math.radians(Roll)
	Pitch = math.radians(Pitch)
	Yaw = math.radians(Yaw)

	cos_Yaw = math.cos(Yaw)
	cos_Pitch = math.cos(Pitch)
	cos_Roll = math.cos(Roll)
	
	sin_Yaw = math.sin(Yaw)
	sin_Pitch = math.sin(Pitch)
	sin_Roll = math.sin(Roll)
	
	# row 1
	Cbn[0,0] = cos_Yaw * cos_Pitch
	Cbn[0,1] = cos_Yaw * sin_Pitch * sin_Roll - sin_Yaw * cos_Roll
	Cbn[0,2]  = cos_Yaw * sin_Pitch * cos_Roll + sin_Yaw * sin_Roll

	# row 2
	Cbn[1,0]  = sin_Yaw * cos_Pitch
	Cbn[1,1]  = sin_Yaw * sin_Pitch * sin_Roll + cos_Yaw * cos_Roll
	Cbn[1,2]  = sin_Yaw * sin_Pitch * cos_Roll - cos_Yaw * sin_Roll

	# row 3
	Cbn[2,0]  = -sin_Pitch
	Cbn[2,1]  = cos_Pitch * sin_Roll
	Cbn[2,2]  = cos_Pitch * cos_Roll

	return(Cbn)

def buildCneMatrix(Lon,Lat):
	# build Cne matrix
	'''
	% matrix of two rotations (3X3)
	% Assumes X = north, Y = East, Z = up
	Cne = [-sind(Lat)*cosd(Lon) -sind(Lon) -cosd(Lat)*cosd(Lon)
		   -sind(Lat)*sind(Lon)  cosd(Lon) -cosd(Lat)*sind(Lon)
			cosd(Lat)            0         -sind(Lat)]

	This gives the point offset (dX, dY, dZ) from the nav frame origin.
	'''
	# transformation / rotation 3X3
	#Cne = np.matrix(np.zeros((3,3))) # nav to ECEF rotation matrix
	Cne = np.zeros((3,3)) # nav to ECEF rotation matrix
	
	sinLat = math.sin(Lat)
	cosLat = math.cos(Lat)
	sinLon = math.sin(Lon)
	cosLon = math.cos(Lon)

	# row 1
	Cne[0,0] = -sinLat * cosLon
	Cne[0,1] = -sinLon
	Cne[0,2] = -cosLat * cosLon

	# row 2
	Cne[1,0]= -sinLat * sinLon
	Cne[1,1] = cosLon
	Cne[1,2] = -cosLat * sinLon

	# row 3
	Cne[2,0] = cosLat
	Cne[2,1] = 0.0
	Cne[2,2] = -sinLat
	return(Cne)

'''
def XYZtoLLH(pointX,pointY,pointZ):
	p = math.sqrt(pointX**2+pointY**2)
	r = math.sqrt(pointX**2+pointY**2+pointZ**2)
	u = math.atan2((pointZ*(1.0-F+(ESQUARED*A)/r)),p)
	
	sin_u = math.sin(u)
	cos_u = math.cos(u)
	Lon = math.atan2(pointY,pointX)
	Lat = math.atan2((pointZ*(1-F)+ESQUARED*A*sin_u*sin_u*sin_u),((1-F)*(p-ESQUARED*A*cos_u*cos_u*cos_u)))
	sin_Lat = math.sin(Lat)
	
	pointHeight = p*math.cos(Lat) + (pointZ * sin_Lat) - A*math.sqrt(1.0 - (ESQUARED * sin_Lat**2))
	
	pointLon = math.degrees(Lon)
	pointLat = math.degrees(Lat)
	
	return(pointLat,pointLon,pointHeight)
'''

def XYZtoLLH(X,Y,Z):
	ecef = pyproj.Proj(proj='geocent',  ellps='WGS84', datum='WGS84')
	wgs84 = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
	lon,lat, alt = pyproj.transform(ecef,wgs84, X,Y,Z)
	return(lon, lat, alt)

def geoPos(Range,Angle,Lat,Lon,Height,Roll,Pitch,Yaw,Tne,ins_lidar,ins_gps):
	''' This function ties together the data from the LiDAR with the GPS INS '''
	
	Lat = math.radians(Lat)
	Lon = math.radians(Lon)
	Angle = math.radians(Angle)

	sinLat = math.sin(Lat)
	cosLat = math.cos(Lat)
	sinLon = math.sin(Lon)
	cosLon = math.cos(Lon)

	''' Setting up some matricies '''
	# coordinates 3X1
	#Pb lidar point in body frame (== INS frame)
	#Pn lidar point in navigation frame
	#Ln  Lidar - GPS offset in nav frame
	#Pe lidar point offset from nav frame origin (dX dY dZ)
	#Tne sensor to body frame rotation matrix
	#Pecef lidar point in XYZ ECEF

	NOe = np.zeros((3,1))# nav frame origin in XYZ ECEF
	Ps = np.zeros((3,1))# lidar point in sensor frame
	
	'''
	# Tne is transformation matrix for body frame to local frame
	# body frame = x direction of vehicle, y clockwise right, z down
	# calcuLate body frame XYZ for target for all lidar measurements
	# assume lidar is aligned to Y-Z body frame plane
	'''

	''' Position vector of point with respect to LiDAR'''
	Ps[0] = Range*math.sin(Angle) 
	Ps[1] = 0.0
	Ps[2] = Range*math.cos(Angle) 

	# rotate Ps by Tne to get Rbrt
	Rbr = np.dot(Tne,Ps)

	# transLate Rb by  to get Pb
	Pb = Rbr - ins_lidar	
	
	#create CbnMatrix
	Cbn = buildCbnMatrix(Roll,Pitch,Yaw)

	# rotate Pb by Cbn to get Pn
	# This is three rotations around (in order) 1)Roll, 2)Pitch 3)Yaw
	Pn = np.dot(Cbn,Pb)
	
	'''
	# Offset between GPS antenna and INS
	#------------------------------------
	# offset in body frame given in input file
	# check if this data is not all 0
	# as this indicates that this trasformation
	# is either not wanted or not needed.
	#if(ts->use_ins_gps)
	#{
	# calcuLate the INS - GPS offset for this epoch
	# in the navigation frame
	#mMultiply(&Ln, &Cbn, &ts->ins_gps)
	'''
	Ln = np.dot(Cbn,ins_gps)

	# add Ln to Pn
	Pn += Ln
	
	# rotate Rn by Tne to get Rt
	Cne = buildCneMatrix(Lon,Lat)

	# rotate Pn by Cne to get Pe
	Pe = np.dot(Cne,Pn)
	# or Rt, if axis transformation is needed

	# or the other way around
	#mMultiply(&Rt, &Cne, &Pn)
	#mMultiply(&Pe, &Tne, &Rt)

	# build NOe
	'''
	transform nav frame origin to ECEF (WGS84) (3X1)
	V is radius of curvature in meridian
	normal section on ellipsoid
	v = a/(sqrt(1-esq*(sind(Lat))**2))
	
	NOe = [(v+h)*cosd(Lat)*cosd(Lon)
		   (v+h)*cosd(Lat)*sind(Lon)
		   (v*one_minus_esquared+h)*sind(Lat)]

	'''

	''' conversion to ECEF '''
	v = A/(math.sqrt(1.0 - (ESQUARED * sinLat**2)))
	
	NOe[0] = (v + Height) * cosLat * cosLon
	NOe[1] = (v + Height) * cosLat * sinLon
	NOe[2] = (v * ONE_MINUS_ESQUARED + Height) * sinLat


	'''
	Apply Range offset to origin in ECEF to obtain the XYZ coordinates of the target.
	Recef = NOe + Pe %(3X1)
	'''
	Pecef = NOe+Pe

	pointX = float(Pecef[0])
	pointY = float(Pecef[1])
	pointZ = float(Pecef[2])
	
	lat,lon,height = XYZtoLLH(pointX,pointY,pointZ)

	return(lat,lon,height)