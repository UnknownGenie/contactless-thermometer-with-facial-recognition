# -*- coding: utf-8 -*-
"""
Created on Mon May 18 12:25:52 2020

@author: ME
"""

import sqlite3


class db_ops():
    def __init__(self, path):
        try:
            
            self.conn = sqlite3.connect(path, check_same_thread=False)
            self.c = self.conn.cursor()
            
            print("INFO: databse connection success")
            
            self.execute('SELECT SQLITE_VERSION()')
            data = self.c.fetchone()
            print('SQLite version:', data[0])
            
            self.execute('''CREATE TABLE IF NOT EXISTS train (
                            file TEXT NOT NULL,
                           	persongroup TEXT NOT NULL,
                         	person TEXT NOT NULL,
                            done INT NOT NULL DEFAULT 0
                        )''')
            
            self.execute('''CREATE TABLE IF NOT EXISTS detect (
                         	file TEXT NOT NULL,
                           	persongroup TEXT NOT NULL,
                         	done INT NOT NULL DEFAULT 0
                        )''')
            
            self.execute('''CREATE TABLE IF NOT EXISTS attendance (
                            appeared_at TEXT NOT NULL,        	
                            azureid TEXT NOT NULL,
                           	name TEXT NOT NULL,
                            temperature REAL NOT NULL,
                        	file TEXT NOT NULL
                        )''')
            
            self.execute('''CREATE TABLE IF NOT EXISTS person (
                         	name TEXT NOT NULL,
                           	azureid TEXT,
                         	contact TEXT,
                            persongroup TEXT,
                            CONSTRAINT id UNIQUE (azureid)
                        )''')
            print("Tables created/modiified")
                                 
        except sqlite3.Error as error:
            print("ERROR: ", error)
    
    def update(self, table, vals, expression=None):
        query =  "UPDATE {} SET {} WHERE {};".format(table, vals,
                                                    expression)
        self.execute(query)
        self.commit()
        print("INFO: Updated {}".format(table))
    def insert(self, table, cols, vals):
        query = 'INSERT INTO {} {} VALUES {};'.format(table,
                                                     str(cols),
                                                     str(vals))
        self.execute(query)
        self.commit()
        print("INFO: Inserted in {}".format(table))
    def get(self, cols, table, expression=None, fetch = 'all'):
        if expression:
            query = 'SELECT {} FROM {} WHERE {};'.format(cols, table, 
                                                        expression)
        else:
            query = 'SELECT {} FROM {}'.format(cols, table)
        self.execute(query)
        if fetch == 'all': return self.c.fetchall()
        elif fetch == 'one': return self.c.fetchone()
        
    def close(self):
        self.conn.close()
    
    def commit(self):
        self.conn.commit()
    
    def execute(self, query):
        try:
            self.c.execute(query)
        except sqlite3.Error as e:
            print("QUERY:{}".format(query))
            print("ERROR: query failed: {}".format(e))
        
        
        
        
        
        