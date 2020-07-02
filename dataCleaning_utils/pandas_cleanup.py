#   @@@@@@@@@@@@@@@@@@@@@@@@
#   **Code by Aron Talai****
#   @@@@@@@@@@@@@@@@@@@@@@@@


# various pandas based data cleaning tools

# def libs
import os
import math 
import numpy as np
import pandas as pd
from collections import Counter 


# init 
list_of_columns = ['Edition Statement','Corporate Author','Corporate Contributors',
            'Former owner','Engraver','Contributors',
            'Issuance type','Shelfmarks']

# def func
def drop_unrelated_columns(data, list_of_columns):
    '''drops unrelated columns from a pandas dataframe
    list_of_columns is a list of header names to be droped'''
    return data.drop(list_of_columns, axis=1)

def rename_columns(data, dict_of_names):
    '''renames columns to other names contained in the dict_of_names
    parameter.
    example: {'old_name1': 'new_name1','old_name2': 'new_name2'}'''
    return data.rename(columns = dict_of_names)

def apply_func(data, input_function):
    '''applies input fucntion on the entire dataset
    example: 
    def input_function(item):
        if ' (' in item:
            return item[:item.find(' (')]
        elif '[' in item:
            return item[:item.find('[')]
        else: 
            return item
            '''
    return data.applymap(input_function)

def find_nan_columns(data):
    '''return a list of nan  values in each dataframe column'''
    null_columns = data.columns[data.isnull().any()]
    nan_vals = data[null_columns].isnull().sum()
    return null_columns, nan_vals

def drop_known_nan(data, columns):
    '''drops rows with missing values that pandas understands'''
    print ('Old data had a length of', len(data))
    new_data = data.dropna(subset = columns)
    print ('New data has a length of:', len(new_data))
    return new_data

def drop_all_nan(data):
    '''automatically detects rows with nan values and drops them'''
    columns_with_nans = [i for i in find_nan_columns(data)[0]]
    data = drop_known_nan(data, columns_with_nans)
    return data

def define_nan(path_to_data, nan_list):
    '''considers all in nan_list to be real nans from pandas perspective'''
    data = pd.read_csv(path_to_data, na_values = nan_list)
    return data

def replace_missing_val(data, column_name):
    '''helper function'''
    # Replace missing values with a number
    data[column_name].fillna(125, inplace=True)

    # Location based replacement
    data.loc[2,column_name] = 125

    # Replace using median 
    median = data[column_name].median()
    data[column_name].fillna(median, inplace=True)

def remove_outlier(data, dist_num):
    '''removes outliers from each column of a pandas dataframe
    automatically excludes categorical cells and columns'''
    for clms in data.columns:
        try:
            mean = data[clms].mean()
            std = data[clms].std()
            data = data[(data[clms] < mean + dist_num*std) & (data[clms] > mean - dist_num*std)]
        #pass on categorical data
        except:
            pass 

    return data

def make_balanced_dataset(input_df, class_size):
	''' make a balanced dataset of binary labels given class_size and generate independent train and validation datasets
	input1: input dataframe where the format is data_label, content and the column names are label and text
	input2: class size is the number of training cases for each category
	output: shuffeled pandas dataframe for train and validation'''

	# get list of unique labels in dataframe
	label_count = []
	labels = input_df.label.unique()
	for label in labels:
		input_df_temp = input_df[input_df['label'] == label]
		label_count.append([label, len(input_df_temp)])

	# make a balanced training data set 
	minority_label = sorted(label_count, key = lambda x:x[1])[0]
	majority_label = sorted(label_count, key = lambda x:x[1])[1]

	if class_size > int(minority_label[1]):
		print ('Class size should be lower than minority class size!')
		raise ValueError 
		os.abort()

	temp_data = input_df[input_df['label'] == str(minority_label[0])]
	minority_df = temp_data.sample(frac=1)
	minority_df_train = minority_df.head(class_size)
	minority_df_val = minority_df.tail(len(minority_df) - class_size)


	temp_data = input_df[input_df['label'] == str(majority_label[0])]
	majority_df = temp_data.sample(frac=1)
	majority_df_train = majority_df.head(class_size)
	majority_df_val = majority_df.tail(len(majority_df) - class_size)


	frames = [minority_df_train, majority_df_train]
	merged_df = pd.concat(frames)
	merged_df = merged_df.sample(frac=1)
	merged_train = merged_df.reset_index()

	frames = [minority_df_val, majority_df_val]
	merged_df = pd.concat(frames)
	merged_df = merged_df.sample(frac=1)
	merged_val = merged_df.reset_index()


	return merged_train, merged_val
