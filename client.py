# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 15:58:25 2020

@author: ME
"""
import os
import sys
import time
import keyboard
import argparse

import cv2
# from facerecognition import face_locations
from imutils.video import VideoStream

from rpi.request import send_request
from rpi.sensors import init_sensors

def get_timestamp():
    epoch_time = int(time.time())
    formatted_time = time.ctime(epoch_time)
    return '{}'.format(formatted_time)

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", action = 'store_true', default=False,
	help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())
is_pi = args["picamera"]

url = 'https://quiet-tundra-18558.herokuapp.com/api/v1/device'
user_id = "rada5f0ec33c798af800044cb2d9" 
wait_for_temperature = 2
wait_for_snap = 2


get_temperature, get_proximity = init_sensors(is_pi)

cascade_path = os.path.join('face_rec','haarcascade_frontalface_default.xml')

face_cascade = cv2.CascadeClassifier(cascade_path)
vs = VideoStream(usePiCamera=is_pi, resolution = (1280,720)).start()
time.sleep(2.0)

def quit():
    print("Exiting...")
    sys.exit()

# loop over the frames from the video stream
print("Intialized")
while True:
    try:
        if get_proximity():
            print("in range")
            break_it = False
            time.sleep(0.2)
            getting_temerature = time.time()  
            while(True):
                to_send, temperature = get_temperature()
                if to_send:
                    print("correct temperature")
                    # Get timestamp
                    time.sleep(wait_for_snap)
                    timestamp = get_timestamp()
                    # Get frame
                    frame = vs.read()
                    print("Snapped")
                    # Send request
                    response = send_request(frame, temperature, timestamp, user_id, url)
                    print(response)
                    break 
                if time.time() - getting_temerature > wait_for_temperature:
                    break
    except KeyboardInterrupt:
        break
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
print("Exiting...")
sys.exit()
