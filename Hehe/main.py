from importlib.resources import path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import os
import pickle
import scrape as sca 
import sys
import csv
import random
import bs4

#Get date and times

global tata
global times

with open('varf.txt') as fi:
    za = fi.readlines()
    path = za[0]

list_id = []
with open(path+"configs/dat.csv") as csvf:
    x = csvf.readlines()
    for m in x:
        list_id.append(m.split(',')[2])


def test_login(driver):
    driver.get('https://www.instagram.com/direct/inbox/')
    try:
        send_msg_button=driver.find_element(by=By.XPATH,value='/html/body/div[1]/section/div/div[2]/div/div/div[2]/div/div[3]/div/button')
        return True
    except:
        return False

def network_reset():
    net1,net2 = logina(2)
    os.system("nmcli con down "+net1)
    #os.system("nmcli con down "+net2)
    time.sleep(2)
    os.system("nmcli con up "+net1)
    #os.system("nmcli con up '"+net2+"'")
    time.sleep(4)

def update_cookies():
    global path
    if os.path.isfile(path+'configs/cookies.pkl'):
        os.remove(path+'configs/cookies.pkl')
    driver = webdriver.Chrome()
    driver.get('https://www.instagram.com/')
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
    user = driver.find_element(by=By.NAME,value="username")
    paswd = driver.find_element(by=By.NAME,value="password")
    userna,passa = logina(1)
    user.send_keys(userna)
    paswd.send_keys(passa,Keys.ENTER)
    savshit = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/section/main/div/div/div/section/div/button")))
    savs = driver.find_element(by = By.XPATH,value='//*[@id="react-root"]/section/main/div/div/div/section/div/button')
    savs.click()
    pickle.dump( driver.get_cookies() , open(path+"configs/cookies.pkl","wb"))
    print("Password Login and cookies updated")

