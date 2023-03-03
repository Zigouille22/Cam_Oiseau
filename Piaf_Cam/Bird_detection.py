import cv2
import datetime 
import time
import os

compteur = 0

NAS = "Z:\Cam_Oiseau\photo_oiseaux"

if not os.path.exists(NAS):
    print("Nas inaccessible")
    
now = datetime.datetime.now()
date = now.strftime('%d-%m-%Y-%H-%M')

bird2_cascade = cv2.CascadeClassifier('bird2-cascade.xml')
 
cam = cv2.VideoCapture("http://192.168.1.54:81/stream")

fps = cam.get(cv2.CAP_PROP_FPS)
print("Le frame rate actuel de la vidéo est :", fps)
nouveau_fps = 20
cam.set(cv2.CAP_PROP_FPS, nouveau_fps)
fps = cam.get(cv2.CAP_PROP_FPS)
print("Le nouveau frame rate de la vidéo est :", fps)

start_time = time.time()

while 1: 
    ret, frame = cam.read() 

    if not(ret):
        print("camera ne marche pas")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    birds2 = bird2_cascade.detectMultiScale(gray, 1.3, 5)
    elapsed_time = time.time() - start_time  

    for (x,y,w,h) in birds2:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, 'Bird', (x-w, y-h), font, 0.5, (0,255,255), 2, cv2.LINE_AA)
        if elapsed_time >= 5:
            cv2.imwrite(os.path.join(NAS,'image_{} {}.jpg'.format(compteur, date)), frame)
            compteur +=1
            print("photo capturée !")
            start_time = time.time()
        
 
    cv2.imshow('img',frame)
 
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
 
cam.release()

cv2.destroyAllWindows() 
