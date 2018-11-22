import cv2
import requests
import json
from time import sleep
face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_alt2.xml')
#eye_cascade  = cv2.CascadeClassifier('data/haarcascade_eye.xml')
old_face_exist = False
cap = cv2.VideoCapture(0)
cap.set(3, 400)
cap.set(4, 400)
bulb_id = 17
base_end_point = 'http://192.168.1.19/api/'
token_end_point = base_end_point+'token'
end_point_thing = base_end_point+'thing/'+str(bulb_id)+'/'
credential = {'email':'me@gmail.com',
               'password':'memememe'}
headers = {'Content-Type':'application/json'}
print('authentication ... ')
r1 = requests.post(token_end_point,data=json.dumps(credential),headers=headers)
token = r1.json()['access']
if token :
    print('authenticated')
headers_token= {'Content-Type':'application/json',
               'Authorization':'Bearer '+token}

def toogle_bulb(state) :
    global end_point_thing
    global headers_token
    action = 'switch_on/'
    if state == False :
        action = 'switch_off/'
    r2 = requests.put(end_point_thing+action,headers=headers_token)
    print(r2)


print('after 5 seconds we will run the webcam')
sleep(5)

while(cap.isOpened()):
    ret, frame = cap.read()
    
    faces = face_cascade.detectMultiScale(frame,1.1,5) # detect faces
    print('there are {nb} face(s) on the video now '.format(nb=len(faces)))
    if len(faces) >= 1 and old_face_exist == False :
        print('turn on')
        toogle_bulb(True)
        old_face_exist = True
    elif len(faces) == 0 and old_face_exist == True :
        print('turn off')
        toogle_bulb(False)
        old_face_exist = False
    for (x,y,w,h) in faces : # loop throught faces
       print('looping throught faces')
       color = (90,202,245) # BGR
       stroke = 5
       strokee = 5
       cv2.rectangle(frame,(x,y),(x+w,y+h),color,stroke)
       # eyes = eye_cascade.detectMultiScale(frame[y:y+h,x:x+w])
       # for (ex,ey,ew,eh) in eyes :
       #     print('eyes cord : ')
       #     cv2.rectangle(frame[y:y+h,x:x+w],(ex,ey),(ex+ew,ey+eh),color,strokee)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('d'):
        break

cap.release()
cv2.destroyAllWindows()
