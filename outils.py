#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import logging
from parametres import Parametres
from erreurs import *

def dictionnaire_csv(chemin_fichier):
    """Créé un DictReader à partir du fichier csv et d'une liste de 
    délimiteurs. Renvoie le dictionnaire ainsi que le fichier ouvert avec une
    ligne consommée"""
    for delim in Parametres.delimiteurs_fichier:
        fichier = open(chemin_fichier)

        donnees = csv.DictReader(fichier, delimiter=delim)
        for donnee in donnees:
            if len(donnee) <= 1: #Le fichier ne contient qu'une seule colonne, on passe au délimiteur suivant
                continue
            fichier.seek(0) #On réinitialise l'offset du fichier
            fichier.readline()
            return (donnees, fichier)

       
    raise FormatDeFichierNonReconnu(chemin_fichier)


def afficher_log(chemin, message, format=logging.Formatter('%(asctime)s %(levelname)s %(message)s'), niveau=logging.INFO, affichage=True):
    """Permet d'afficher un message et de l'écrire dans un fichier de log dont
    le chemin est spécifié"""
    infoLog = logging.FileHandler(chemin)
    infoLog.setFormatter(format)
    logger = logging.getLogger(chemin)
    logger.setLevel(niveau)

    if not logger.handlers:
        logger.addHandler(infoLog)
        if (niveau == logging.INFO):
            logger.info(message)
        if (niveau == logging.ERROR):
            logger.error(message)
        if (niveau == logging.WARNING):
            logger.warning(message)

    infoLog.close()
    logger.removeHandler(infoLog)
    if affichage:
        print(message)
        
def compter_colonnes(nom, data, fichier):
        """Compte le nombre de colonne de la forme nom+i avec i un entier
        dans un fichier csv et remet l'offset à 0"""
        res = 0
        try:
            for d in data:
                for i in range(1, len(d)+1):
                    d[nom+str(i)]
                    res += 1
                break 
        except:
            fichier.seek(0)
            return res
        fichier.seek(0)
        return res

def lire_entier_colonnes_multiples(nom, ligne):
    """Renvoie la liste des entiers contenus dans les colonnes de la forme 
    nom+i ou i est un entier. ligne doit être une ligne obtenu à partir d'un
    DictReader. Renvoie une liste vide si les colonnes sont inexistantes"""
    res = []
    try:
        for i in range(1, len(ligne)+1):
            elt = ligne[nom+str(i)]
            if elt == '':
                continue
            res.append(int(elt))
    except:
        return res
    return res

def lire_texte_colonnes_multiples(nom, ligne):
    """Renvoie la liste des entiers contenus dans les colonnes de la forme 
    nom+i ou i est un entier. ligne doit être une ligne obtenu à partir d'un
    DictReader. Renvoie une liste vide si les colonnes sont inexistantes"""
    res = []
    try:
        for i in range(1, len(ligne)+1):
            elt = ligne[nom+str(i)]
            if elt == '':
                continue
            res.append(elt)
    except:
        return res
    return res

def nb_colonnes_csv(nom_fichier, chaine = False):
    """Renvoie le nombre de colonne du fichier dont le chemin est passe
    en argument
    Si chaine vaut True, cela indique que nom_fichier est une chaine de caractères contenant 
    les résultats en format CSV (et non pas un nom de fichier a ouvrir)"""
    res = 0
    if (chaine):
        fichier = nom_fichier
    else:
        fichier = open(nom_fichier, "r")
    obj = csv.reader(fichier, delimiter=';')
    for ligne in obj:
        taille_ligne = len(ligne)
        if taille_ligne > res:
            res = taille_ligne
    if (not chaine):
        fichier.close()
    return res
            

    