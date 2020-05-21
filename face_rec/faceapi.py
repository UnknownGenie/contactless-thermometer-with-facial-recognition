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

class face_client():
    
    def __init__(self, cred_path):
        print("INFO: Authenticating client...")

        KEY, ENDPOINT = self.parse_creds(cred_path) 
        self.client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
        
        print('INFO: Client authenticated.')

    def parse_creds(self, cred_path):
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
    
    def add_group(self, group):
        self.client.person_group.create(person_group_id=group, name=group)
    
    def add_person(self, group, name):
        person = self.client.person_group_person.create(group, name)
        person.name = name
        return person
    
    def add_image(self, group, person, path):
        f = open(path, 'r+b')
        self.client.person_group_person.add_face_from_stream(group, 
                                                        person.person_id, 
                                                        f)
    def clean_groups(self):
        groups = self.client.person_group.list()
        group_names = [group.name for group in groups]
        for group_name in group_names:
            self.client.person_group.delete(group_name)
            
    def train(self, group):
        print('INFO: training {}'.format(group))
        self.client.person_group.train(group)
        while (True):
            training_status = self.client.person_group.get_training_status(group)
            print("Training status: {}.".format(training_status.status))
            print()
            if (training_status.status is TrainingStatusType.succeeded):
                break
            elif (training_status.status is TrainingStatusType.failed):
                sys.exit('Training the person group has failed.')
            time.sleep(5)
            
    def test_metadeta_from_dir(self, test_path, DB):
        for persongroup in os.listdir(test_path):
            if os.path.isfile(persongroup):
                continue
            print("INFO: Processing persongroup {} for testing".format(persongroup))
            persongroup_path = os.path.join(test_path, persongroup)
            for path in os.listdir(persongroup_path):
                image_path = os.path.join(persongroup_path, path)
                cols = '(file, persongroup)'
                vals = "('{}','{}')".format(image_path, persongroup)
                DB.insert('detect', cols, vals)
                
    def identify(self, path, persongroup, id2name):
        image = open(path, 'r+b')
        face_ids = []
        faces = self.client.face.detect_with_stream(image)
        azureids = []
        names = []
        for face in faces:
            face_ids.append(face.face_id)
        results = self.client.face.identify(face_ids, persongroup)
        print('INFO: Identifying faces in {}'.format(path.split(os.sep)[-1]))
        if not results:
            print('INFO: No person identified in the person group for faces from {}.'.format(path))
        for person, face in zip(results, faces):
            if len(person.candidates) != 0:
                azureid = person.candidates[0].person_id
                name = id2name[azureid]
                confidence = person.candidates[0].confidence
                print('INFO: {} is identified with {:.2f} score'.format(name, confidence))
                azureids.append(azureid)
                names.append(name)
        return azureids, names
    def train_metadeta_from_dir(self, train_path, DB):
        groups = self.client.person_group.list()
        group_names = [group.name for group in groups]
        for persongroup in os.listdir(train_path):
            if os.path.isfile(persongroup):
                continue
            print("INFO: Processing persongroup {}".format(persongroup))
            persongroup_path = os.path.join(train_path, persongroup)
            
            if not persongroup in group_names: 
                self.add_group(persongroup)
            
            persons = self.client.person_group_person.list(persongroup)
            person_names = [person.name for person in persons]
              
            for person in os.listdir(persongroup_path):
                if os.path.isfile(person):
                    continue
                print("INFO: Processing person {}".format(person))
                person_path = os.path.join(persongroup_path, person)
        
                if not person in person_names: 
                    person_object = self.add_person(persongroup, person)
                    azure_id = person_object.person_id
                    name = person_object.name
                    cols = '(name, azureid, persongroup)'
                    vals = "('{}','{}','{}')".format(name, azure_id, persongroup)
                    DB.insert('person', cols, vals)
                else:
                    idx = person_names.index(person)
                    person_object = persons[idx]
                
                
                for image in os.listdir(person_path):
                    if image.endswith('jpg'):
                        image_path = os.path.join(person_path, image)
                        print("INFO: Processing image {}".format(image))
                        try: 
                            self.add_image(persongroup, 
                                  person_object,
                                  image_path)
                        except Exception as ex:
                            print("ERROR: {}".format(ex))
                        cols = '(file, persongroup, person)'
                        vals = "('{}','{}','{}')".format(image_path,
                                                      persongroup, person)
                        DB.insert('train', cols, vals)