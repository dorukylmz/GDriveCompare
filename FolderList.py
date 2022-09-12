import os
listoffiles=[]
for path, subdirs, files in os.walk(r"C:\Users\Doruk\Desktop"):
    for name in files:
     listoffiles.append(name)

print(listoffiles)

