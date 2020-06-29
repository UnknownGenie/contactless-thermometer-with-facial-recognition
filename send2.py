# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 15:58:25 2020

@author: ME
"""

import requests

def send_request(image, temperature, current_time, user_id, url): 
    request ={
       "temperature": temperature,
        "time": current_time, 
        "userId": user_id
    }
    
    try:
        imencoded = cv2.imencode(".jpg", image)[1]
        file = {'image': ('image.jpg', imencoded.tostring(), 'image/jpeg', {'Expires': '0'})}
    except TypeError as e:
        print("Please pass image as numpy array")
        return 0
    try:
        x = requests.post(url, data = request, files=file)
        return x
    except Exception as e:
        print(e)
        return 0

if __name__ == '__main__':
    import cv2
    import argparse
    import time

    parser = argparse.ArgumentParser(description = ''' Send requests to server side.\n
                                     takes image path as input. set other variables itself''')
    parser.add_argument("path", help="Path to image")
    args = parser.parse_args()
    
    url = 'https://quiet-tundra-18558.herokuapp.com/api/v1/device'
    temperature = "27.7C"
    user_id = "rada5eeca953242e110004455232"
    image = cv2.imread(args.path)
    current_time = time.time()
    
    ArgumentParserresponse = send_request(image, temperature, current_time, user_id, url)
    print(ArgumentParserresponse)