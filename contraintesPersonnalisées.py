#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from parametres import Parametres
from erreurs import *
from outils import *
from etudiant import Etudiant
from ue import UE
from traitement import *
import gurobipy as gp
from gurobipy import GRB
import solveur as solveur

def ajouter_contraintes(modele, vars_x, vars_y, vars_x_par_ue, 
                        vars_creneaux_incompatibles, vars_cours_par_ue, vars_td_tme_par_ue):
    """Fonction appelée par le solveur de contrainte au moment de l'ajout des
    contraintes au modèle"""
    ajouter_containtes_M1_S2(modele, vars_x, vars_y, vars_x_par_ue, 
                        vars_creneaux_incompatibles, vars_cours_par_ue, vars_td_tme_par_ue)
    
    
    
def ajouter_containtes_M1_S1(modele, vars_x, vars_y, vars_x_par_ue, 
                        vars_creneaux_incompatibles, vars_cours_par_ue, vars_td_tme_par_ue):   
    """Contraintes particulières au premier semestre de M1"""
    return 

def ajouter_containtes_M1_S2(modele, vars_x, vars_y, vars_x_par_ue, 
                        vars_creneaux_incompatibles, vars_cours_par_ue, vars_td_tme_par_ue):   
    """Contraintes particulières au second semestre de M1"""
    ajouter_contrainte_speciale_ml_mll(modele, vars_y)
     
def ajouter_contrainte_speciale_ml_mll(modele, vars_y):
    """Un étudiant ne peut pas etre inscrit en ml et en mll"""
    for etu, variables in vars_y.items():
        y_ml = solveur.chercher_variable_par_ue(variables, "ml")
        y_mll = solveur.chercher_variable_par_ue(variables, "mll")
        if (y_ml and y_mll):
            modele.addConstr(gp.quicksum([y_ml, y_mll]) <= 1)
