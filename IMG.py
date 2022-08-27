import numpy as np
import PIL
import mediapipe as mp 
import pandas as pd
import os
import cv2

with open('varf.txt') as fi:
    za = fi.readlines()
    path = za[0]

def find_face(imgs,a,nosh=False):
    global path 
    mp_face = mp.solutions.mediapipe.python.solutions.face_detection
    mp_draw = mp.solutions.mediapipe.python.solutions.drawing_utils
    count = 0
    with mp_face.FaceDetection(model_selection=1,min_detection_confidence=0.5) as face_det:
        for idx, files in enumerate(imgs):
            image = cv2.imread(files)
            results = face_det.process(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))
            if not results.detections:
                if nosh == True:
                    hass = str(path+'data/imgsc/no/%d/'%a)
                    if os.path.isdir(hass):
                        cv2.imwrite(hass + str(idx) + '.png', image)
                        continue
                    else:
                        os.mkdir(hass)
                        cv2.imwrite(hass + str(idx) + '.png', image)
                        continue
                else:
                    continue
            count+=1
            annoted_img = image.copy()
            for detection in results.detections:
                path_to_folder = str(path+'data/imgsc/imgo/%d/'%a)
                if os.path.isdir(path_to_folder):
                    cv2.imwrite(path_to_folder + str(idx) + '.png', annoted_img)
                else:
                    hpath = os.path.join(path+'data/imgsc/imgo/',str(i))
                    os.mkdir(hpath)
                    cv2.imwrite(path_to_folder + str(idx) + '.png', annoted_img)      
    print("%d Images had a face in them"%count)
    return count
    
def scan_user(a):
    global path
    imgs = []
    for root, dirs, files in os.walk((path+"data/imgsc/imgs/%d/"%a), topdown=False):
            for name in files:
                print(os.path.join(root, name))
                imgs.append(os.path.join(root, name))
            if len(imgs) !=0:
                return find_face(imgs,a)
            else:
                return

if __name__== "__main__":
    i = 0
    zeta = True
    totcount=0
    while zeta is True:
        patha = str(path+'data/imgsc/imgs/%d/'%i)
        print(patha)
        if os.path.isdir(patha) is True:
            print('yee')
            totcount+=scan_user(i)
            i+=1
        else:
            pathb = str(path+'data/imgsc/imgs/%d/'%(i+1))
            if os.path.isdir(pathb) is True:
                totcount+=scan_user(i+1)
                i+=2
            else:
                pathc = str(path+'data/imgsc/imgs/%d/'%(i+2))
                if os.path.isdir(pathc) is True:
                    totcount+=scan_user(i+2)
                    i+=3
                else:
                    break
    print("Tot no of img with face=",totcount)