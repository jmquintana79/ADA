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
        #self.columns = dict()
        self.columns = Columns()
        
        for name in self.df.columns:
            name_modif = name.replace(' ', '_')
            self.df.rename(columns={name: name_modif}, inplace=True)
            col = Column(name_modif)
            col.type = self.df.dtypes.to_dict()[name_modif] 
            setattr(self.columns, name_modif, col)
        
    def get_column_names(self):
        return list(self.columns.__dict__.keys())
        
    def get_column_data(self, name):
        return self.df[name].tolist()
      
        
class Columns():
    pass

        
    
class Column():
    def __init__(self, name):
        self.name = name
        self.type = None
        
    def say_hi(self):
        print("Soy Column",self.df.head()) 

    
# %%

df = load_scikit_dataset()      
ada = ADA(df)
