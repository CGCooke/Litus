import unittest
import numpy as np
import random
import time
import os

import geoidReader

class TestSequenceFunctions(unittest.TestCase):
	
	def test_XYZ2LLH(self):

		#Create a test data file 
		f = open('test.csv','w')
		f.write('-4657740.9452499999,2550059.4295000001,-3521355.9040000001\n')
		f.write('-4657740.9452499999,2550059.4295000001,-3521355.9040000001\n')
		f.close()

		#Run it through XYZ2LLH
		os.system('python XYZ2LLH.py  -i  test.csv -o testOut.csv')
		
		#Check the results
		inputData = np.loadtxt('testOut.csv',delimiter=',',usecols=(0,1,2))
		lon=inputData[0,0]
		lat=inputData[0,1]
		height=inputData[0,2]
		np.testing.assert_allclose([lon,lat,height],[151.299804,-33.727470,18.7184])

		#Clean up
		os.system('rm test.csv')
		os.system('rm testOut.csv')
	
	'''
	def test_Reproject(self):

		#Create a test data file 
		f = open('test.csv','w')
		f.write('151.30518782,-33.70769934,22.216\n')
		f.write('151.30518782,-33.70769934,22.216\n')
		f.close()

		#Run it through XYZ2LLH
		os.system('python Reproject.py -i test.csv -o testOut.csv --epsgCode epsg:32756')
		
		#Check the results
		inputData = np.loadtxt('testOut.csv',delimiter=',',usecols=(0,1,2))
		lon=inputData[0,0]
		lat=inputData[0,1]
		height=inputData[0,2]
		np.testing.assert_allclose([lon,lat,height],[151.299804,-33.727470,18.7184])

		#Clean up
		os.system('rm test.csv')
		os.system('rm testOut.csv')
	'''

	def test_Filtering(self):
		#Create a test data file 
		f = open('test.csv','w')
		f.write('0,0,0\n')
		f.write('0,0,0\n')
		f.write('2,2,0\n')
		f.write('0,0,5\n')
		f.write('0,0,-5\n')
		f.close()

		f = open('polygon.csv','w')
		f.write('1,-1,-1\n')
		f.write('2,1,-1\n')
		f.write('3,1,1\n')
		f.write('4,-1,1\n')
		f.close()

		#Test with a polygon
		#Run it through Filter.py
		os.system('python Filter.py -i test.csv -o testOut.csv --minHeight -1 --maxHeight 1 --polygon polygon.csv')
		
		#Check the results
		inputData = np.loadtxt('testOut.csv',delimiter=',',usecols=(0,1,2))
		np.testing.assert_allclose(inputData[0],[0.0,0.0,0.0])
		
		#Test and see what happens when you don't have a polygon
		#Run it through Filter.py
		os.system('python Filter.py -i test.csv -o testOut.csv --minHeight -1 --maxHeight 1')
		
		#Check the results
		inputData = np.loadtxt('testOut.csv',delimiter=',',usecols=(0,1,2))
		np.testing.assert_allclose(inputData[0],[0.0,0.0,0.0])
		np.testing.assert_allclose(inputData[1],[0.0,0.0,0.0])
		np.testing.assert_allclose(inputData[2],[2.0,2.0,0.0])
		
		#Clean up
		os.system('rm polygon.csv')
		os.system('rm test.csv')
		os.system('rm testOut.csv')

	def test_computePointOffset(self):
		#Heights are being checked against Geoscience Australia Applet
		#http://www.ga.gov.au/ausgeoid/nvalcomp.jsp

		offsetDict = geoidReader.loadOffsetDict()

		#Opera House
		offset=geoidReader.computePointOffset(offsetDict,(151.2140,-33.8587))
		np.testing.assert_allclose(round(offset,3),22.762)

		#Barrenjoey Head
		offset=geoidReader.computePointOffset(offsetDict,(151.3300,-33.5800))
		np.testing.assert_allclose(round(offset,3),23.706)

		#Narrabeen
		offset=geoidReader.computePointOffset(offsetDict,(151.2952,-33.7231))
		np.testing.assert_allclose(round(offset,3),23.211)

		#Try and make geoidReader break.
		#Generate 10,000 points randomly within ~5km of narrabeen
		random.seed(0)
		for i in range(0,1000000):
			lon,lat = 151.2952+(random.random()-0.5)*0.1,-33.7231+(random.random()-0.5)*0.1
			offset=geoidReader.computePointOffset(offsetDict,(lon,lat))

if __name__ == '__main__':
	unittest.main()