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
from contraintesPersonnalisées import ajouter_contraintes
import re

def creation_modele(dictionnaire_ue, liste_etudiants, 
                    contrainte_relachee_affectation=False, contrainte_relachee_capacite=False):
    """Creation du solveur. Si contrainte_relachee_affectation vaut True, il est possible 
    que des etudiants n'aient pas une affectation complete
    Si contrainte_relachee_capacite vaut True, le modele ne prendra pas en compte
    les contraintes sur les capacites des groupes"""
    
    modele = gp.Model("Affectation")
    vars_x, vars_y, vars_x_par_ue, vars_creneaux_incompatibles, vars_cours_par_ue, vars_td_tme_par_ue = ajouter_vars(modele, dictionnaire_ue, liste_etudiants) 
    ajouter_fonction_objectif(modele, vars_y)
    ajouter_contrainte_ue_obligatoires(modele, vars_y)
    if not contrainte_relachee_capacite:
        ajouter_contrainte_capacite_groupes(modele, vars_x_par_ue)
    ajouter_contrainte_groupe_unique(modele, vars_x_par_ue)
    ajouter_contrainte_nombre_ue_etudiant(modele, vars_y, contrainte_relachee_affectation)
    ajouter_contrainte_edt(modele, vars_creneaux_incompatibles)
    ajouter_contrainte_inscription_complete(modele, vars_cours_par_ue, vars_td_tme_par_ue, vars_y)
    ajouter_contraintes(modele, vars_x, vars_y, vars_x_par_ue, 
                        vars_creneaux_incompatibles, vars_cours_par_ue, vars_td_tme_par_ue)
    return (modele, vars_x, vars_y, vars_x_par_ue)

def marquer_etudiants(dictionnaire_ue, liste_etudiants):
    """Marque les etudiants dont les voeux sont incoherents et les retourne
    sous forme de liste"""
    modele, vars_x, vars_y, vars_x_par_ue = creation_modele(dictionnaire_ue,
                                             liste_etudiants, True, True)
    modele.optimize()
    etu_edt_incoherent = []
    for etu, variables in vars_y.items():
        ue_obtenues = 0
        for var in variables:
            if ue_obtenues == etu.nb_ue_a_suivre:
                break
            if var.X == 0:
                continue
            ue_obtenues += 1
        if ue_obtenues != etu.nb_ue_a_suivre:
            etu.edt_incompatible = True
            etu_edt_incoherent.append(etu)
    return etu_edt_incoherent

def resoudre(dictionnaire_ue, liste_etudiants, fichier = None, contrainte_relachee=False):
    """Fonction creant le  modele, resolvant le probleme et inscrivant les 
    resultats dans un fichier passe en argument. 
    Si fichier vaut None, la fonction retourne une chaine de caractères contenant les résultats
    et n'écrit pas dans un fichier"""
    modele, vars_x, vars_y, vars_x_par_ue = creation_modele(dictionnaire_ue,
                                                            liste_etudiants, contrainte_relachee)
    modele.optimize()
    nb_etu_affectation_incomplete = 0
    satisfaction_totale = 0
    chaine = ""
    for etu, variables in vars_x.items():
        debut_ligne = "{};{};".format(etu.parcours, etu.numero)
        ligne = ""
        cpt = 0 
        ue_obtenues = 0
        ue_desirees = 0
        liste_ue_obtenues = []
        for var in variables:
            if ue_obtenues == etu.nb_ue_a_suivre:
                break
            if var.X == 0:
                continue
            parcours, nom_ue, numero_groupe = decompose_var_x(var.VarName)
            liste_ue_obtenues.append(nom_ue)
            ligne += ";{} ({})".format(nom_ue, numero_groupe)
            ue_obtenues += 1
            voeux = ""               #
            voeux_obtenus = 1       # utile pour afficher les voeux obtenus
        for n_ue in etu.listes_ue():
            if n_ue in liste_ue_obtenues:
                ue_desirees += 1
                voeux += str(voeux_obtenus) + " , "
            voeux_obtenus += 1
        if ue_obtenues != etu.nb_ue_a_suivre:
            if etu.edt_incompatible:
                ligne += Parametres.texte[53][Parametres.langue]
            else:
                ligne += Parametres.texte[52][Parametres.langue]
            nb_etu_affectation_incomplete += 1
        satisfaction = ue_desirees / etu.nb_ue_a_suivre * 100
        voeux = voeux[:-3]  # on enleve le dernier - (avec espaces) de la chaine 
        satisfaction_totale += satisfaction
        if (fichier != None):
            fichier.write(debut_ligne + "{}".format(voeux) + ligne+"\n")
        else:
            chaine += debut_ligne + "{}".format(voeux) + ligne+"\n"
    satisfaction_totale /= len(vars_y)
    calculer_remplissage_groupes(vars_x_par_ue)
    if (fichier == None):
        chaine += "Total;;{}".format(satisfaction_totale)
        return chaine, nb_etu_affectation_incomplete
    fichier.write("Total;;{}".format(satisfaction_totale))
    return nb_etu_affectation_incomplete

