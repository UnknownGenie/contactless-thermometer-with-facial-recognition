# -*- coding: utf-8 -*-
"""
Created on Thu May 21 21:58:15 2020

@author: ME
"""
import watchdog.events
import os

class Handler(watchdog.events.PatternMatchingEventHandler): 
    def __init__(self): 
        # Set the patterns for PatternMatchingEventHandler 
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.jpg'], 
                                                             ignore_directories=True, case_sensitive=False) 
        self.queue = list()
    def on_created(self, event): 
        try:
            parts = event.src_path.split(os.sep)
            # image_path = os.path.join(*parts)
            image_path = event.src_path
            
            if 'train_data' in event.src_path:
                person = parts[-2]
                persongroup = parts[-3]
                cols = '(file, persongroup, person)'
                vals = "('{}','{}','{}')".format(image_path,
                                              persongroup, person)
                self.queue.append(['train', cols, vals])
            
            elif 'test_data' in event.src_path:
                persongroup = parts[-2]
                cols = '(file, persongroup)'
                vals = "('{}','{}')".format(image_path, persongroup)
                self.queue.append(['detect', cols, vals])
        except Exception as e:
            print("ERROR: {}".format(e))