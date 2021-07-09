# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 15:11:31 2021

@author: al-abiad

This script contains helper functions to be used in main code 

"""
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

def Find_jumps_using_peaks(array_dataframe=[],plot=True):
    """
    This functions detect the first highest peak at the begining of signal
    and the last highest peak at the end of the signal. Peaks are calculated using
    find_peaks function 
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html

    Parameters
    ----------
    array_dataframe : list, optional
        This is a list of dataframes where we need to calculate the peaks.
        Phone, Xsens, Gaitup

    Returns
    -------
    Jump_start : list of peaks at start of the signal
        
    Jump_end : list of peaks at end of the signal
        

    """
    print("detecting peak")
    Jump_start=[]
    Jump_stop=[]
    i=0
    plt.figure()
    for df in array_dataframe:
        print("dataframe %d"%i)
        i=i+1
        norm= calculate_norm(df)
        #distance are parameters to be tuned
        peaks, _ = find_peaks(norm, distance=1000)
        
        if len(peaks)>2:
            Jump_start.append(peaks[0])
            Jump_stop.append(peaks[-1])
            if plot==True:
                plt.title("dataframe%d"%(i))
                plt.plot(norm[peaks[0]:peaks[-1]],color='k')
        else:
            print("could not detect peaks correctly: check the parameters in find_peaks to be tuned")

    return Jump_start,Jump_stop

def gtom2s(dataframe):
    """
    Change unit of accelerometer signal into m/s^2
    """
    dataframe=dataframe.mul(9.8)
    return 

def rad2deg(dataframe):
    """
    Change unit of gyroscope signal into deg/sec
    """
    c=180/np.pi
    dataframe= dataframe.mul(c)
    return

def crop_signals(array_dataframe,Jump_start,Jump_end):
    """
    Crops the dataframes according to detected Jumps at begining and Jumps at the end

    Parameters
    ----------
    array_dataframe : list of dataframes
        lsit of IMU dataframes. The default is [].
    Jump_start : list of start jump indexes
        DESCRIPTION.
    Jump_end : list of end jump indexes
        DESCRIPTION.

    Returns
    -------
    cropped_dataframes : dataframes cropped according to jumps 
        DESCRIPTION.

    """
    print("cropping signals")
    if (len(array_dataframe)!=len(Jump_start)) or (len(array_dataframe)!=len(Jump_end)):
        print("the length of jumps array and number of dataframes is not the same")
        return [0]
    i=0
    cropped_dataframes=[]
    for df in array_dataframe:
        df=df.iloc[Jump_start[i]:Jump_end[i],:].copy()
        i=i+1
        cropped_dataframes.append(df)
        
    return cropped_dataframes
  
    
def calculate_norm(dataframe):
    """
    Takes IMU signal in form of a dataframe and calculates the euclidean norm
    and returns it as a numpy array

    Parameters
    ----------
    dataframe : pandas dataframe
        IMU signal dataframe

    Returns
    -------
    norm : numpy array
        The norm of the IMU signal

    """
    print("calculating norm of vector")
    
    matrix1=dataframe
    x=matrix1.iloc[:,0].values**2
    y=matrix1.iloc[:,1].values**2
    z=matrix1.iloc[:,2].values**2
    m=x+y+z
    norm=np.array([np.sqrt(i) for i in m])
    
    return norm
    
    
    
    
    
    
    
    
    
    
    
    