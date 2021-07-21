# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 00:10:07 2021

@author: swd7788
"""

from pymongo import MongoClient
import datetime

#url='mongodb://localhost:27017/'

class database_operations:
    def __init__(self,url):
        
        self.url=url

    def create_connection(self):
        self.client = MongoClient(self.url)
        return self.client

    def connect_database(self):       

        self.mydb = self.client ['bottle_detection_database_1']
        my_collection = self.mydb['correct_detection']
        return self.mydb
    
    def find_data(self):
        data=list(self.mydb.mytable.find())
        return data

    def insert_data(self,insert_data):
        record_id2 = self.mydb.mytable.insert_one(insert_data)


# a=database_operations(url)
# a.create_connection()
# a.connect_database()
# print(a.find_data())
