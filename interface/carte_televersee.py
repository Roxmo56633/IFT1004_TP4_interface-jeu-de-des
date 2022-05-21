"""
Ce module contient la classe CarteTeleversee. Celle-ci permet d'utiliser une carte de jeu
provenant d'un fichier texte. Ce fichier doit contenir des . là où il y aura une case, et des
espaces là où il y aura des trous. Évidemment, la carte doit être connectée (toutes les cases
sont accessibles).

Exemple valide:
.. ..
 ...
  .

Exemple invalide:
..
.  .
  ..

"""

from guerre_des_des_tp3.carte import Carte
from guerre_des_des_tp3.case import Case


class CarteTeleversee(Carte):
    def __init__(self, nom_fichier):
        """
        Constructeur de la classe CarteTeleversee.

        Args:
            nom_fichier (str): Le nom du fichier contenant la carte sous forme de points.
        """
        cases = self.lire_fichier_carte(nom_fichier)
        hauteur = 0
        largeur = 0
        for coor in cases.keys():
            hauteur = max(hauteur, coor[0] + 1)
            largeur = max(largeur, coor[1] + 1)
        super().__init__(hauteur, largeur, cases)

    def lire_fichier_carte(self, nom_fichier):
        """
        Cette méthode lit le fichier et convertit son contenu en cases.

        Args:
            nom_fichier (str): Le nom du fichier à lire

        Returns:
            dict: Le dictionnaire de cases, dont les clés sont les coordonnées.
        """
        # VOTRE CODE ICI
        raise NotImplementedError("Vous devez faire le défi #4 pour que cette fonctionnalité fonctionne")
