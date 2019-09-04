#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 09:16:41 2019

@author: admin
"""

from functions import load_scikit_dataset, clean_string
import numpy as np
from scipy.stats import kurtosis, skew

    
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
            col.type = 'numerical' if name in self.num_columns else 'categorical'
            setattr(self.columns, name, col)
        
    def get_column_names(self):
        return list(self.columns.__dict__.keys())
        
    def get_column(self, name):
        return getattr(self.columns, name)
    
    def get_data(self, names:'str or list'):
        return self.df[names].values
    
    def calculate_stats_num(self, name, per = [5,25,50,75,95]):
        # get columnt instance
        Col = self.get_column(name)
        # type validation
        assert Col.type == 'numerical', 'only possible numerical columns.'
        # get data
        data = self.get_data(name)
        # initialize
        stats = dict()
        # calculate statistics
        stats['mean'] = np.mean(data)
        stats['median'] = np.median(data)
        stats['std'] = np.std(data)
        stats['min'] = np.min(data)
        stats['max'] = np.max(data)
        stats['skew'] = skew(data)
        stats['kurtosis'] = kurtosis(data)
        for ip in per:
            stats['per%s'%ip] = np.percentile(data, ip)
        # return
        Col.stats = stats


class Columns():
    pass

        
    
class Column():
    def __init__(self, name):
        self.name = name
        self.type = None
        self.stats = None
        
    def __str__(self):
        print('\n"%s" (%s)'%(self.name, self.type))
        print('Stats:')
        for k,v in self.stats.items():
            print('\t%s = %s'%(k,v))
        return '\n'
        
    



    
# %%

df = load_scikit_dataset()      
ada = ADA(df)
