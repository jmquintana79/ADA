#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 09:16:41 2019

@author: admin
"""

from functions import load_scikit_dataset
    
class ADA:
    
    def __init__(self, df, depth = 'all'):
        self.df = df
        self.depth = depth
        self.columns = dict()
        
        for col in self.df.columns:
            self.columns[col] = Column(col)
        
    def say_hi(self):
        print("Soy ADA",self.df.head())
        

    
class Column(ADA):
    def __init__(self, name):
        self.name = name
        
    
    def say_hi(self):
        print("Soy Column",self.df.head()) 

    
# %%

df = load_scikit_dataset()      
ada = ADA(df)
