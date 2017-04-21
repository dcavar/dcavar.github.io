#! /usr/bin/env python

"""
chi2.py
(C) 2004 by Damir Cavar <dcavar@indiana.edu>

License:

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

http://www.gnu.org/licenses/gpl.txt


chi2-test

chi2-value = sum over (Observation - Expectation)^2/Expectation

Observation = found frequency
Expectation = expected frequency
"""

from math import pow

class Chi2:
	# Probability 				
	probs = (0.99, 0.95, 0.05, 0.01, 0.001)
	# by df
	table = {
		1:(0, 0.004, 3.84, 6.64, 10.83),
		2:(0.02, 0.103, 5.99, 9.21, 13.82),
		3:(0.115, 0.352, 7.82, 11.35, 16.27),
		4:(0.297, 0.711, 9.49, 13.28, 18.47),
		5:(0.554, 1.145, 11.07, 15.09, 20.52),
		6:(0.872, 1.635, 12.59, 16.81, 22.46),
		7:(1.239, 2.167, 14.07, 18.48, 24.32),
		8:(1.646, 2.733, 15.51, 20.09, 26.13),
		9:(2.088, 3.325, 16.92, 21.67, 27.88),
		10:(2.558, 3.94, 18.31, 23.21, 29.59),
		11:(3.05, 4.58, 19.68, 24.73, 31.26),
		12:(3.57, 5.23, 21.03, 26.22, 32.91),
		13:(4.11, 5.89, 22.36, 27.69, 34.53),
		14:(4.66, 6.57, 23.69, 29.14, 36.12),
		15:(5.23, 7.26, 25, 30.58, 37.7),
		16:(5.81, 7.96, 26.3, 32, 39.25),
		17:(6.41, 8.67, 27.59, 33.41, 40.79),
		18:(7.02, 9.39, 28.87, 34.81, 42.31),
		19:(7.63, 10.12, 30.14, 36.19, 43.82),
		20:(8.26, 10.85, 31.41, 37.57, 45.32),
		21:(8.9, 11.59, 32.67, 38.93, 46.8),
		22:(9.54, 12.34, 33.92, 40.29, 48.27),
		23:(10.2, 13.09, 35.17, 41.64, 49.73),
		24:(10.86, 13.85, 36.42, 42.98, 51.18),
		25:(11.52, 14.61, 37.65, 44.31, 52.62),
		26:(12.2, 15.38, 38.89, 45.64, 54.05),
		27:(12.88, 16.15, 40.11, 46.96, 55.48),
		28:(13.57, 16.93, 41.34, 48.28, 56.89),
		29:(14.26, 17.71, 42.56, 49.59, 58.3),
		30:(14.95, 18.49, 43.77, 50.89, 59.7) }


	def getChi2Value(self, sample, expectation):
		"""Calculate the t-test value for a sample."""
		chi2 = 0.0
		for x in range(len(sample)):
			for i in range(len(sample[0])):
				chi2 += pow(float(sample[x][i] - expectation[x][i]), 2) / float(expectation[x][i])
		return chi2


	def getDF(self, sample):
		"""Returns the degree of freedom."""
		return (len(sample) - 1) * (len(sample[0]) - 1)


	def getSignificance(self, chi2value, df):
		"""Returns the probability = significance value for the tvalue, given the df."""
		if df > len(self.table.keys()):
			df = max(self.table.keys())
		scores = self.table[df]
		for i in range(len(scores)):
			if scores[i] > chi2value:
				i = i - 1
				break
		if i == -1:
			return 1.0
		else:
			return self.probs[i]


	def isSignificant(self, sample, expectation, level):
		"""Returns the significance of the difference between two samples."""
		val = self.getSignificance(self.getChi2Value(sample, expectation), self.getDF(sample))
		if val <= level:
			return True
		return False


if __name__ == "__main__":
	# some example
	sample = [(161, 59, 58), (23, 21, 29)]
	expectation = [(60, 60, 60), (20, 20, 20)] # H0 = equal proportions

	myChi2 = Chi2()
	df = myChi2.getDF(sample)
	chi2 = myChi2.getChi2Value(sample, expectation)
	significance = myChi2.getSignificance(chi2, df)
	print "Sample", sample
	print "Expectation = H0:", expectation
	print "chi2-test:\nchi2 =", chi2
	print "df =", df
	print "Is significant: (0.05)", myChi2.isSignificant(sample, expectation, 0.05)
	# print "Alpha level exceeded", significance
