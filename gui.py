#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter.messagebox import *
from tkinter import messagebox
from tkinter import filedialog
import tkinter.ttk as ttk
from parametres import Parametres
from solveur import *
from outils import *
import csv

class MenuGestionnaireVoeux:
    def __init__(self):
        """Fonction de lancement de l'application"""
        self.mode_testeur = False    # Mode permettant de charger les fichiers du dossier testeur
        
        self.fenetre = Tk()
        largeur_ecran = self.fenetre.winfo_screenwidth()
        hauteur_ecran = self.fenetre.winfo_screenheight()
        self.fenetre.geometry("{}x{}+0+0".format(largeur_ecran - 150, hauteur_ecran - 150))
        self.fenetre.title(Parametres.texte[18][Parametres.langue])
        self.menubar = Menu(self.fenetre)
        self.menu1 = Menu(self.menubar, tearoff=0) # Operations relatives aux fichiers
        self.menu2 = Menu(self.menubar, tearoff=0) # Operations relatives au calcul / affichage sur la gui
        self.menu3 = Menu(self.menubar, tearoff=0) # Autre (mode testeur, aide)
        
        
        self.notebook = ttk.Notebook(self.fenetre)
        self.notebook.pack()
        self.onglet_affectations = Frame(self.notebook)
        self.onglet_remplissage_groupes = Frame(self.notebook)
        self.notebook.add(self.onglet_affectations, text=Parametres.texte[16][Parametres.langue])
        self.notebook.add(self.onglet_remplissage_groupes, text=Parametres.texte[17][Parametres.langue])
        
        self.scrollbarx_affectations = Scrollbar(self.onglet_affectations, orient=HORIZONTAL)
        self.scrollbary_affectations = Scrollbar(self.onglet_affectations, orient=VERTICAL)
        self.scrollbarx_remplissage = Scrollbar(self.onglet_remplissage_groupes, orient=HORIZONTAL)
        self.scrollbary_remplissage = Scrollbar(self.onglet_remplissage_groupes, orient=VERTICAL)
        
        self.chargerMenuFichier()
        self.chargerMenuCalculer()
        self.chargerMenuAide()
        
        
        self.menubar.add_cascade(label=Parametres.texte[0][Parametres.langue], menu=self.menu1)
        self.menubar.add_cascade(label=Parametres.texte[1][Parametres.langue], menu=self.menu2)
        self.menubar.add_cascade(label=Parametres.texte[2][Parametres.langue], menu=self.menu3)
        
        self.affectation_realisee = False
        self.remplissage_realise = False
        
        self.fenetre.config(menu=self.menubar)
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("Treeview", 
                        background="#D3D3D3",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#D3D3D3")
        self.style.configure("Treeview.Heading", 
                        background="orange",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="orange")
        self.style.map('Treeview', background=[("selected", "orange")])
        
        self.fenetre.lift()
        self.rafraichir()
        self.fenetre.mainloop()
    
    def testeur(self):
        """Fonction qui active/désactive le mode testeur selon le choix de l'utilisateur"""
        if not self.mode_testeur:
            choix = messagebox.askquestion (Parametres.texte[14][Parametres.langue],Parametres.texte[19][Parametres.langue],icon = 'warning')
            if choix == "yes":
                self.mode_testeur = True
                self.rafraichir(True)
    
        else:
           choix = messagebox.askquestion (Parametres.texte[14][Parametres.langue],Parametres.texte[20][Parametres.langue],icon = 'warning')
           if choix=="yes":
               self.mode_testeur = False
               self.rafraichir(True)
               
    def aide(self):
        """Fonction qui affiche un readMe sur la gui"""
        showinfo(Parametres.texte[41][Parametres.langue], Parametres.texte[42][Parametres.langue])
        afficher_log(Parametres.chemin_log, Parametres.texte[42][Parametres.langue], niveau=logging.INFO, affichage=False)
    
    def chargerMenuFichier(self, recharger=False, resetHard=False):
        """Charge les boutons du menu Fichier. recharger indique si cette fonction est appelee au lancement de la gui ou suite
        a un changement de mode. resetHard indique s'il faut refaire tous les boutons du menu (du a un changement de langue)"""
        if (resetHard):
            a_supprimer = 7
            if self.mode_testeur:
                a_supprimer = 6
            for i in range(a_supprimer):
                self.menu1.delete(0)
            self.menubar.entryconfig(1,label=Parametres.texte[0][Parametres.langue])
                
        if self.mode_testeur:
            if (recharger):
                for i in range (7):
                    self.menu1.delete(0)    
            self.menu1.add_command(label=Parametres.texte[3][Parametres.langue], command=self.charger_fichiers)
        else:
            if (recharger):
                for i in range(6):
                    self.menu1.delete(0)
            self.menu1.add_command(label=Parametres.texte[4][Parametres.langue], command=self.charger_edt)
            self.menu1.add_command(label=Parametres.texte[6][Parametres.langue], command=self.charger_voeux)
            
        self.menu1.add_command(label=Parametres.texte[7][Parametres.langue], command=self.exporter_res, state=DISABLED)
        self.menu1.add_command(label=Parametres.texte[8][Parametres.langue], command=self.exporter_stats, state=DISABLED)
        self.menu1.add_separator()
        self.menu1.add_command(label=Parametres.texte[9][Parametres.langue], command=self.fenetre.quit)
     
        
    def chargerMenuCalculer(self, resetHard=False):
        if (resetHard):
            for i in range(2):
                self.menu2.delete(0) 
            self.menubar.entryconfig(2,label=Parametres.texte[1][Parametres.langue])
        self.menu2.add_command(label=Parametres.texte[10][Parametres.langue], command=self.calculer, state=DISABLED)
        self.menu2.add_command(label=Parametres.texte[11][Parametres.langue], 
                               command=self.afficher_remplissage_groupes, state=DISABLED)
        
    def chargerMenuAide (self, recharger=False, resetHard=False):
        """Charge les boutons du menu Aide. recharger indique si cette fonction est appelee au lancement de la gui ou suite
        a un changement de mode"""
        if (resetHard):
            for i in range(3):
                self.menu3.delete(0)
            self.menubar.entryconfig(3,label=Parametres.texte[2][Parametres.langue])
        if recharger:
            self.menu3.delete(2)
        else:
            self.menu3.add_command(label=Parametres.texte[12][Parametres.langue], command=self.aide)
            self.menu3.add_command(label=Parametres.texte[13][Parametres.langue], command=self.langue)
        
        if (self.mode_testeur):
            self.menu3.add_command(label=Parametres.texte[15][Parametres.langue], command=self.testeur)
        else:
            self.menu3.add_command(label=Parametres.texte[14][Parametres.langue], command=self.testeur)
    
    def charger_fichiers(self):
        """Fonction du monde testeur. Permet de charger tous les csv contenus dans le dossier testeur."""
        Parametres.chemin_edt = "./testeur/EDT22_M1S2.csv"
        Parametres.chemin_voeux = "./testeur/voeux.csv"
        showinfo(Parametres.texte[21][Parametres.langue], Parametres.texte[22][Parametres.langue])
        afficher_log(Parametres.chemin_log, Parametres.texte[22][Parametres.langue], niveau=logging.INFO, affichage=False)
        self.rafraichir()
    
    def charger_csv(self, message):
        """Fonction de chargement d'un fichier csv. Retourne le chemin du fichier
        sélectionné (la chaine vide si aucun n'a ete selectionne) et affiche le 
        message"""
        
        chemin = filedialog.askopenfilename(title=Parametres.texte[23][Parametres.langue],filetypes=[('CSV', '.csv')])
        if chemin != "":
            showinfo(Parametres.texte[24][Parametres.langue], message)
            afficher_log(Parametres.chemin_log, Parametres.texte[24][Parametres.langue], niveau=logging.INFO, affichage=False)
        else:
             showinfo(Parametres.texte[25][Parametres.langue], Parametres.texte[26][Parametres.langue])   
             afficher_log(Parametres.chemin_log, Parametres.texte[26][Parametres.langue], niveau=logging.INFO, affichage=False)
        self.rafraichir()
        return chemin
    
    def charger_edt(self):
        """Fonction de chargement de l'edt"""
        Parametres.chemin_edt = self.charger_csv(Parametres.texte[27][Parametres.langue])
        self.rafraichir()
    
    def charger_voeux(self):
         """Fonction de chargement des voeux"""
         Parametres.chemin_voeux = self.charger_csv(Parametres.texte[29][Parametres.langue])
         self.rafraichir()
    
    
    def calculer(self):
        """Fonction qui calcule les affectations et les affiche sur l'application"""
        try:
            self.dictionnaire_ue = recuperer_ue (Parametres.chemin_edt)
            self.liste_etudiants = recuperer_etudiants(Parametres.chemin_voeux)
            etudiants_edt_incompatible = marquer_etudiants(self.dictionnaire_ue, self.liste_etudiants)
            chaine = ""
            try:
                chaine += Parametres.texte[44][Parametres.langue]
                res, nb_etu_affectation_incomplete = resoudre(self.dictionnaire_ue, self.liste_etudiants)
            except Exception as e:
                res, nb_etu_affectation_incomplete = resoudre(self.dictionnaire_ue, self.liste_etudiants, contrainte_relachee=True)
            if nb_etu_affectation_incomplete > 0:
                msg = Parametres.texte[31][Parametres.langue] + str(nb_etu_affectation_incomplete) + \
                    Parametres.texte[32][Parametres.langue]
                afficher_log(Parametres.chemin_log, msg, niveau=logging.WARNING, affichage=False)
                showwarning(title=Parametres.texte[30][Parametres.langue], message=msg)
            
            chaine += res
            self.donnees = chaine.splitlines()
            self.afficher_resultats2(self.donnees)
            self.affectation_realisee = True
       
        except Exception as e:
            showerror(title=Parametres.texte[5][Parametres.langue], message=e)
            afficher_log(Parametres.chemin_log, msg, niveau=logging.ERROR, affichage=False)
        
        self.rafraichir()
        
    def exporter_res(self):
        """Fonction d'ecriture des resultats"""
        fichier = filedialog.asksaveasfile (title = Parametres.texte[33][Parametres.langue], defaultextension = ".csv")
        if (fichier == None):
            showinfo(Parametres.texte[34][Parametres.langue], Parametres.texte[35][Parametres.langue])
            afficher_log(Parametres.chemin_log, Parametres.texte[35][Parametres.langue], niveau=logging.INFO, affichage=False)
            return
        for ligne in self.donnees:
            fichier.write(ligne + "\n")
        fichier.close()
        showinfo(Parametres.texte[36][Parametres.langue], Parametres.texte[37][Parametres.langue])
        afficher_log(Parametres.chemin_log, Parametres.texte[37][Parametres.langue], niveau=logging.INFO, affichage=False)
        self.rafraichir()
    
    def exporter_stats(self):
        """Fonction d'ecriture des statistiques"""
        fichier = filedialog.asksaveasfile (title = Parametres.texte[33][Parametres.langue], defaultextension = ".csv")
        if (fichier == None):
            showinfo(Parametres.texte[34][Parametres.langue], Parametres.texte[35][Parametres.langue])
            afficher_log(Parametres.chemin_log, Parametres.texte[35][Parametres.langue], niveau=logging.INFO, affichage=False)
            return
        
        
        for ligne in self.remplissage:
            fichier.write(ligne + "\n")
        fichier.close()
        showinfo(Parametres.texte[36][Parametres.langue], Parametres.texte[38][Parametres.langue])
        afficher_log(Parametres.chemin_log, Parametres.texte[38][Parametres.langue], niveau=logging.INFO, affichage=False)
        self.rafraichir()

    def langue(self):
        """Change la langage de l'application (français ou anglais)"""
        if Parametres.langue == 0:
            choix = messagebox.askquestion ("Changer de langue","Souhaitez-vous passer en anglais ?",icon = 'warning')
        else:
            choix = messagebox.askquestion ("Switching language","Would you like to switch to French ?",icon = 'warning')
        
        if choix == "yes":
            Parametres.langue = (Parametres.langue + 1) % 2
            #changement des menu (et de leurs boutons)
            self.chargerMenuFichier(resetHard=True)
            self.chargerMenuCalculer(resetHard=True)
            self.chargerMenuAide(resetHard=True)
            #changement des onglets
            self.notebook.tab(0, text = Parametres.texte[16][Parametres.langue])
            self.notebook.tab(1, text = Parametres.texte[17][Parametres.langue] )
            self.fenetre.title(Parametres.texte[18][Parametres.langue])
            #showinfo(Parametres.texte[41][Parametres.langue], Parametres.texte[43][Parametres.langue])
        self.rafraichir()
        

    def afficher_remplissage_groupes(self):
        """Affiche le remplissage de chaque groupe dans un onglet dedie"""
        nb_colonnes = 0
        lignes_a_afficher = []
        stockagePourExport = []
        tmp = ""
        for nom_ue, ue in self.dictionnaire_ue.items():
            nb_groupes = len(ue.capacites_groupes)
            nb_colonnes = max(nb_colonnes, nb_groupes)
            ligne = [nom_ue]
            tmp = nom_ue + ';'
            for i in range(nb_groupes):
                ligne.append(str(ue.nb_inscrits[i]) + " : " + str(ue.capacites_groupes[i]))
                tmp += str(ue.nb_inscrits[i]) + Parametres.texte[51][Parametres.langue] + str(ue.capacites_groupes[i]) + ";"
            stockagePourExport.append(tmp)
            lignes_a_afficher.append(ligne)
            
        nb_colonnes += 1
        colonnes = [Parametres.texte[45][Parametres.langue]]
        col = Parametres.texte[45][Parametres.langue] + ";"
        for i in range(1, nb_colonnes):
            colonnes.append(Parametres.texte[46][Parametres.langue].format(i))
            col += (Parametres.texte[46][Parametres.langue] + ";").format(i)
        
        stockagePourExport.insert(0, col)
        self.remplissage = stockagePourExport # Utile pour l'export sur un csv
        
        self.arbre_remplissage = ttk.Treeview(self.onglet_remplissage_groupes, columns=(colonnes), height=400,
                    yscrollcommand=self.scrollbary_remplissage.set, xscrollcommand=self.scrollbarx_remplissage.set,
                    show="headings", selectmode="extended") 
        
        self.scrollbary_remplissage.config(command = self.arbre_remplissage.yview)
        self.scrollbarx_remplissage.config(command = self.arbre_remplissage.xview)
        self.scrollbary_remplissage.pack(side=RIGHT, fill=Y)
        self.scrollbarx_remplissage.pack(side=BOTTOM, fill=X)
        
        for i in range(nb_colonnes):
            self.arbre_remplissage.heading('#'+str(i+1), text=colonnes[i], anchor=W)
            self.arbre_remplissage.column('#'+str(i+1), stretch=NO, minwidth=0)
        
        self.arbre_remplissage.pack()
        
        i = 0
        for ligne in lignes_a_afficher:
            self.arbre_remplissage.insert("", index=i, values=(ligne))
            i+=1
            
        self.remplissage_realise = True
        showinfo(Parametres.texte[39][Parametres.langue], Parametres.texte[40][Parametres.langue])
        afficher_log(Parametres.chemin_log, Parametres.texte[40][Parametres.langue], niveau=logging.INFO, affichage=False)
        self.rafraichir()
        
    def griser_menu(self, numero, etat=True, menu=1):
        """Gris le menu dont le numero est passe en argument si etat=True,
        le degrise sinon"""
        if etat:
            if (menu == 1):
                self.menu1.entryconfigure(numero, state=DISABLED)
            else:
                self.menu2.entryconfigure(numero, state=DISABLED) # pas besoin de tester menu3, aucun bouton grisable
        else:
            if (menu == 1):
                self.menu1.entryconfigure(numero, state=NORMAL)
            else:
                self.menu2.entryconfigure(numero, state=NORMAL) # pareil
        
    def griser_calculer(self, etat=True): 
        """Grise le menu export si etat=True, le degrise sinon"""
        bouton = 0
        self.griser_menu(bouton, etat, 2)
    
    def griser_exporter_resultats(self, etat=True):
        """Grise le menu d'export des résultats si 
        etat=True, le degrise sinon"""
        bouton = 2
        if self.mode_testeur:
            bouton = 1
        self.griser_menu(bouton, etat)
        
    def griser_exporter_statistiques(self, etat=True):
        """Grise le menu d'export des résultats si 
        etat=True, le degrise sinon"""
        bouton = 3
        if self.mode_testeur:
            bouton = 2
        self.griser_menu(bouton, etat)
        
    def griser_afficher_remplissage(self, etat=True): 
        """Grise le menu export d'affichage du remplissage des groupes si 
        etat=True, le degrise sinon"""
        bouton = 1
        self.griser_menu(bouton, etat, 2)
            
    def rafraichir(self, changementMode=False):
        """Actualise l'etat de la fenetre. changementMode indique qu'un changement de mode (testeur) a été effectué
        et qu'il faut par conséquent remplacer des boutons"""
        
        if Parametres.chemin_edt == "" or Parametres.chemin_voeux == "":
            self.griser_calculer()
        else:
            self.griser_calculer(False)
        
        if changementMode:
            self.chargerMenuFichier(recharger=True)
            self.chargerMenuAide(recharger=True)
        
        if self.affectation_realisee:
            self.griser_afficher_remplissage(False)
            self.griser_exporter_resultats(False)
        else:
            self.griser_afficher_remplissage()
            
        if self.remplissage_realise:
            self.griser_exporter_statistiques(False)
        

        
    def afficher_resultats(self, nom_fichier):
        """Affiche les affectations (contenues dans un fichier) dans un onglet dedie"""
        nb_colonnes = nb_colonnes_csv(nom_fichier)
        colonnes = [ Parametres.texte[47][Parametres.langue], Parametres.texte[48][Parametres.langue], Parametres.texte[49][Parametres.langue] ]
        for i in range(1, nb_colonnes+1 - len(colonnes)):
            colonnes.append(Parametres.texte[50][Parametres.langue] + str(i))
        
        self.arbre_affectations = ttk.Treeview(self.onglet_affectations, columns=(colonnes), height=400,
                    yscrollcommand=self.scrollbary_affectations.set, xscrollcommand=self.scrollbarx_affectations.set,
                    show="headings", selectmode="extended")    
        
        self.scrollbary_affectations.config(command = self.arbre_affectations.yview)
        self.scrollbarx_affectations.config(command = self.arbre_affectations.xview)
        self.scrollbary_affectations.pack(side=RIGHT, fill=Y)
        self.scrollbarx_affectations.pack(side=BOTTOM, fill=X)

        for i in range(nb_colonnes):
            self.arbre_affectations.heading('#'+str(i+1), text=colonnes[i], anchor=W)
            self.arbre_affectations.column('#'+str(i+1), stretch=NO, minwidth=0)
            
        self.arbre_affectations.pack()
        i = -1
        
        with open(nom_fichier, 'r') as f:
            obj = csv.reader(f, delimiter=';')
            for ligne in obj:
                if i == -1:
                    i = 0
                    continue
                
                if Parametres.texte[52][Parametres.langue][1:] in ligne:
                    self.arbre_affectations.insert("", index=i, values=(ligne), tag="TAG_INCOMPLET")
                elif Parametres.texte[53][Parametres.langue][1:] in ligne:
                    self.arbre_affectations.insert("", index=i, values=(ligne), tag="TAG_CHEVAUCHEMENT")

                else:
                    self.arbre_affectations.insert("", index=i, values=(ligne))
                i+=1
        self.arbre_affectations.tag_configure ("TAG_INCOMPLET" , foreground = "white" , background = "red")
        self.arbre_affectations.tag_configure ("TAG_CHEVAUCHEMENT" , foreground = "white" , background = "purple")
        self.rafraichir()
    
    def afficher_resultats2(self, donnees):
        """Affiche les affectations (recues sous forme de chaine de caractères) dans un onglet dedie"""
        nb_colonnes = nb_colonnes_csv(donnees, True)
        
        colonnes = [ Parametres.texte[47][Parametres.langue], Parametres.texte[48][Parametres.langue], Parametres.texte[49][Parametres.langue] ]
        for i in range(1, nb_colonnes+1 - len(colonnes)):
            colonnes.append(Parametres.texte[50][Parametres.langue] + str(i))
        
        self.arbre_affectations = ttk.Treeview(self.onglet_affectations, columns=(colonnes), height=400,
                    yscrollcommand=self.scrollbary_affectations.set, xscrollcommand=self.scrollbarx_affectations.set,
                    show="headings", selectmode="extended")    
        
        
        self.scrollbary_affectations.config(command = self.arbre_affectations.yview)
        self.scrollbarx_affectations.config(command = self.arbre_affectations.xview)
        self.scrollbary_affectations.pack(side=RIGHT, fill=Y)
        self.scrollbarx_affectations.pack(side=BOTTOM, fill=X)

        for i in range(nb_colonnes):
            self.arbre_affectations.heading('#'+str(i+1), text=colonnes[i], anchor=W)
            self.arbre_affectations.column('#'+str(i+1), stretch=NO, minwidth=0)
            
        self.arbre_affectations.pack()
        i = -1
        
        obj = csv.reader(donnees, delimiter=';')
        for ligne in obj:
            if i == -1:
                i = 0
                continue
            if Parametres.texte[52][Parametres.langue][1:] in ligne:
                self.arbre_affectations.insert("", index=i, values=(ligne), tag="TAG_INCOMPLET")
            elif Parametres.texte[53][Parametres.langue][1:] in ligne:
                self.arbre_affectations.insert("", index=i, values=(ligne), tag="TAG_CHEVAUCHEMENT")
            else:
                self.arbre_affectations.insert("", index=i, values=(ligne))
            i+=1
        self.arbre_affectations.tag_configure ("TAG_INCOMPLET" , foreground = "white" , background = "red")
        self.arbre_affectations.tag_configure ("TAG_CHEVAUCHEMENT" , foreground = "white" , background = "purple")
        self.rafraichir()