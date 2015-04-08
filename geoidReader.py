''' Style Guide http://www.python.org/dev/peps/pep-0008/ '''

''' standard library imports '''
import math
import pickle

''' related third party imports ''' 
import numpy as np

''' local application/library specific imports '''

''' Functions relating to AUSGoid09, read 
http://www.ga.gov.au/ausgeonews/ausgeonews201003/ausgeoid.jsp
for more information 
'''

def createoffsetDict(fString='Data/Common/AUSGeoid09_GDA94_V1.01_NSW_ACT_CLIP.txt'):
	''' This function loads offsets to the AUS Geoid from a text file '''

	offsetDict={}
	f = open(fString,'r')
	f.readline()
	for line in f:
		LatDegrees,LatMinutes,LonDegrees,LonMinutes,Offset =line.split()[2],line.split()[3],line.split()[5],line.split()[6],line.split()[1]
		
		if LatDegrees[0] =='S':
			LatDegrees = -1*int(LatDegrees[1:])
			LatMinutes = int(LatMinutes)
			LatDecimalDegrees =  LatDegrees - (LatMinutes/60.0)
		else:
			LatDegrees = int(LatDegrees[1:])
			LatMinutes = int(LatMinutes)
			LatDecimalDegrees =  LatDegrees + (LatMinutes/60.0)
			
		LonDegrees = int(LonDegrees[1:])
		LonMinutes = int(LonMinutes)
		LonDecimalDegrees =  LonDegrees + (LonMinutes/60.0)

		offsetDict[(LonDecimalDegrees,LatDecimalDegrees)] =float(Offset)
		
	f.close()
	return(offsetDict)

def loadOffsetDict():
	try:
		f = open("Data/Common/AUSGeoid09_GDA94_V1.01_NSW_ACT_CLIP.bin", "rb" )
		offsetDict =pickle.load(f)
		f.close()
	except:
		offsetDict = createoffsetDict(fString='Data/Common/AUSGeoid09_GDA94_V1.01_NSW_ACT_CLIP.txt')
		f = open("Data/Common/AUSGeoid09_GDA94_V1.01_NSW_ACT_CLIP.bin", "wb" )
		pickle.dump(offsetDict, f)
		f.close()
	return(offsetDict)

def computePointOffset(offsetDict,point):

	#http://www.ga.gov.au/ausgeoid/nvalcomp.jsp
	#Use Bilinear interpolation
	# See formula at:  http://en.wikipedia.org/wiki/bilinearInterpolation

	TargetLon,TargetLat =point
	
	Lon1,Lat1 =  math.floor(TargetLon*60)/60.0,	math.floor(TargetLat*60)/60.0
	Lon2,Lat2 =  math.ceil(TargetLon*60)/60.0,	math.ceil(TargetLat*60)/60.0

	Offset1=offsetDict[(Lon1,Lat1)]
	Offset2=offsetDict[(Lon1,Lat2)]
	Offset3=offsetDict[(Lon2,Lat1)]
	Offset4=offsetDict[(Lon2,Lat2)]
	
	offset =(Offset1 * (Lon2 - TargetLon) * (Lat2 - TargetLat) +
			Offset3 * (TargetLon - Lon1) * (Lat2 - TargetLat) +
			Offset2 * (Lon2 - TargetLon) * (TargetLat - Lat1) +
			Offset4 * (TargetLon - Lon1) * (TargetLat - Lat1)
		    ) / ((Lon2 - Lon1) * (Lat2 - Lat1))

	return(offset)