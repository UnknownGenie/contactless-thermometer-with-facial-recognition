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

def add_person(client, group, name):
        try:
            person = client.person_group_person.create(group, name)
            person.name = name
            return person
        except Exception as e:
            print("Error occured while adding person")
            print("Error: {}".format(e))
    
def add_group(client, group):
        try:
            client.person_group.create(person_group_id=group, name=group)
        except Exception as e:
            print("Error occured while adding group")
            print("Error: {}".format(e))
            
def add_image(client, group, person, path):
        try:
            f = open(path, 'r+b')
            client.person_group_person.add_face_from_stream(group, 
                                                            person.person_id, 
                                                            f)    
        except Exception as e:
            print("Error occured while adding image")
            print("Error: {}".format(e))
            
def face_client(cred_path):
    try:
        KEY, ENDPOINT = parse_creds(cred_path) 
        client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
        return client
    except Exception as e:
        print("Authentication failed, kindly check creds.json is placed")
        print("Error: {}".format(e))
        sys.exit()
        

def train(client,group):
        client.person_group.train(group)
        print("training...")
        while (True):
            training_status = client.person_group.get_training_status(group)
            if (training_status.status is TrainingStatusType.succeeded):
                break
            elif (training_status.status is TrainingStatusType.failed):
                print('ERROR: Training failed., Try Again...')
            time.sleep(5)
    
def check_add_train(creds_path, group, person, images):
    client = face_client(creds_path)
    
    groups = client.person_group.list()
    group_names = [group.name for group in groups]
    # Add group if not found    
    persongroup = group
    if not persongroup in group_names: 
        add_group(client, persongroup)
    
    persons = client.person_group_person.list(persongroup)
    person_names = [person.name for person in persons]
    # Add person if not found
    if not person in person_names: 
        person_object = add_person(client, persongroup, person)
    else:
        idx = person_names.index(person)
        person_object = persons[idx]
    
    for image in images:
        if image.endswith('jpg'):
            add_image(client, persongroup, person_object, image)
        else:
            print("Error: Please provide images with jpg format")
    train(client, persongroup)
    return person_object.person_id  
if __name__=='__main__':
    parser = argparse.ArgumentParser(description='''Adds group, person and image if not found. Trains as well. ''')
    parser.add_argument("id", help="ID of the client, this will be name of persongroup")
    parser.add_argument("person", help="person name to be added")
    parser.add_argument("images", help = "Path to images to be added")
    parser.add_argument("-k",  help="path to credentials, defaults to cred.json",
                        default='creds.json')
    args = parser.parse_args()
    creds_path = args.k
    creds_path = os.path.abspath(creds_path)
    group = args.id
    person = args.person
    images_path = args.images
    images = glob.glob(os.path.join(images_path, '*.jpg'))
    id_for_person = check_add_train(creds_path, group, person, images)
    print(id_for_person)