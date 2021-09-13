# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 14:16:14 2021

@author: guitteny
"""

from NBC_fonctions import *
import Fonction_utiles as Fu
import numpy as np
from numpy import matlib as mb
from scipy import *

# #Creation dataframe des etats des vidéos décrits par Mathilde - sampled to 1Hz
fichier = "Etats_S2_RE_1.xlsx"

Etat= pd.read_excel(fichier,sheet_name=0)


Etat_new = pd.DataFrame({'Time': [c for c in range(1,Etat.iloc[len(Etat)-1,0]+1)], 'Etat': [c for c in range(1,Etat.iloc[len(Etat)-1,0]+1)]})
prev_time = 0 #initialisation
for i, row in Etat.iterrows():
    itime = row["Temps (en s)"]
    ietat = row["Etat"]
    Etat_new.iloc[prev_time:itime,1]=ietat
    prev_time = itime
    


#Enregistrement des DataFrame des états_vidéo décrit par Mathilde
with pd.ExcelWriter(fichier[0:len(fichier)-5]+'_resampled.xlsx') as writer:
    Etat_new.to_excel(writer,sheet_name=fichier[6:8])
