# -*- coding: utf-8 -*-
"""
Created on Wed May 26 11:17:38 2021

@author: Jules
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from os import listdir
import shutil
import copy
from sklearn.impute import SimpleImputer

#hiii mathberger was here
def importer_data(name,path):

    data=pd.read_csv(f"{path}/{name}", sep=':')
    freq=int(data[' 0'][0][1:len(data[' 0'][0])-4])
    data=pd.read_csv(f'{path}/{name}')
    data=data.iloc[3:len(data)-2,0]
    data=data.str.split("\t")
    file=data.to_list()

    data=pd.DataFrame(file)
    name=data.iloc[0,:8].to_list()[1:len(data.iloc[0,:8].to_list())-1]
    data=data.iloc[1:,:]
    data.iloc[:,0]=np.linspace(0,data.shape[0]/freq,data.shape[0])
    data.set_index(data[0],drop=True, inplace=True)
    data=data.iloc[:,1:7]
    
    data.columns=name
    data.replace('', np.nan, inplace=True)
    imputer=SimpleImputer(missing_values=np.nan,strategy='mean')
    imputer.fit_transform(data)
    data=pd.DataFrame(data,dtype=np.float64)
    
    return(data,freq)
    
def egalisation(DATA,FREQ):
    
    #FONCTION QUI MET TOUT LES TABLEAUX D'UNE MEME ACQUISITION A LA MEME LONGUEUR
    #FONCTION QUI REINDEX LES TABLEAUX AVEC EXACTEMENT LE MEME VECTEUR DE TEMPS i.e. : permet ensuite la fusion sans décalage
    id_min=np.argmin([len(DATA[i]) for i in range(len(DATA))])

    for k in range(len(DATA)):
        periode=1/FREQ[k]
        ind=np.linspace(0,len(DATA[id_min])*periode,len(DATA[id_min]))
        DATA[k]=DATA[k].iloc[:len(DATA[id_min]),:]
        DATA[k].index=ind
    return(DATA)
    
"""
def cadrage(data,t1,t2):
    
    ind1=np.argmin(abs(data.index-t1))
    ind2=np.argmin(abs(data.index-t2))
    
    vitesse=data.iloc[ind1:ind2,0].tolist()
    delta=data.iloc[ind1:ind2,1]
    
    data_delta=pd.DataFrame(delta)
    idx=data.index[ind1:ind2]
    data=pd.DataFrame(vitesse,index=idx)
    
    data=pd.concat([data,data_delta],axis=1)
    
    data.columns=['vitesse','delta']
    
        
    return(data)
"""

def importation(dossier,exceptions):
    ##edited by naima.. changed method to import files 
    dirs = listdir(dossier)

    DATA=[]
    FREQ=[]
    NAME=[]
    ETIQUETTE=[]
    ind_a_tracer=[]
    
    dirs=[f for f in dirs if f not in exceptions]

    for file in dirs:
        Data=importer_data(file,dossier)
        NAME.append(file)
        DATA.append(Data[0])
        FREQ.append(Data[1])
                
    DATA=egalisation(DATA,FREQ)
    num_ID=[int(NAME[i][13]) for i in range(len(dirs))]

    i=0
    for num in num_ID :
        if num%2==1:
            ind_a_tracer.append(i)
            
            if num==6 or num==5:
                ETIQUETTE.append('Hanche droite')
            if num==3 or num==4:
                ETIQUETTE.append('Poignet droit')
            if num==2 or num==7:
                ETIQUETTE.append('Cuisse droite')
        i+=1
    print(f"{len(DATA)} fichiers importés avec succès")
    
    return(DATA,NAME,FREQ,ETIQUETTE,ind_a_tracer)
    

def plot_signaux(DATA,ind_a_tracer,ETIQUETTE,dossier):

    k=0
    fig=plt.figure()
    fig.suptitle(f"{dossier}", fontsize=25)
    
    for i in ind_a_tracer:
        data=DATA[i]    
        plt.subplot(3,1,1+k)
        plt.plot(data['Acc_X'],label='Acc_X')
        plt.plot(data['Acc_Y'],label='Acc_Y')
        plt.plot(data['Acc_Z'],label='Acc_Z')
        plt.plot(data['Gyr_X'],label='Gyr_X')
        plt.plot(data['Gyr_Y'],label='Gyr_Y')
        plt.plot(data['Gyr_Z'],label='Gyr_Z')
    
        plt.legend()
        plt.grid()
        plt.title(f"{ETIQUETTE[k]}")
        plt.ylabel("$Acc (m.s^-2)$ / $Gyr (rad.s^-2$)")
        plt.xlabel("Temps (s)")
        plt.legend(bbox_to_anchor=(1,1), loc='right',)
    
        
        k+=1
    print(f"Signaux de {len(ind_a_tracer)} capteurs affichés avec succès")
    
    
    
if __name__=="__main__":
    plt.close('all')
    
    