def calculer_remplissage_groupes(vars_x_par_ue):
    """Fonction a appeler apres resolution du probleme afin d'evaluer le
    remplissage de chaque groupe. Modifie directement l'attribut 
    nb_inscrits de chacune des UE"""
    for ue, dico in vars_x_par_ue.items():
        for k, variables in dico.items():
            for var in variables:
                if var.X == 1:
                    ue.nb_inscrits[k] += 1
    
def ajouter_vars(modele, dictionnaire_ue, liste_etudiants):
    """Ajout des variables relatives aux UE des etudiants"""
    
    vars_x = dict()
    vars_y = dict()
    #Dictionnaire utile pour les contraintes sur les capacites
    vars_x_par_ue = dict()
    #Dictionnaire des incompatibilites par etudiant
    vars_creneaux_incompatibles = dict()
    #Dictionnaire des cours
    vars_cours_par_ue = dict()
    vars_td_tme_par_ue = dict()
    for etu in liste_etudiants:
        vars_x[etu] = []
        vars_y[etu] = []
        vars_creneaux_incompatibles[etu] = dict()
        vars_cours_par_ue[etu] = dict()
        vars_td_tme_par_ue[etu] = dict()
        
        #Ajout des y_i_j
        for nom in etu.noms_vars_ue_obligatoires():
            vars_y[etu].append(modele.addVar(vtype=GRB.BINARY, name=nom))       
        for nom in etu.noms_vars_ue_conseillees():
            vars_y[etu].append(modele.addVar(vtype=GRB.BINARY, name=nom)) 
        for nom in etu.noms_vars_ue_equivalentes():
            vars_y[etu].append(modele.addVar(vtype=GRB.BINARY, name=nom)) 
    
        #Ajout des x_i_j_k
        for nom_ue in etu.listes_ue():
            ue = dictionnaire_ue[nom_ue]
            cpt = 0
            if ue not in vars_cours_par_ue[etu]:
                vars_cours_par_ue[etu][ue] = []
            if ue not in vars_td_tme_par_ue[etu]:
                vars_td_tme_par_ue[etu][ue] = []
            for cours in ue.creneaux_cours:
                nom_cours = etu.nom_variable + "_{}_{}_{}".format(nom_ue, "cours", cpt)
                var_cours = modele.addVar(vtype=GRB.BINARY, name=nom_cours)
                vars_cours_par_ue[etu][ue].append(var_cours)
                creneau_cours = ue.creneaux_cours[cpt]
                if creneau_cours not in vars_creneaux_incompatibles[etu]:
                    vars_creneaux_incompatibles[etu][creneau_cours] = []
                vars_creneaux_incompatibles[etu][creneau_cours].append(var_cours)
                cpt += 1
            cpt = 0
            if not ue in vars_x_par_ue:
                vars_x_par_ue[ue] = dict()
            for k in range(ue.nb_groupes):
                if not k in vars_x_par_ue[ue]:
                    vars_x_par_ue[ue][k] = []
                nom = etu.nom_variable + "_{}_{}".format(nom_ue, k)
                var = modele.addVar(vtype=GRB.BINARY, name=nom)
                if len(ue.creneaux_td) > cpt:
                    creneau_td = ue.creneaux_td[cpt]
                    if creneau_td not in vars_creneaux_incompatibles[etu]:
                        vars_creneaux_incompatibles[etu][creneau_td] = []
                    vars_creneaux_incompatibles[etu][creneau_td].append(var)
                if len(ue.creneaux_tme) > cpt:
                    creneau_tme = ue.creneaux_tme[cpt]
                    if creneau_tme not in vars_creneaux_incompatibles[etu]:
                        vars_creneaux_incompatibles[etu][creneau_tme] = []
                    vars_creneaux_incompatibles[etu][creneau_tme].append(var)
                vars_x[etu].append(var)
                vars_td_tme_par_ue[etu][ue].append(var)
                vars_x_par_ue[ue][k].append(var)
                cpt += 1
    modele.update()
    return (vars_x, vars_y, vars_x_par_ue, vars_creneaux_incompatibles, vars_cours_par_ue, vars_td_tme_par_ue)

