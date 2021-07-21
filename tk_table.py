# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 00:46:22 2021

@author: swd7788
"""

import tkinter as tk
from tkinter import ttk

class data:
    
    def __init__(self,data_temp):
        self.data_temp=data_temp
        
        scores = tk.Tk() 
        label = tk.Label(scores, text="Detection Dashboard", font=("Arial",30)).grid(row=0, columnspan=1)
        # create Treeview with 3 columns
        
        
        # obj=data(data_temp)    
        cols = ("ID",'SKU_ID', 'UNIT_ID', 'STATUS',"TIMESTAMP")
        listBox = ttk.Treeview(scores, columns=cols, show='headings')
        # set column headings
        for col in cols:
            listBox.heading(col, text=col)    
        listBox.grid(row=1, column=1, columnspan=2)
        
        tempList=[]
        
        one_time_flag=0
        
        if one_time_flag!=1:
        
            for j in self.data_temp:
                tempList.append([j.get("sku_id"),j.get("Unit_id"),j.get("status"),j.get("timestamp")])
                
            tempList.sort(key=lambda e: e[1], reverse=False)
        
            for i, (name, score,status,timestamp) in enumerate(tempList, start=1):
                listBox.insert("", "end", values=(i, name, score,status,timestamp))

            one_time_flag=1
            
        # obj.show_data(listBox)
        # showScores = tk.Button(scores, text="Show more", width=15, command=obj.show_data).grid(row=4, column=0)
        # closeButton = tk.Button(scores, text="Close", width=15, command=exit).grid(row=4, column=1)
        
        
        scores.mainloop()


    # def show(self,tempList):
    #     tempList=self.temp
    
    #     # tempList = [['Jim', '0.33'], ['Dave', '0.67'], ['James', '0.67'], ['Eden', '0.5']]
    #     tempList.sort(key=lambda e: e[1], reverse=True)
    
    #     for i, (name, score) in enumerate(tempList, start=1):
            # listBox.insert("", "end", values=(i, name, score))
    def show_data(self,listbox):
        tempList=[]
        
        for j in self.data_temp:
            tempList.append([j.get("sku_id"),j.get("Unit_id"),j.get("status"),j.get("timestamp")])
            
        tempList.sort(key=lambda e: e[1], reverse=True)
    
        for i, (name, score,status,timestamp) in enumerate(tempList, start=1):
            listBox.insert("", "end", values=(i, name, score,status,timestamp))




   
        
# data_temp=[{'sku_id': '1', 'Unit_id': 'u1', 'status': 'Good', 'timestamp': '2021-07-22 00:02:01.186872'},{'sku_id': '1', 'Unit_id': 'u1', 'status': 'Good', 'timestamp': '2021-07-22 00:02:01.186872'},{'sku_id': '1', 'Unit_id': 'u1', 'status': 'Good', 'timestamp': '2021-07-22 00:02:01.186872'}
# ,{'sku_id': '1', 'Unit_id': 'u1', 'status': 'Good', 'timestamp': '2021-07-22 00:02:01.186872'}]

        
