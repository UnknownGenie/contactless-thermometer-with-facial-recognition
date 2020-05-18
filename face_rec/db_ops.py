# -*- coding: utf-8 -*-
"""
Created on Mon May 18 12:25:52 2020

@author: ME
"""

import sqlite3

conn = sqlite3.connect('data.db')

c = conn.cursor()

c.execute('''CREATE TABLE stocks
             (date text, trans text, symbol text, qty real, price real)''')