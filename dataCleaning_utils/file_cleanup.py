#   @@@@@@@@@@@@@@@@@@@@@@@@
#   ***Code by Aron Talai***
#   @@@@@@@@@@@@@@@@@@@@@@@@


#Delete files with strange names in a given directory 


# def libs
import os
import pickle
import pandas as pd  
from os import listdir
from os.path import isfile, join
from random import randint
from pathlib import Path
from random import shuffle
from tqdm import tqdm

sentiment_list = ['list of files with words that makes them candidates for deleting']

def cleanup_dir(MAIN_PATH, path_to_store, csv_name):

    current_dir = [f.split('_')[0] for f in os.listdir(MAIN_PATH)]
    empty_list = []

    for k in range(0,len(current_dir)):

        result = ''.join(i for i in str(current_dir[k]) if not i.isdigit())
        empty_list.append(result.replace('-',''))

    empty_list = sorted(list(set(empty_list)))
    current_dir = pd.DataFrame(empty_list)
    current_dir.to_csv(os.path.join(path_to_store, csv_name), sep = ',', index = False)

def delete_files_with_sentiment(MAIN_PATH,sentiment_list):
    """Deletes specific files that have words given in the passed list"""

    all_files = [f for f in os.listdir(MAIN_PATH)]
    bad_files_count = 0

    for current_file in range(0,len(all_files)):

        for i in range(0,len(sentiment_list)):

            if sentiment_list[i] in all_files[current_file]:

                try:

                    os.remove(MAIN_PATH + str(all_files[current_file]))
                    bad_files_count += 1

                except:
                    pass

    print (bad_files_count,'files were deleted due to tags indicating suboptimal signal quality!')

def random_file_deletion(MAIN_PATH,num_of_files_to_keep):
    """ Randomly deletes files a user specified number of
    data in a given directory"""

    all_files = [f for f in os.listdir(MAIN_PATH) if f.endswith('.npy')]
    shuffle(all_files)
    num_of_files_to_delete = len(all_files) - int(num_of_files_to_keep)

    file_counter = 0

    while file_counter < num_of_files_to_delete:
        
        index = randint(0, len(all_files)-1)

        try:

            os.remove(MAIN_PATH + all_files[index])
            file_counter += 1

        except:
            pass

def delete_null_file(MAIN_PATH): 
    """ Deletes potential null numpy files in a given directory"""

    files = [f for f in os.listdir(MAIN_PATH) if f.endswith('.npy')]

    for i in tqdm(range(0,len(files))):
        data = np.load(MAIN_PATH + files[i])
        if np.isnan(data).any():
            os.remove(MAIN_PATH + files[i])
            print ('Trivial Warning: We detected some null files!')

def list_of_files(MAIN_PATH,CSV_NAME,SAVING_PATH):
    """ Returns a csv list of all the existing files in a given directory
    and stores them in SAVING_PATH directory"""

    files = [f for f in os.listdir(MAIN_PATH)]
    files = pd.DataFrame(files)
    files.to_csv(SAVING_PATH + '{}.csv'.format(CSV_NAME), sep = ',', index = False)