def get_instagram_browser(hid=True):
    if hid == True:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
    else:
        driver = webdriver.Chrome()
    driver.get("https://www.instagram.com/")
    time.sleep(2)
    #login
    try:
        cookies = pickle.load(open(path+"configs/cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        time.sleep(2)
        driver.get('https://www.instagram.com/')
        time.sleep(2)
        mamahar = driver.find_element(by=By.XPATH,value='/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[6]/div[1]/span')
        driver.get('https://www.instagram.com/')
        print("Cookie Login")
        if hid != True:
            try:
                notif = driver.find_element_by_xpath('/html/body/div[6]/div/div/div/div[3]/button[2]')
                notif.click()
                time.sleep(.45)
            except:
                pass
        return driver
    except exceptions.NoSuchElementException:
        try:
            driver = webdriver.Chrome()
            driver.get('https://www.instagram.com/')
            user = driver.find_element(by=By.NAME,value="username")
            paswd = driver.find_element(by=By.NAME,value="password")
            userna,passa = logina(1)
            user.send_keys(userna)
            paswd.send_keys(passa,Keys.ENTER)
            time.sleep(4)
            savs = driver.find_element(by = By.XPATH,value='//*[@id="react-root"]/section/main/div/div/div/section/div/button')
            savs.click()
            pickle.dump(driver.get_cookies(), open(path+"configs/cookies.pkl","wb"))
            #notif = driver.find_element_by_xpath('/html/body/div[6]/div/div/div/div[3]/button[2]')
            #notif.click()
            print("Password login")
            time.sleep(2)
            return driver
        except exceptions.NoSuchElementException:
            network_reset()
            return 0 
    except:
        driver = webdriver.Chrome()
        driver.get('https://www.instagram.com/')
        time.sleep(1)
        user = driver.find_element(by=By.NAME,value="username")
        paswd = driver.find_element(by=By.NAME,value="password")
        userna,passa = logina(1)
        user.send_keys(userna)
        paswd.send_keys(passa,Keys.ENTER)
        time.sleep(4)
        savs = driver.find_element(by = By.XPATH,value='//*[@id="react-root"]/section/main/div/div/div/section/div/button')
        savs.click()
        pickle.dump( driver.get_cookies() , open(path+"configs/cookies.pkl","wb"))
        print("Password login")
        time.sleep(2)
        return driver

def doda():
    global path
    global list_id
    driver = get_instagram_browser()
    with open(path+'configs/dat.csv','r') as csfile:
        i= 0
        if int(tata[5:7])%5 ==0:
            update_cookies()
            for m in list_id:
                sca.check_upload(driver,m)
        #check the date 
        for row in csfile:
            zab = row.split(",")
            print(zab[1])
            kaka = None
            if zab[1] == tata[5:10]:
                if os.path.isdir(path+'/data/imgsc/imgo/%d/'%i) is True:
                    for root, dirs, files in os.walk((path+"/data/imgsc/imgo/%d/"%i), topdown=False):
                        z = files[random.randrange(len(files))]
                        msg = "Happy Birthday " + zab[0] +",many many happy returns of the day."               
                        kaka = str((path+'/data/imgsc/imgo/%d/'%i)+z)
                    rmsghi(driver,[msg,[zab[2]]],imgpath=kaka)
            i+=1

def addrall(msg):
    global path
    lina = []
    with open(path+'configs/dat.csv','r') as csfile:
        for row in csfile:
            zab = row.split(",")
            lina.append(zab[2])
        print("Send the Following message to the ppl in the list below:"+"\n'''"+ msg +"'''\n"+"List of ppl this is being sent to")
        for z in range(0,len(lina)):
            print(lina[z])
        sure = input("Do u want to send this message to all the above mentioned ppl[Y/N]:")
        if sure.capitalize == "Y":
            rmsghi([msg,lina])
        else:
            quit()
            
def addrone(msg,usrno):
    global path
    lina = []
    i= 0
    with open(path+'configs/dat.csv','r') as csfile:
        for row in csfile:
            zab = row.split(",")
            if i == usrno:
                lina.append(zab[2])
        print([msg,lina])
        for z in range(0,len(lina)):
            print(lina[z])

def logina(a):
    global path
    if a == 1:
        mama = open(path+'configs/passa.txt','r')
        sama = mama.readlines()
        acc,passa = sama[0],sama[1]
        return acc,passa
    elif a ==2:
        mama = open(path+'configs/passa.txt','r')
        sama = mama.readlines()
        return sama[2],sama[3]

def rmsghi(driver= None,lis = ["Works",['@bigerbomb2020']],n=0,hid = True,imgpath = None):
    global path

    #initializes the driver/browser
    if driver ==None:
        driver = get_instagram_browser()
        if driver == 0:
            print("Error retrying hit Control+q if this goes on for too long")
            time.sleep(1)
            rmsghi(driver,lis,n,hid)
    #look for the acc
    msg = lis[0]
    for sus in range(0,len(lis[1])):
        acc = lis[1][sus]
        searchs = driver.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input')
        searchs.send_keys(acc)
        time.sleep(1)
        #ENTER USERNAME IN SEARCH BAR
        usersa = driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div/a/div')
        usersa.click()
        #finds the msg button
        time.sleep(3)
        try:
            #click on the msg button
            msgba = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[1]/button')
            msgba.click()
        except exceptions.NoSuchElementException:
            print("Cannot message to this "+ acc +" account as it is not following you and is private")
            ma = input("Wound you like to follow said account:[Y/N]")
            if ma.capitalize() == 'Y':
                try:
                    folo = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/button")
                    folo.click()
                    continue
                except exceptions.NoSuchElementException:
                    continue
            else:
                continue
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')))
        #notification
        if hid != True:
            notif = driver.find_element_by_xpath('/html/body/div[6]/div/div/div/div[3]/button[2]')
            notif.click()
            time.sleep(.45)
        #Enters msg text
        msgbox = driver.find_element_by_xpath('/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')
        msgbox.send_keys(msg,Keys.ENTER)
        print("Message'",msg,"' sent to ",acc)
        #image
        if imgpath!=None:
            imgb = driver.find_element(by = By.XPATH,value='/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/form/input')
            imgb.send_keys(imgpath)
    driver.quit()    

if __name__ == "__main__":
    if len(sys.argv) ==1:
        #stuff only to run when not called via 'import' here
        tata = datetime.datetime.today().strftime('%Y-%d-%m %H:%M:%S')
        times= tata[11:16]
        while True:
            if times == "12:00":
                doda()
            time.sleep(1)
    elif len(sys.argv) ==2:
        addrall(sys.argv[1])
    elif len(sys.argv) ==3:
        addrone(sys.argv[1],sys.argv[2])
