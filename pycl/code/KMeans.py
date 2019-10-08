#!/usr/bin/env python

"""
VectorSpace.py
(C) 2005 by Damir Cavar

This code is free; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This is an implementation of a simple vector space generator for documents and
words in documents.

The columns are words and their relative frequency. The rows are documents.
The program only keeps track of which word appears in which document
how many times. The vectors contain relative frequencies for each word
occurance. The sum over all numbers in a vector is 1.
"""


import sys, math, glob, os.path
from VectorSpace import *


def EuclideanDistance(v1, v2):
	"""Returns the Euclidean distance between two vectors."""
	distance = 0.0
	for m in range(len(v1)):
		distance += math.pow(float(v1[m]-v2[m]), 2)
	return math.sqrt(distance)


def findMostDistant(vectorspace, k):
	"""Find the most distant k vectors."""
	distances = [ ]
	for x in range(len(vectorspace)):
		dv = [ ]
		for y in range(x + 1, len(vectorspace)):
			dv.append(EuclideanDistance(vectorspace[x], vectorspace[y]))
		distances.append(dv)

	dv = [ ]
	for x in distances:
		dv += x
	dv.sort()

	vectors = [ ]
	for x in range(len(distances)):
		for y in range(len(distances[x])):
			if distances[x][y] in dv[-k:]:
				if x not in vectors:
					vectors.append(x)
				if y not in vectors:
					vectors.append(y)
	return vectors[:k]


def getCentroid(v1, v2):
	"""Return the centroid of two vectors."""
	res = []
	for i in range(len(v1)):
		res.append(float(v1[i] + v2[i])/2.0)
	return res
	# return [ (i+j)/2 for i in v1 for j in v2 ]


def recalcCentroid(cval, vectorspace):
	"""Recalculate centroid."""
	tmp = vectorspace[cval[0]][:]
	for i in cval[1:]:
		tmp = getCentroid(tmp, vectorspace[i])
	return tmp


def kMeansCluster(vectorspace, k):
	"""K-Means clustering."""
	# no vector is assigned to a centroid
	notassigned = range(len(vectorspace))
	assigned    = {}
	cvectors    = {}
	# create centroid lists
	centroids   = []
	for x in range(k):
		centroids.append([])

	print "Initialization..."
	# initialize centroids
	c = findMostDistant(vectorspace, k)
	for x in range(len(c)):
		del notassigned[notassigned.index(c[x])]
		assigned[c[x]] = x        # remember which vector belongs to which cluster
		cvectors[x]    = [ c[x] ] # remember which cluster has which vectors
		centroids[x]   = vectorspace[c[x]]

	print "Initial assignment..."
	# assign the rest
	for x in notassigned:
		distances = []
		for i in centroids:
			distances.append(EuclideanDistance(vectorspace[x], i))
		c = distances.index(min(distances))
		assigned[x] = c
		value       = cvectors[c]
		value.append(x)
		cvectors[c]  = value
		centroids[c] = getCentroid(vectorspace[x], centroids[c])
	notassigned = [ ]

	print assigned
	print "Optimization loop..."
	# loop over the vectors and check whether they are still closest to their centroid
	change = True
	while change:
		change = False
		for x in assigned.keys():
			distances = []
			for i in centroids:
				distances.append(EuclideanDistance(vectorspace[x], i))
			c = distances.index(min(distances))
			if c != assigned[x]:
				print "Moving centroid..."
				change = True
				value  = assigned[x]
				cval   = cvectors[value]
				cval.remove(x)
				cvectors[value] = cval
				# recalculate centroid 1
				centroids[value] = recalcCentroid(cval, vectorspace)
				assigned[x]  = c
				value        = cvectors[c]
				value.append(x)
				cvectors[c]  = value
				# recalculate centroid 2
				centroids[c] = recalcCentroid(value, vectorspace)
				centroids[c] = getCentroid(vectorspace[x], centroids[c])
	return cvectors


if __name__ == "__main__":
	if len(sys.argv) > 1:
		docnames = []
		for x in sys.argv[1:]:
			for y in glob.glob(os.path.normcase(x)):
				print "Loading file:", y
				docnames.append(y)
				collectWords(y)
		vectorspace = makeVectorSpace()
		documents = {}  # clean up memory
		k = 4
		clusters = kMeansCluster(vectorspace, k)
		for i in range(k):
			print "Cluster", i
			for x in clusters[i]:
				print docnames[x]
			print ""
	else:
		print "Usage:"
		print "python KMeans.py filename[s]"
