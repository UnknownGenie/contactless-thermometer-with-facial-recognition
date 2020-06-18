# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 15:58:25 2020

@author: ME
"""

import requests
import time
import argparse

def send_request(image, temperature, current_time, user_id): 
    url = 'Localhost:5000/api/v1/device'
    request ={
       "Image": image, 
        "temperature": temperature,
         "time": current_time, 
        "User ID": user_id
    }
    try:
        x = requests.post(url, data = request)
        return x
    except Exception as e:
        return e

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description = ''' Send requests to server side.\n
                                     takes image path as input. set other variables itself''')
                                 
    parser.add_argument("path", help="Path to image")
    
    args = parser.parse_args()
    temperature = "27.7C"
    user_id = "rada637367363" 
    image = open(args.path, 'r+b')
    current_time = time.time()
    
    response = send_request(image, temperature, current_time, user_id)
    print(response)
