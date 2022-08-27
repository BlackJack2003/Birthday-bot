import zipfile
import os

with open('varf.txt') as fi:
    za = fi.readlines()
    path = za[0]

k = path+"'install fold'/bdayw.zip"

if os.path.isfile(k):
    os.remove(k)

zipfile("")
