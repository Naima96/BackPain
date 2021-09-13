# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 11:35:55 2021

@author: Jules
"""

from NBC_fonctions import *
import os
# =============================================================================
# VOICI QUELQUES LIGNES DE CODE POUR IMPORTER ET AFFICHER LES SIGANUX DES XSENS
# =============================================================================

# 1°) Renseigner le nom de l'experience à importer dans la variable 'dossier' (ex : dossier='S1_CU_2')

dossier=os.getcwd()+'\\Data_S1\\S1_ME_1'

# 2°) Si jamais certains fichiers sont corrompus et ne doivent pas être lus, renseigner le nom du fichier dans la liste  'execptions' 
#exceptions=['S1_CU_2-341106.txt']
exceptions=["S1_ME_1_gaitupraw.BIN","S1_ME_1_phone.csv"]

DATA,NAME,FREQ,ETIQUETTE,ind_a_tracer=importation(dossier,exceptions) #Ici s'importe les données sous la forme d'une liste de DataFrames pandas
#plot_signaux(DATA,ind_a_tracer,ETIQUETTE,dossier) #Ici s'affichent les 3 accélérations et 3 vitesses de rotations des 3 XSens 


# Remove data before and after the jump
[Jump_start,Jump_end] = Fu.Find_jumps_using_peaks(DATA)
Cropped_DATA = Fu.crop_signals(DATA,Jump_start,Jump_end)

#Affichage signaux rempli et coupés aux sauts
plot_signaux_v2(Cropped_DATA,ind_a_tracer,ETIQUETTE,dossier)


#Enregistrement des dataframe cropped dans un fichier excel
capteur_nb = 0
with pd.ExcelWriter(dossier+'.xlsx') as writer:  
    for df in Cropped_DATA:
        num_ID = int(NAME[capteur_nb][13])
        if num_ID==6 or num_ID==5:
            sensor_loc = 'Hanche droite'
        if num_ID==3 or num_ID==4:
            sensor_loc = 'Poignet droit'
        if num_ID==2 or num_ID==7:
            sensor_loc = 'Cuisse droite'  
        df.to_excel(writer,sheet_name=sensor_loc+str(num_ID))
        capteur_nb+=1