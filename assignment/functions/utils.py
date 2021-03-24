# Utility functions for processing .csv data in assignment 6
import numpy as np
import pandas as pd
import os
import natsort
import glob

# get_files function:
def get_files(pattern):
    #Get files in alphanumerical order that match the pattern I provided
    if isinstance(pattern, list):
        pattern = os.path.join(*pattern)

    files = natsort.natsorted(glob.glob(pattern))


    return files

# find_middle function:
def find_middle(in_column):
    """""Find middle index
    Args:
        in_column ([type]): [array or dataframe column]
    """""
    
    middle = float(len(in_column))/2
    return int(np.floor(middle)) 

#realign to peak or center function
def realign_data(in_data, align='max'):
    """Center data around center of shortest column
    Args:
        in_data: array of input data
        align (str): "max" or "center"
    
    Returns: 
        d - new dataframe with realigned data
        shifts - how each entry was shifted
    """
    x, y = in_data.shape
    d = pd.DataFrame(0, index=np.arange(x), columns=np.arange(y))
    shifts = np.zeros(y)

    #find longest length
    ind_longest = np.argmin((in_data == 0).astype(int).sum(axis=0).values)
    #find the peak index of the longest column
    peak_longest = np.argmax(in_data.loc[:, ind_longest].values)
    #use find_middle function to find the center point of the longest column
    mid_longest = find_middle(in_data.index[in_data[ind_longest]!=0].values)
    
    for column in in_data:
        if align == 'max':
            peak = np.argmax(in_data[column].values)
            pdiff = peak_longest - peak
            d[column] = in_data[column].shift(periods=pdiff, fill_value=0)
            shifts[column] = pdiff
        elif align == 'center':
            # Write the alignment code here, replacing peak with the center that you found (mid_longest). 
            center = find_middle(in_data.index[in_data[column]!=0].values)
            cdiff = mid_longest - center
            d[column] = in_data[column].shift(periods=cdiff, fill_value=0)
            shifts[column] = cdiff
            
    return d, shifts

