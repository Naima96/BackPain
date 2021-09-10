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

DATA,NAME,FREQ,ETIQUETTE,ind_a_tracer=importation(dossier,exceptions) #Ici s'importe les données sous la forme s'un DataFrame pandas
plot_signaux(DATA,ind_a_tracer,ETIQUETTE,dossier) #Ici s'affichent les 3 accélérations et 3 vitesses de rotations des 3 XSens 

#Test GITHUB Sacha