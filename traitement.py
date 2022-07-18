#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from parametres import Parametres
from erreurs import *
from outils import *
from etudiant import Etudiant
from ue import UE


def recuperer_etudiants (chemin_fichier):
    """Retourne la liste des etudiants contenus dans un fichier csv dont le
    chemin est passé en argument
    Peut lever une erreur de type ColonneInexistante ou FormatDeFichierNonReconnu"""
    res = []
    lignes, fichier = dictionnaire_csv (chemin_fichier)
    try:
        for ligne in lignes:
            res.append(Etudiant(ligne))
    except (Exception) as e:
        raise e
    finally:
        fichier.close()
    return res

def recuperer_ue (chemin_fichier):
    """Retourne le dictionnaire (nom_ue : UE) des UE contenues dans un fichier csv dont le
    chemin est passé en argument
    Peut lever une erreur de type ColonneInexistante ou FormatDeFichierNonReconnu"""
    res = dict()
    lignes, fichier = dictionnaire_csv (chemin_fichier)
    try:
        for ligne in lignes:
            ue = UE(ligne)
            res [ue.intitule] = ue
    except (Exception) as e:
        raise e
    finally:
        fichier.close()
    return res