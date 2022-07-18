#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from parametres import Parametres
from erreurs import ColonneInexistante
from outils import *

"""Classe representant les données d'une UE"""
class UE:
    def __init__(self, ligne_ue):
        """Constructeur d'UE. Prend en argument une ligne d'un fichier csv 
        representant une UE. 
        Peut lever une erreur de type ColonneInexistante"""
        try:
            self.intitule = ligne_ue[Parametres.colonne_intitule]
        except:
            raise ColonneInexistante(Parametres.colonne_intitule, Parametres.chemin_edt)
        try:
            self.id = int(ligne_ue[Parametres.colonne_id_ue])
        except:
            raise ColonneInexistante(Parametres.colonne_id_ue, Parametres.chemin_edt)
        try:
            self.nb_groupes = int(ligne_ue[Parametres.colonne_nb_groupes])
        except:
            raise ColonneInexistante(Parametres.colonne_nb_groupes, Parametres.chemin_edt)
        self.creneaux_cours = lire_entier_colonnes_multiples(Parametres.colonne_cours, ligne_ue)
        self.creneaux_td = lire_entier_colonnes_multiples(Parametres.colonne_td, ligne_ue)
        self.creneaux_tme = lire_entier_colonnes_multiples(Parametres.colonne_tme, ligne_ue)
        self.capacites_groupes = lire_entier_colonnes_multiples(Parametres.colonne_capacite, ligne_ue)
        self.nb_inscrits = [0 for i in range(len(self.capacites_groupes))]
        #On décrémente le nombre de groupe pour ne pas créer de variable x_i_j_k pour les creneaux poubelle
        if self.creneaux_td == [Parametres.creneau_poubelle]:
            self.creneaux_td.remove(Parametres.creneau_poubelle)
            self.nb_groupes = 0
        if self.creneaux_tme == [Parametres.creneau_poubelle]:
           self.creneaux_tme.remove(Parametres.creneau_poubelle)
           self.nb_groupes = 0

        
        
    def __str__(self):
        res = self.intitule + " (" + str(self.id) + ") :\n\t-Nombre de groupes : " \
            + str(self.nb_groupes) + "\n\t-Creneaux de cours : " + \
            str(self.creneaux_cours) + "\n\t-Creneaux de TD : " + \
            str(self.creneaux_td) + "\n\t-Creneaux de TME : " + str(self.creneaux_tme) +\
            "\n\t-Capacite des groupes : " + str(self.capacites_groupes) + \
            "\n\t-Nombre d'inscrits par groupe : " + str(self.nb_inscrits)
        return res
    