# -*- coding: utf-8 -*-
"""
Created on Mon May 18 09:17:05 2020

@author: ME
"""

from face_rec.faceapi import train, add_group, add_person, add_image
import os

def train_model(face_client, train_path):
    groups = face_client.person_group.list()
    group_names = [group.name for group in groups]
    for persongroup in os.listdir(train_path):
        if os.path.isfile(persongroup):
            continue
        print("INFO: Processing persongroup {}".format(persongroup))
        persongroup_path = os.path.join(train_path, persongroup)
        
        if not persongroup in group_names: 
            add_group(face_client, persongroup)
        
        persons = face_client.person_group_person.list(persongroup)
        person_names = [person.name for person in persons]
            
        for person in os.listdir(persongroup_path):
            if os.path.isfile(person):
                continue
            print("INFO: Processing person {}".format(person))
            person_path = os.path.join(persongroup_path, person)
    
            if not person in person_names: 
                person_object = add_person(face_client, persongroup, person)
            else:
                idx = person_names.index(person)
                person_object = persons[idx]
            
            
            for image in os.listdir(person_path):
                if image.endswith('jpg'):
                    image_path = os.path.join(person_path, image)
                    print("INFO: Processing image {}".format(image))
                    try: 
                        add_image(face_client,
                              persongroup, 
                              person_object,
                              image_path)
                    except Exception as ex:
                        print("ERROR: {}".format(ex))
                    
    for persongroup in os.listdir(train_path):
        if os.path.isfile(persongroup):
            continue
        train(face_client, persongroup)
        
    
    
    
    
    