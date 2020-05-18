# -*- coding: utf-8 -*-
"""
Created on Mon May 18 10:59:21 2020

@author: ME
"""
import os


def identify(face_client, test_path):
    for persongroup in os.listdir(test_path):
        if os.path.isfile(persongroup):
            continue
        print("INFO: Processing persongroup {}".format(persongroup))
        persongroup_path = os.path.join(test_path, persongroup)
        persons = face_client.person_group_person.list(persongroup)
        id2name = {person.person_id:person.name for person in persons}
        for path in os.listdir(persongroup_path):
            abspath = os.path.join(persongroup_path, path)
            
            image = open(abspath, 'r+b')
            face_ids = []
            faces = face_client.face.detect_with_stream(image)
            for face in faces:
                face_ids.append(face.face_id)
                
            results = face_client.face.identify(face_ids, persongroup)
            print('INFO: Identifying faces in {}'.format(path))
            if not results:
                print('INFO: No person identified in the person group for faces from {}.'.format(path))
            for person, face in zip(results, faces):
                if len(person.candidates) != 0:
                  print('INFO: {} is identified with {:.2f} score'.format(id2name[person.candidates[0].person_id],
                                                                    person.candidates[0].confidence)) # Get topmost confidence score