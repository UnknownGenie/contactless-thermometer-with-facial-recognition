# -*- coding: utf-8 -*-
"""
Created on Mon May 18 11:19:17 2020

@author: ME
"""

import os
from train import train_model
from identify import identify
from face_rec.faceapi import parse_creds, initialize


data_path = os.path.abspath('train_data')
creds_path = os.path.abspath('creds.json')
train_path = os.path.abspath('train_data')
test_path = os.path.abspath('test_data')

print("INFO: Authenticating client...")

KEY, ENDPOINT = parse_creds(creds_path)
face_client = initialize(KEY, ENDPOINT)

print('INFO: Client authenticated.')

train_model(face_client, train_path)
identify(face_client, test_path)