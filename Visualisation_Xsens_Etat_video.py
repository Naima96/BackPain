# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 14:19:01 2021

@author: guitteny
"""

from NBC_fonctions import *
import Fonction_utiles as Fu
import numpy as np
from numpy import matlib as mb
from scipy import *

# Import seaborn
import seaborn as sns

# Apply the default theme
sns.set_theme()

dossier='S1_RE_1'
ind_a_tracer=[1,3,5]
ETIQUETTE = ['Poignet droit', 'Hanche droite', 'Cuisse droite']

# Récupération liste de data frames à partir du fichier excel
X_sens = pd.read_excel("Data X_sens/"+dossier+"/"+dossier+'.xlsx',sheet_name=None)
X_sens =list(X_sens.values())

for i in range(6):
    X_sens[i].columns = ['Time', 'Acc_X', 'Acc_Y','Acc_Z','Gyr_X','Gyr_Y','Gyr_Z']


#Récupération des DataFrame des états_vidéo décrit par Mathilde transformée à 1Hz
etats = pd.read_excel('Etats video/Etats_'+dossier+'.xlsx')
    
# #Visualisation finale avec etats en couleur 

#plot_signaux_v3(X_sens,ind_a_tracer,ETIQUETTE,dossier,etats)

#Utilisation de seaborn pour visualisation:
df_poignet = X_sens[1].melt('Time')
df_poignet['type']=[i.split('_')[0] for i in df_poignet.variable]
df_poignet['direction']=[i.split('_')[-1] for i in df_poignet.variable]
df_poignet['capteur']=['Poignet' for i in df_poignet.variable]

df_hanche = X_sens[3].melt('Time')
df_hanche['type']=[i.split('_')[0] for i in df_hanche.variable]
df_hanche['direction']=[i.split('_')[-1] for i in df_hanche.variable]
df_hanche['capteur']=['Hanche' for i in df_hanche.variable]

df_cuisse = X_sens[5].melt('Time')
df_cuisse['type']=[i.split('_')[0] for i in df_cuisse.variable]
df_cuisse['direction']=[i.split('_')[-1] for i in df_cuisse.variable]
df_cuisse['capteur']=['Cuisse' for i in df_cuisse.variable]

frames = [df_poignet, df_hanche,df_cuisse]

df = pd.concat(frames)


# # # Create a visualization
g1 = sns.relplot(
     data=df,
     x="Time", y="value", col='type', row ='capteur',kind='line',
     hue="direction")
         

axes = g1.fig.axes
for c in range(6):
    imin=0
    for t, row in etats.iterrows():
            itime = row["Temps (en s)"]
            ietat = row["Etat"]
            if ietat == 'de_dyn':
                color = 'r'
            if ietat == 'de_stat_sup_dyn':
                color = 'm'
            if ietat == 'as':
                color = 'g'
            if ietat == 'al':
                color='b'
            axes[c].axvspan(imin,itime, facecolor=color, alpha=0.5)
            imin=itime

g1.fig.suptitle(dossier,fontsize=24, fontdict={"weight": "bold"})