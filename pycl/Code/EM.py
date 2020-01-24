#! /usr/bin/env python

"""
EM2.py
(C) 2005 by Damir Cavar
GNU General Public License

Expectation Maximization clustering
"""

import math, operator

income = {}
income["Josh"] = 1550.0
income["Tossi"] = 1460.0
income["Amber"] = 1278.0
income["Debbie"] = 3400.0
income["Paul"] = 5430.0
income["Giancarlo"] = 5540.0

group = {}
probability = {}


# Gaussians: mean, deviation
Gaussians = [(1200.0, 200.0), (5000.0, 300.0)]


def GaussianPDF(value, G):
	return (1/float(math.sqrt(2 * math.pi * G[1]))) * math.e**(-1 * (value - G[0])**2 / (2 * G[1]**2))
	# operator.div(1.0, val)


def expectation():
	global group, probability, Gaussians
	for x in income.keys():
		p_g1 = GaussianPDF(income[x], Gaussians[0])
		p_g2 = GaussianPDF(income[x], Gaussians[1])
		print x,
		if p_g1 > p_g2:
			print "G1", p_g1
			group[x] = 0
			probability[x] = p_g1
		else:
			print "G2", p_g2
			group[x] = 1
			probability[x] = p_g2


def maximization():
	global group, Gaussians, probability
	for x in range(len(Gaussians)):
		probs = 0.0
		posprobs = 0.0
		deviations = 0.0
		for i in group.keys():
			if group[i] == x:
				probs += probability[i]
				posprobs += (probability[i] * income[i])
		mean = math.floor(posprobs/probs)
		for i in group.keys():
			if group[i] == x:
				deviations += probability[i] * (mean - income[i])**2
		deviations = math.floor(math.sqrt(deviations / probs))
		Gaussians[x] = (mean, deviations)

print "Data:"
print income

print "Initialization:"
print Gaussians

for x in range(5):
	expectation()
	maximization()
	print "Iteration:", x
	print Gaussians
	print probability, "\n"