def ajouter_contrainte_ue_obligatoires(modele, vars_y):
    """Ajout d'une contrainte pour verifier que chaque etudiant est inscrit 
    dans ses UE obligatoires"""
    for etu, variables in vars_y.items():
        for i in range(etu.nb_ue_obligatoires):
            nom = str(variables[i]) + " == 1"
            modele.addConstr(variables[i] == 1, name=nom)
    modele.update()
    
def ajouter_contrainte_capacite_groupes(modele, vars_x_par_ue):
    """Ajout d'une contrainte pour verifier qu'on affecte pas plus d'etudiants
    que la capacite maximale d'un groupe"""
    for ue, dico in vars_x_par_ue.items():
        for k, variables in dico.items():
            modele.addConstr(gp.quicksum(variables) <= ue.capacites_groupes[k])
    modele.update()
    
def ajouter_contrainte_groupe_unique(modele, vars_x_par_ue):
    """Ajout d'une contrainte pour s'assurer qu'un etudiant est inscrit dans
    au plus un groupe au sein d'une meme UE"""
    for ue, dico in vars_x_par_ue.items():
        #La contrainte ne concerne pas les UE avec un groupe ou moins
        if ue.nb_groupes <= 1:
            continue
        for i in range(len(dico[0])):
            somme_variables = []
            for k in range(ue.nb_groupes):
                somme_variables.append(dico[k][i])
            modele.addConstr(gp.quicksum(somme_variables) <= 1)
    modele.update()

def ajouter_contrainte_nombre_ue_etudiant(modele, vars_y, contrainte_relachee):
    """Ajout d'une contrainte pour s'assurer qu'un etudiant suit bien le bon
    nombre d'UE"""
    if contrainte_relachee:
        for etu, variables in vars_y.items():
            nb_ue = etu.nb_ue_a_suivre
            modele.addConstr(gp.quicksum(variables) <= nb_ue)
    else: 
        for etu, variables in vars_y.items():
            nb_ue = etu.nb_ue_a_suivre
            modele.addConstr(gp.quicksum(variables) == nb_ue)
    modele.update()
    
def ajouter_contrainte_edt(modele, vars_creneaux_incompatibles):
    """Ajout d'une contrainte pour s'assurer qu'aucun etudiant n'est inscrit
    a des UE qui se chevauchent"""
    for etu, dico in vars_creneaux_incompatibles.items():
        for creneau, variables in dico.items():
            if len(variables) <= 1 or creneau == Parametres.creneau_poubelle:
                continue
            modele.addConstr(gp.quicksum(variables) <= 1)
    modele.update()

def ajouter_contrainte_inscription_complete(modele, vars_cours_par_ue, vars_td_tme_par_ue, vars_y):
    """Ajout d'une contrainte pour s'assurer qu'un etudiant inscrit dans un
    groupe d'une UE est bien inscrit dans un cours"""
    for etu, dico in vars_cours_par_ue.items():
        cpt = 0
        for ue, variables in dico.items():
            modele.addConstr(gp.quicksum(variables) == gp.quicksum(vars_td_tme_par_ue[etu][ue]))
            modele.addConstr(vars_y[etu][cpt] == gp.quicksum(variables))  
            cpt += 1
    modele.update()
    
def ajouter_fonction_objectif(modele, vars_y):
    """Ajout de la fonction objectif visant à maximiser la satisfaction 
    globale des etudiants"""
    expr = gp.LinExpr()
    for etu, variables in vars_y.items():
        cpt = 1
        coeff = 10000
        for var in variables:
            expr.add(coeff*var)
            coeff -= (cpt * (etu.nb_ue_a_total - cpt))
            cpt += 1
    modele.setObjective(expr, GRB.MAXIMIZE)
    modele.update()
    
def decompose_var_x(nom_var):
    """Renvoie le parcours, l'ue et le parcours a partir d'un nom de variable x"""
    m = re.search("x_.*_(.*)_(.*)_(.*)", nom_var)
    return (m.group(1), m.group(2), str(int(m.group(3))+1))

def decompose_var_y(nom_var):
    """Renvoie l'ue a partir d'un nom de variable y"""   
    m = re.search("y_.*_(.*)", nom_var)
    return m.group(1)  

def chercher_variable_par_ue(variables, ue):
    """recoit les variables y d'un etudiant et retourne le y de la matiere demandée"""
    for var in variables:
        if (decompose_var_y(var.VarName) == ue):
            return var
    return False