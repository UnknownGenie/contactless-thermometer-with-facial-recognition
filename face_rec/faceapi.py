# -*- coding: utf-8 -*-
"""
Created on Mon May 18 09:08:26 2020

@author: ME
"""
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType
import json
import os
import sys
import time


def initialize(KEY, ENDPOINT):
    return FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

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

def add_group(client, group):
    client.person_group.create(person_group_id=group, name=group)

def add_person(client, group, name):
    person = client.person_group_person.create(group, name)
    person.name = name
    return person

def add_image(client, group, person, path):
    f = open(path, 'r+b')
    client.person_group_person.add_face_from_stream(group, 
                                                    person.person_id, 
                                                    f)

def train(client, group):
    client.person_group.train(group)
    while (True):
        training_status = client.person_group.get_training_status(group)
        print("Training status: {}.".format(training_status.status))
        print()
        if (training_status.status is TrainingStatusType.succeeded):
            break
        elif (training_status.status is TrainingStatusType.failed):
            sys.exit('Training the person group has failed.')
        time.sleep(5)