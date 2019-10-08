file = open("readfilelp.py", "r")
line = file.readline()
while line:
   print line,
   line = file.readline()
file.close()
