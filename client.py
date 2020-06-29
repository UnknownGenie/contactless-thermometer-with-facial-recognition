# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 15:58:25 2020

@author: ME
"""
import os
import time
import argparse

import cv2
# from facerecognition import face_locations
from imutils.video import VideoStream

from rpi.request import send_request
from rpi.sensors import init_sensors


def detect_face(image):
    #Load a cascade file for detecting faces
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    faces = len(faces)
    
    print("Found "+str(faces)+" face(s)")
    if faces > 0: 
        return True
    else:
        return False

def get_timestamp():
    epoch_time = int(time.time())
    formatted_time = time.ctime(epoch_time)
    return '{}'.format(formatted_time)

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=0,
	help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())

is_pi = args["picamera"]

url = 'https://quiet-tundra-18558.herokuapp.com/api/v1/device'
user_id = "rada5eedf4c9518ee30004f2eba8" 

    
get_temperature, get_proximity = init_sensors(is_pi)

cascade_path = os.path.join('face_rec','haarcascade_frontalface_default.xml')

face_cascade = cv2.CascadeClassifier(cascade_path)
vs = VideoStream(usePiCamera=is_pi, resolution = (1280,720)).start()
time.sleep(2.0)

# loop over the frames from the video stream
print("Intialized")
while True:
    key = cv2.waitKey(1) & 0xFF
	# if the `q` key was pressed, break from the loop
    if get_proximity():
        person_entered = time.time()
        print("in range")
        break_it = False
        while True:
            # Get timestamp
            timestamp = get_timestamp()
            # Get frame
            frame = vs.read()
            if detect_face(frame):
                face_deteted = time.time()
                while True:
                    # Get temperature and trigger condition
                    to_send, temperature = get_temperature()
                    if to_send:
                        print("correct temperature")
                        request = send_request(frame, temperature, timestamp, user_id, url) 
                        print(request)
                        break_it = True
                        break
                    elif time.time() - face_deteted > 2: 
                        print("didnt got Temperature")
                        break_it = True
                        break
            elif time.time() - person_entered > 5: 
                print("face not detected")
                break
            if break_it: break
    if key == ord("q"):
        break
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()

