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
    except TypeError:
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
    
    # All variables
    url = 'http://127.0.0.1:5000/api/v1/device'
    temperature_float = 27.7
    temperature_string = "{} C".format(temperature_float) # temperature foramtted as this 
    user_id = "rada637367363" 
    
    # Get and format time
    epoch_time = int(time.time())
    formatted_time = time.ctime(epoch_time)
    string_time = '{}'.format(formatted_time)
    
    # load image
    image = cv2.imread(args.path)
    
    # call send_request
    response = send_request(image, temperature_string, string_time, user_id, url)
    print(response)
    