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
import filecmp
import csv
import main as ms

global hdriver

global path
with open('varf.txt') as fi:
    za = fi.readlines()
    path = za[0]

id_no = {}
with open(path+'configs/dat.csv','r') as csvfi:
    lines = csvfi.readlines()
    for m in range(len(lines)):
        line = lines[m]
        li = line.split(',')
        id_no[li[2]] = m

def get_id(a):
    vas = list(id_no.values())
    ke = list(id_no.keys())
    for m in ke:
        if id_no.get(m)==a:
            return id_no[m]
    print("No not present in list")
    quit()

def get_num(id):
    num = id_no.get(id)
    if num == None:
        print("ID is not present in the list")
        quit()
    else:
        return num 

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

def download_from_url_list(lam,id):
    global path
    count = 0
    a = get_num(id)
    for z in lam:
        filename = str(path+'data/imgsc/imgs/%d'%a)
        files = str(path+'data/imgsc/imgs/%d/latest/'%a)
        if count == 1:
            if os.path.isdir(files) is True:
                try:
                    wget.download(z,out=files)
                    count+=1
                except ValueError:
                    continue
            else:
                if os.path.isdir(filename):
                    os.mkdir(files)
                else:
                    os.mkdir(filename)
                    os.mkdir(files)
                try:
                    wget.download(z,out=files+'lat')
                except ValueError:
                    continue
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

def do_list_of_id(id):
    print("Starting")
    driver = ms.get_instagram_browser()
    for m in range(len(id)): 
        urla = "https://www.instagram.com/"+id[m][1:]+'/'
        driver.get(urla)
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        try:
            suggetion=driver.find_element(by=By.XPATH,value='/html/body/div[1]/section/main/div/div[3]/article/div[2]/div/div[2]')
            driver.execute_script("""
            var shit = document.evaluate('/html/body/div[1]/section/main/div/div[3]/article/div[2]/div/div[2]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            shit.remove();
            """)
        except:
            pass
        try:
            mama = driver.find_element(by=By.XPATH,value='/html/body/div[1]/section/main/div/div[1]/div/div')
            driver.execute_script("var crap = document.evaluate('/html/body/div[1]/section/main/div/div[1]/div/div', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;crap.remove();")
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
        download_from_url_list(urls,id[m])
        remjunk()
        time.sleep(2)

def alldo():
    with open(path+'configs/dat.csv','r') as csvfi:
        lines = csvfi.readlines()
        list_of_id = []
        for line in lines:
            #Name,date,ID
            line = line.split(',')
            list_of_id.append(line[2].replace('\n',''))
        do_list_of_id(list_of_id)

def do_user(num):
    do_list_of_id([get_id(num)])

def check_latest(list_of_acc):
    list_id=[]
    with open(path+'configs/dat.csv','r') as csvfi:
        lines = csvfi.readlines()
        for line in lines:
            #Name,date,ID
            line = line.split(',')
            list_id.append(line[2].replace('\n',''))

def check_upload(driver,id):
    #Requires an "driver" webdriver with instgram cookies/logged in and an  target ID
    global path
    driver.get('https://www.instagram.com/%s/'%id)
    temp_path = path+'data/temp'
    try:
        suggetion=driver.find_element(by=By.XPATH,value='/html/body/div[1]/section/main/div/div[3]/article/div[2]/div/div[2]')
        driver.execute_script("""
        var shit = document.evaluate('/html/body/div[1]/section/main/div/div[3]/article/div[2]/div/div[2]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        shit.remove();
        """)
    except:
        pass
    try:
        mama = driver.find_element(by=By.XPATH,value='/html/body/div[1]/section/main/div/div[1]/div/div')
        driver.execute_script("var crap = document.evaluate('/html/body/div[1]/section/main/div/div[1]/div/div', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;crap.remove();")
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
    kaka = wget.download(urls[1],out=temp_path+'/lat')
    for root,dirs,files in os.walk(path+'data/imgsc/imgs/3/latest'):
        fi = files[0]
        pathf = root+'/'+fi
    print("-------x-------"+'\n')
    comp = filecmp.cmp(temp_path+'lat',pathf)
    if comp is True:
        adds = get_num(id)
        os.path.rmdir(path+'data/imgsc/imgs/%d'%adds)
        do_user(adds)

def mains():
    id_present = False
    if len(sys.argv) == 1:
        alldo()
    elif len(sys.argv) == 2:
        arg = sys.argv[1]
        if arg.isalnum() is True: 
            do_list_of_id([get_id(arg)])
        else:
            do_list_of_id([arg])

if __name__ == '__main__':
    mains()
    