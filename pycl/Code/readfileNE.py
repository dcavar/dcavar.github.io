try:
	file = open("some.txt")
	text = file.read()
	file.close()
except IOError:
	print "Cannot open file some.txt."
else:
	print text