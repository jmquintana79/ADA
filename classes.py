#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 09:16:41 2019

@author: admin
"""

from functions import load_scikit_dataset, clean_string
    
class ADA:
    
    def __init__(self, df, depth = 'all'):
        self.df = df
        self.depth = depth
        #self.columns = dict()
        self.columns = Columns()
        
        # rename columns if it is necessary
        for name in self.df.columns:
            self.df.rename(columns={name: clean_string(name)}, inplace=True)
            
        # collect column names per type
        self.num_columns = self.df.select_dtypes(include=['float64']).columns.values         # numerical columns
        self.cat_columns = self.df.select_dtypes(include=['object', 'int64']).columns.values # categorical columns

        # create columns instances
        for name in self.df.columns:
            col = Column(name)
            col.type = 'num' if name in self.num_columns else 'cat'
            setattr(self.columns, name, col)
        
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
