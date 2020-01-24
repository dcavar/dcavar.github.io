file = open("readfilel.py")
text = file.readlines()
file.close()
for i in text:
   print i,
