import os
import pathlib

os.system("pip3 install -r req.txt")

from importlib.resources import path
import zipfile
import pyAesCrypt as pya 
import time

current_dir = os.getcwd()
def get_path():
    path = input("Please enter a path to install the script, a new folder will be created in said folder containing the Code for the program please donot add a / or \ at the end:")
    try:
        os.mkdir(path+'/bdayw')
    except FileExistsError:
        print("Previous install Detected, it is recomended u delete the previus install by after stoping the current script and deleting the bdayw folder manually and then rerunning the script, you have 4 seconds to hit CTRL+C or CTRL+Z")
        time.sleep(4)
    except:
        print("please enter a valid Path")
        get_path()
    return path

path = get_path()

try:
    os.mkdir(current_dir+'/temp')
except FileExistsError:
    pass
temp_path = current_dir+'/temp'

with zipfile.ZipFile("bdayw.zip") as arch:
    arch.extractall(path)

with open(path+'/bdayw/Code/python/varf.txt','w') as ksa:
    ksa.writelines([path+'/bdayw/'])

def login_and_check(acc,password):
    return True

def get_ma_pass():
    global path
    pkey = input("Please enter a master password [Remember this password as it cannot be reset and will be used to encrypt login information]:")
    acc = input("Please enter a valid Instgram account to be used by the program your login info will be encrypted with above mentioned password, hence it is safe I guess]:")
    password = input("Enter password for instgram account:")
    k = login_and_check(acc,password)
    if k is True:
        print(path+'/bdayw/data/temp/passa.txt')
        with open(path+'/bdayw/data/temp/passa.txt','w') as we:
            we.writelines([acc+'\n',password])
        pya.encryptFile(path+"/bdayw/data/temp/passa.txt",path+'/bdayw/configs/passa.txt.aes',pkey)
        os.remove(path+'/bdayw/data/temp/passa.txt')
    else:
        get_ma_pass()

get_ma_pass()