from parametres import Parametres

class ColonneInexistante(Exception):
    def __init__(self, message, fichier):
        super().__init__(Parametres.texte[54][Parametres.langue] + message +
                         Parametres.texte[56][Parametres.langue] + fichier)

class FormatDeFichierNonReconnu(Exception):
    def __init__(self, fichier):
        super().__init__(Parametres.texte[55][Parametres.langue] + fichier)