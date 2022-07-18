#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Parametres:
    chemin_edt = ""                         #emplacement du fichier edt
    chemin_voeux = ""                       #emplacement du fichier voeux
    chemin_res = ""                         #emplacement du fichier de resultat 
    chemin_log = "log.txt"                  #emplacement du fichier de log
    delimiteurs_fichier = [",", ";"]        #delimiteurs dans les csv
    creneau_poubelle = -1                   #valeur du creneau non pris en compte
    
    #Nom des colonnes dans le csv edt
    colonne_id_ue = "id_ue"
    colonne_intitule = "intitule"
    colonne_nb_groupes = "nb_groupes"
    colonne_capacite = "capac"
    colonne_cours = "cours"
    colonne_td = "td"
    colonne_tme = "tme"
    
    #Nom des colonnes dans le csv voeux
    colonne_num = "num"
    colonne_equiv = "equiv"
    
    #Nom des colonnes dans le csv parcours
    colonne_indice = "index"
    colonne_nb_ue = "nb_ues"
    
    #Colonne commune a parcours.csv et a voeux.csv
    colonne_parcours = "parcours"
    colonne_conseillee = "cons"
    colonne_obligatoire = "oblig"
    
    langue = 0 # 0 = francais, 1 = anglais
    
    # Dictionnaire pour les langues de l'application
    texte = dict()
    
    # les 3 menus
    texte[0] = ("Fichier", "File")
    texte[1] = ("Calculer", "Compute")
    texte[2] = ("Aide", "Help")
    
    #boutons de Fichier
    texte[3] = ("Charger tous les fichiers", "Load all files")
    texte[4] = ("Importer EDT", "Import Time schedule")
    texte[5] = ("Erreur", "Error")
    texte[6] = ("Importer Voeux", "Import Wishes")
    texte[7] = ("Exporter les résultats", "Export results")
    texte[8] = ("Exporter les statistiques", "Export statistics")
    texte[9] = ("Quitter", "Exit")
    
    #boutons de Calculer
    texte[10] = ("Résoudre le modèle", "Solve the model")
    texte[11] = ("Afficher le remplissage des groupes", "Show group filling")
    
    #boutons de Aide
    texte[12] = ("À propos", "Readme")
    texte[13] = ("Langue", "Language")
    texte[14] = ("Mode testeur", "Tester mode")
    texte[15] = ("Désactiver le mode testeur", "Disable tester mode")
    
    #onglets
    texte[16] = ("Affectations", "Assignments")
    texte[17] = ("Remplissage des groupes", "Filling of groups")
    
    #titre fenetres / popup
    texte[18] = ("Gestionnaire de voeux", "Wishes manager")
    texte[19] = ("Etes-vous sur d'activer le mode testeur ?", "Are you sure to switch on the tester mode ?")
    texte[20] = ("Souhaitez-vous désactiver le mode testeur", "Do you want to switch off the tester mode ?")
    texte[21] = ("Fichiers chargés", "Files loaded")
    texte[22] = ("Tous les fichiers ont été récupérés", "All files have been collected")
    texte[23] = ("Veuillez selectionner le fichier à charger", "Please select the file to load")
    texte[24] = ("Fichier chargé", "File loaded")
    texte[25] = ("Problème de chargement", "Loading issue")
    texte[26] = ("Attention: aucun fichier n'a été chargé", "Warning: no file has been loaded")
    texte[27] = ("Le fichier EDT a bien été chargé", "The time schedule file has been successfully loaded")
    texte[28] = ("Le fichier Parcours a bien été chargé", "The Program file has been successfully loaded")
    texte[29] = ("Le fichier Voeux a bien été chargé", "The Wishes file has been successfully loaded")
    texte[30] = ("Problème lors de l'affectation" , "Issue with the assignment")
    texte[31] = ("L'affectation ne s'est pas deroulée correctement: ", "The assignment did not go well: ")
    texte[32] = (" etudiants ont une affectation incomplete.", " students have an incomplete assignment.")
    texte[33] = ("Enregistrer sous ...", "Save as ...")
    texte[34] = ("Export annulé", "Export canceled")
    texte[35] = ("Résultats non enregistrés", "Results have not been saved")
    texte[36] = ("Export réussi" ,"Successful export")
    texte[37] = ("Résultats enregistrés" ,"Results have been saved")
    texte[38] = ("Statistiques enregistrées" ,"Statistics have been saved")
    texte[39] = ("Calcul effectué", "Calculation performed")
    texte[40] = ("Affichage disponible", "Display available")
    texte[41] = ("En cours...", "In progress...")
    texte[42] = ("Cette fonctionnalité est en développement", "This feature is under development")
    texte[43] = ("Développement en cours. Il reste encore des éléments à traduire", "Development in progress. There are still elements to be translated")
    
    # Contenu dans CSV
    texte[44] = ("Parcours;numero;ue obtenues\n", "Program;number;modules obtained\n")
    texte[45] = ("Nom de l'UE", "Name of the module")
    texte[46] = ("Groupe {}", "Group {}")
    texte[47] = ("Parcours", "Program")
    texte[48] = ("Numero", "Number")
    texte[49] = ("Voeux obtenus", "Wishes obtained")
    texte[50] = ("Affectation n°" , "Assignment n°")
    texte[51] = (" sur ", " on ")
    texte[52] = (";INSCRIPTION INCOMPLETE !", ";INCOMPLETE LISTING !")
    texte[53] = (";PROBLEME DE CHEVAUCHEMENT !", ";OVERLAP PROBLEM !" )
    
    # Gestion des erreurs
    texte[54] = ("Colonne inexistante : ", "Missing column : ")
    texte[55] = ("Format de fichier non reconnu pour le fichier ", "Unknown file format for file")
    texte[56] = (" dans ", " in ")
    
    
    