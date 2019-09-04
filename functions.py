#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 08:58:38 2019

@author: admin
"""
import pandas as pd

## load sample dataset from scikit-learn
def load_scikit_dataset(name:str = 'iris')->'df':
    """
    Load sample dataset from scikit-learn.
    name -- name of dataset to be loaded (default 'iris').
    return -- dataset in a df.
    """
    # import library function
    try:
        if name is 'iris':
            from sklearn.datasets import load_iris as dataset
    except Exception as e:
        print(str(e))
        return None
    # import data
    data = dataset()
    # store in a df
    df = pd.DataFrame(data.data, columns = data.feature_names)
    df['target'] = [ data.target_names[i] for i in data.target]
    # return    
    return df

## clean a string (remove symbols)
def clean_string(string:str)->str:
    """
    Clean a string removing symbols, capitalize each word and join.
    string -- string to be cleaned.
    return -- cleaned string.
    """
    string_cleaned = string.translate(str.maketrans(' ', ' ', '!"“”#$%&\'()*+/:;<=>?@[\\]^_`{|}~'))
    return ''.join([i.capitalize() for i in string_cleaned.split(' ')])
 