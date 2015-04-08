import unittest
import numpy as np
import random
import time

import geoidReader

class TestSequenceFunctions(unittest.TestCase):

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