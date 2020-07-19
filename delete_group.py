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

def delete_group(creds_path, persongroup):
    client = face_client(creds_path)
    groups = client.person_group.list()
    group_names = [group.name for group in groups]
    persongroup = group
    # Add group if not found
    if persongroup in group_names:
        client.person_group.delete(persongroup)
        return "Success"
    else:
        print("Group not found")
        sys.exit()

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='''Delete persongroup/employee given id(persongroup). ''')
    parser.add_argument("id", help="ID of the client, this will be name of persongroup")
    parser.add_argument("-k",  help="path to credentials, defaults to cred.json",
                        default='creds.json')
    args = parser.parse_args()
    group = args.id
    creds_path = args.k
    ids = delete_group(creds_path, group)
    print(ids)