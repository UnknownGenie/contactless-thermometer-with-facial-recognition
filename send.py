# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 15:58:25 2020

@author: ME
"""

import requests
import argparse
import time
import sys

def send_request(image, temperature, current_time, user_id, url): 
    request ={
       "temperature": temperature,
         "time": current_time, 
        "User ID": user_id
    }
    if isinstance(image, str):
        files = {'media': open(image, 'rb')}
    else:
        files = {'media': image}
    try:
        x = requests.post(url, data = request, files=files)
        return x
    except Exception as e:
        return e

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description = ''' Send requests to server side.\n
                                     takes image path as input. set other variables itself''')
                                 
    parser.add_argument("path", help="Path to image")
    
    args = parser.parse_args()
    
    url = 'Localhost:5000/api/v1/device'
    
    temperature = "27.7C"
    user_id = "rada637367363" 
    image = args.path
    current_time = time.time()
    
    response = send_request(image, temperature, current_time, user_id, url)
    print(response)
