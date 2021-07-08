# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 17:45:12 2021

@author: al-abiad
"""

from CPclass import phone as CP
from Python_G_to_sec import main 
import matplotlib.pyplot as plt
import numpy as np

def Calculate_vector_Magnitude(Act_count_phone):

    x=Act_count_phone['axis1'].values**2
    y=Act_count_phone['axis2'].values**2
    z=Act_count_phone['axis3'].values**2
    m=x+y+z
    mm=np.array([np.sqrt(i) for i in m])
    
    return mm

#cooking
path="d:\\Users\\al-abiad\\Desktop\\back_pain_mathilde\\23_06_21_Alex\\telephone\\v5_20210623_173550_738s.csv"

#cooking
path="d:\\Users\\al-abiad\\Desktop\\back_pain_mathilde\\23_06_21_Alex\\telephone\\v5_20210623_175022_667s.csv"

#doing dishes
path="d:\\Users\\al-abiad\\Desktop\\back_pain_mathilde\\23_06_21_Alex\\telephone\\v5_20210623_180533_768s.csv"

#cleaning
path="d:\\Users\\al-abiad\\Desktop\\back_pain_mathilde\\23_06_21_Alex\\telephone\\v5_20210623_182346_592s.csv"

#eating
path="d:\\Users\\al-abiad\\Desktop\\back_pain_mathilde\\23_06_21_Alex\\telephone\\v5_20210623_183409_722s.csv"

#sleeping + toilet
path="d:\\Users\\al-abiad\\Desktop\\back_pain_mathilde\\23_06_21_Alex\\telephone\\v5_20210623_185441_571s.csv"


CP_data=CP(path,app="sensor play")

rawacc=CP_data.acc_rawdata
rawgyro=CP_data.gyro_rawdata
# plt.plot(rawacc)


CP_data.interpolategyrnacc(fs=30)

acc_interp=CP_data.acc_interp
gyro_interp=CP_data.gyro_interp

plt.plot(acc_interp)

acc_interp_renamed=acc_interp.rename(columns = {'accelX(g)': 'Accx', 'accelY(g)': 'Accy','accelZ(g)':'Accz'}, inplace = False)

Act_count_phone=main(acc_interp_renamed)

# plt.plot(Act_count_phone)

vector_Magnitude=Calculate_vector_Magnitude(Act_count_phone)

# plt.plot(vector_Magnitude)

#where total activity >10
phone_total_activity= np.sum(vector_Magnitude>10)
print("the total activity recorded by the phone is %d"%phone_total_activity)




# CP_data.calculate_norm_accandgyro(gyro=CP_data.gyro_interp,acc=CP_data.acc_interp)


