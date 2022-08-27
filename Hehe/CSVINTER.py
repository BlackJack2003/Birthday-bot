import csv
import scrape as igs

ma = []

with open('varf.txt') as fi:
    za = fi.readlines()
    path = za[0]

def inpu(nas):
    global path
    with open(path+'configs/dat.csv','a') as csvfi:
        csvwriter = csv.writer(csvfi)
        csvwriter.writerows(nas)
    with open(path+'configs/ndat.csv','a') as csvf:
        csvwriter = csv.writer(csvf)
        csvwriter.writerows(nas)
    with open(path+'configs/ndat.csv','r') as csvfi:
        k = csvfi.readlines()
        num = len(k)
        igs.do_user(num)

ga = True
while ga is True:
    x= input("Name:")
    y = input("Date:")
    z = input("InstaID:")
    f = input("More?:[Y/N]")
    ma.append([x,y,z])
    if f.capitalize() != "Y":
        inpu(ma)
        ga = False
    else:
        ga = True