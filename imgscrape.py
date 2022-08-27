import PIL
import pandas as pd
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import wget
import sys
import os
import pickle
import csv
import main as ms

global hdriver

global path
with open('varf.txt') as fi:
    za = fi.readlines()
    path = za[0]

def doda():
    global path
    lina = []
    with open(path+'configs/dat.csv','r') as csfile:
        i = 0
        for row in csfile:
            zab = row.split(",")
            lina.append([zab[2],i])
            i+=1
        olog(lina,0)

def do_user(a):
    global path
    print("Only doing User %d"%a)
    lina = []
    with open(path+'configs/dat.csv','r') as csfile:
        i = 0
        for row in csfile:
            zab = row.split(",")
            lina.append([zab[2],i])
            i+=1
        olog([lina[a-1]],1)

def remjunk():
    zeta = True
    i = 0
    junkl = ['44884218_345707102882519_2446069589734326272_n.jpg']
    for junk in junkl:
        while zeta is True:
            patha = str(path+'/data/imgsc/imgs/%d/'%i)
            if os.path.isdir(patha) is True:
                kk = str(patha+junk)
                if os.path.isfile(kk):
                    os.remove(kk)
                    print("Removed from ",i)
                i+=1
            else:
                pathb = str(path+'/data/imgsc/imgs/%d/'%(i+1))
                if os.path.isdir(patha) is True:
                    kk = str(pathb+junk)
                    if os.path.isfile(kk):
                        os.remove(kk)
                        print("Removed from ",i+1)
                    i+=2
                else:
                    pathc = str(path+'/data/imgsc/imgs/%d/'%(i+2))
                    if os.path.isdir(patha) is True:
                        kk = str(pathc+junk)
                        if os.path.isfile(kk):
                            os.remove(kk)
                            print("Removed from ",i+2)
                        i+=3
                    else:
                        break
    
def down(lam,a):
    count = 0
    for z in lam:
        filename = str(path+'/data/imgsc/imgs/%d/'%a)
        if os.path.isdir(filename) is True:
            try:
                wget.download(z,out=filename)
                count+=1
            except ValueError:
                continue
        else:
            os.mkdir(filename)
            try:
                wget.download(z,out=filename)
                count+=1
            except ValueError:
                continue
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
    print("\nAccount %d Done"%a,end =' ')
    print("%d Images were Downloaded"%count)

def olog(accs,ex):
    driver = ms.get_instagram_browser(hid=True)
    for i in range(len(accs)):
        urla = "https://www.instagram.com/"+accs[i][0][1:]+'/'
        driver.get(urla)
        time.sleep(1)
        try:
            suggetion=driver.find_element(by=By.XPATH,value='/html/body/div[1]/section/main/div/div[3]/article/div[2]/div/div[2]')
            driver.execute_script("""
            var shit = document.evaluate('/html/body/div[1]/section/main/div/div[3]/article/div[2]/div/div[2]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            shit.remove();
            """)
        except:
            pass
        soup = BeautifulSoup(driver.page_source,'html.parser')
        urls = []
        for img in soup.find_all("img"):
            img_url = img.attrs.get("src")
            urls.append(img_url)
            if not img_url:
                # if img does not contain src attribute, just skip
                continue
        down(urls,accs[i][1])
        remjunk()
        time.sleep(2)
    driver.quit()

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
    if len(sys.argv) ==1:
        print("Starting")
        doda()
    else:
        do_user(int(sys.argv[1]))
