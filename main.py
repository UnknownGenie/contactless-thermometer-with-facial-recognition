# -*- coding: utf-8 -*-
"""
Created on Mon May 18 11:19:17 2020

@author: ME
"""
import platform
import os
import sys
from face_rec.faceapi import face_client
from face_rec.db_ops import db_ops


data_path = os.path.abspath('train_data')
creds_path = os.path.abspath('creds.json')
train_path = os.path.abspath('train_data')
test_path = os.path.abspath('test_data')
db_path = os.path.abspath('./face_rec/data.db')
# db_path = ':memory:' # For testing purposes


def creation_date(path_to_file):
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime
def train(client, DB):
    exp = 'done=0'
    groups = DB.get('DISTINCT persongroup', 'train', exp)
    for group, in groups:
        client.train(group)
        DB.update('train', 'done=1', "persongroup='{}'".format(group))

def identify(test_path, client, DB):
    exp = 'done=0'
    to_detect = DB.get('DISTINCT file, persongroup','detect',exp)
    data = DB.get('azureid, name','person')
    id2name = {azureid: name for azureid,name in data}
    cols = '(appeared_at, azureid, name, temperature, file)' 
    for image_path, persongroup in to_detect:
        azureids, names = client.identify(image_path, persongroup, id2name)
        DB.update('detect', 'done=1', "file='{}'".format(image_path))
        if len(azureids) > 0:
            for azureid, name in azureids, names:
                vals = "('{}','{}','{}',{},'{}')".format(creation_date(image_path),
                                                           azureid, name, 33.3,
                                                           image_path)
                DB.insert('attendance', cols, vals)
        
        
         
def main():
    client = face_client(creds_path)
    client.clean_groups()
    DB = db_ops(db_path)
    
    data = DB.get('person', 'train', fetch = 'one') 
    
    if not data:
        client.train_metadeta_from_dir(train_path, DB)
        client.test_metadeta_from_dir(test_path, DB)
    else: 
        print("INFO: Metadata found")
    try:
        while True:
            
            train(client, DB)
            identify(test_path, client, DB)
    except KeyboardInterrupt:
        print("INFO: Exiting program")
        sys.exit()  
    
    DB.close()
if __name__=='__main__':
    main()