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
from Python_G_to_sec import main

def Find_jumps_using_peaks(array_dataframe=[],plot=False):
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
    
    for df in array_dataframe:
        plt.figure()
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


    
def caclulate_activity_count(dataframes=[],sampling_freq=70):
    
    print("Calculating activity count")
    Act_counts=[]
    for df in dataframes:
        df=df.rename(columns = {'Acc_X': 'Accx', 'Acc_Y': 'Accy',
                                              'Acc_Z':'Accz'}, inplace = False)
        
        
        Act_count=main(df,filesf=sampling_freq)
        
        Act_counts.append(Act_count)
    
    return(Act_counts)


def Split_into_Acc_Gyr(dataframes=[]):
    
    print("splitting the dataframes into acc dataframe and gyro dataframe")
    
    Acc=[]
    Gyro=[]
    for df in dataframes:
        df_Gyro=df[df.columns[3:]]
        df_Acc=df[df.columns[0:3]]
        Acc.append(df_Acc)
        Gyro.append(df_Gyro)
        
    return(Acc,Gyro)


    
    
def Calculate_vector_Magnitude(dataframes):
    print("calculating vector magnitude")
    
    Vect_mag=[]
    
    for df in dataframes:
        x=df['axis1'].values**2
        y=df['axis2'].values**2
        z=df['axis3'].values**2
        m=x+y+z
        mm=np.array([np.sqrt(i) for i in m])
        
        Vect_mag.append(mm)
        
    
    return Vect_mag
    
    
        
        
def plot_Vector_Magnitude(DATA,ind_a_tracer,ETIQUETTE,dossier,etats):

    k=0
    fig=plt.figure()
    fig, axe=plt.subplots(3,1,sharex=True)
    fig.tight_layout()
    fig.suptitle(f"{dossier}", fontsize=15)
    
    for i in ind_a_tracer:
        data=DATA[i]    
        #plt.subplot(3,2,2*k+1)
        
        axe[k].plot(data,label='Vect_Mag')
        
        # axe[0,0].legend()
        # axe[0,0].legend(bbox_to_anchor=(1,1), loc='right', fontsize=10)
        
        axe[k].set_title(ETIQUETTE[k]+'_Act_Count')
        axe[1].set_ylabel("Count",fontsize=10)
        axe[2].set_xlabel("Temps (s)")
        imin=0
        nr=0
        nm=0
        ng=0
        nb=0
        
        for i, row in etats.iterrows():
            itime = row["Temps (en s)"]
            ietat = row["Etat"]
            
            if ietat == 'de_dyn':
                color = 'r'
                axe[k].axvspan(imin,itime,label = "_"*(nr)+ietat, facecolor=color, alpha=0.5)

                nr=1
                
            if ietat == 'de_stat_sup_dyn':
                color = 'm'
                axe[k].axvspan(imin,itime,label = "_"*(nm)+ietat, facecolor=color, alpha=0.5)
                nm=1
                
            if ietat == 'as':
                color = 'g'
                axe[k].axvspan(imin,itime,label = "_"*(ng)+ietat, facecolor=color, alpha=0.5)

                ng=1
                
            if ietat == 'al':
                color='b'
                
                axe[k].axvspan(imin,itime,label = "_"*(nb)+ietat, facecolor=color, alpha=0.5)

                nb=1
            
            imin=itime
        
        k=k+1
        
        plt.legend()
        
        
        
    print(f"Signaux de {len(ind_a_tracer)} capteurs affichés avec succès")       

    
    
    

   
   
    
    
    
    
    
    
    
    
    
    
    
    
    