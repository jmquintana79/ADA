# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 09:16:41 2019

@author: admin
"""

from functions import clean_string
import stats
import numpy as np
import pandas as pd


    
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
        self.num_columns = self.df.select_dtypes(include=['float64']).columns.tolist()         # numerical columns
        self.cat_columns = self.df.select_dtypes(include=['object', 'int64']).columns.tolist() # categorical columns

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
    
    def num2cat_binning(self, name, nbins = 10):
        # create new column name
        name_new = name+'_cat%s'%nbins
        # get columnt instance
        Col = self.get_column(name)
        # type validation
        assert Col.type == 'numerical', 'only possible numerical columns.'
        # get data
        data_num = self.get_data(name)
        # calculate bins
        bins = np.linspace(np.min(data_num), np.max(data_num), nbins+1, endpoint=True)
        labels = np.arange(1,nbins+1,1)
        self.df[name_new] = pd.cut(data_num, bins = bins, labels = labels)
        # create a new column
        col = Column(name_new)
        col.type = 'categorical'
        setattr(self.columns, name_new, col)
        # save new column name
        self.cat_columns.append(name_new)
        
    
    def calculate_stats_num(self, name, per = [5,25,50,75,95]):
        # get columnt instance
        Col = self.get_column(name)
        # type validation
        assert Col.type == 'numerical', 'only possible numerical columns.'
        # get data
        data = self.get_data(name)
        # initialize
        dstats = dict()
        # calculate statistics
        dstats['mean'] = stats.mean(data)
        dstats['median'] = stats.median(data)
        dstats['std'] = stats.std(data)
        dstats['min'] = stats.min(data)
        dstats['max'] = stats.max(data)
        dstats['skew'] = stats.skew(data)
        dstats['kurtosis'] = stats.kurtosis(data)
        for ip in per:
            dstats['per%s'%ip] = stats.percentile(data, ip)
        # return
        Col.stats = dstats

    def calculate_stats_cat(self, name):
       # get columnt instance
        Col = self.get_column(name)
        # type validation
        assert Col.type == 'categorical', 'only possible categorical columns.'
        # get data
        data = self.get_data(name)
        # initialize
        dstats = dict()
        dstats['count'] = dict()
        dstats['probability'] = dict()
        
        # count categorical values
        cat, count = np.unique(data, return_index=False, return_inverse=False, return_counts=True, axis=None)
        for icat, icount in zip(cat, count):
            dstats['count'][icat] = icount
            dstats['probability'][icat] = icount / len(data)
        # set a new attributes with the cagories
        setattr(Col, 'categories', list(cat))
        # return
        Col.stats = dstats


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
        
    

