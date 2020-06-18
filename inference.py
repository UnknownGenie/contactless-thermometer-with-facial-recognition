# -*- coding: utf-8 -*-
"""
Created on Mon May 18 11:19:17 2020

@author: ME
"""
import glob
import os
import time
import argparse
import sys
import json

from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType


def parse_creds(cred_path):
      with open(cred_path) as f:
        creds = json.load(f)
        f.close()
      # Set the FACE_SUBSCRIPTION_KEY environment variable with your key as the value.
      os.environ['FACE_SUBSCRIPTION_KEY'] = creds['FACE_SUBSCRIPTION_KEY']
      KEY = os.environ['FACE_SUBSCRIPTION_KEY']
    
      # Set the FACE_ENDPOINT environment variable with the endpoint from your Face service in Azure.
      os.environ['FACE_ENDPOINT'] = creds['FACE_ENDPOINT']
      ENDPOINT = os.environ['FACE_ENDPOINT']
      return KEY, ENDPOINT

def face_client(cred_path):
    try:
        KEY, ENDPOINT = parse_creds(cred_path) 
        client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
        return client
    except Exception as e:
        print("Authentication failed, kindly check creds.json is placed")
        print("Error: {}".format(e))
        sys.exit()

def run_inference(creds_path, persongroup, path):
    client = face_client(creds_path)
    try:
        image = open(path, 'r+b')
    except Exception as e:
        print("Invalid Path")
        print("Error: {}".format(e))
        sys.exit()
        
    face_ids = []
    azureids = []
    file = path.split(os.sep)[-1]
    try: 
        faces = client.face.detect_with_stream(image)
        if not faces:
            raise Exception('No face detected from image {}'.format(file))
    except Exception as e: 
        print("ERROR: {}".format(e))
        sys.exit
     
    for face in faces:
        face_ids.append(face.face_id)
    
    results = client.face.identify(face_ids, persongroup)
    not_found = 0
    for person, face in zip(results, faces):
        if person.candidates:
            azureid = person.candidates[0].person_id
            azureids.append(azureid)
        else:
            not_found += 1
    if len(results) == not_found:
        sys.exit()
    return azureids

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='''Run unference for image against given id(persongroup). ''')
    parser.add_argument("id", help="ID of the client, this will be name of persongroup")
    parser.add_argument("image", help = "Path to images to be added")
    parser.add_argument("-k",  help="path to credentials, defaults to cred.json",
                        default='creds.json')
    args = parser.parse_args()
    creds_path = args.k
    group = args.id
    image_path = args.image
    ids = run_inference(creds_path, group, image_path)
    print(ids)