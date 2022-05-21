"""
Contient la classe JoueurHumainConsole, qui hérite de Joueur. Permet l'interaction avec l'utilisateur.

Pour cette classe, vous êtes encouragé à créer vos propres méthodes afin de réutiliser du code.
"""

from guerre_des_des_tp3.afficheur import afficher, demander
from guerre_des_des_tp3.joueur import Joueur


class JoueurHumainConsole(Joueur):
    def __init__(self, couleur):
        """
        Constructeur de la classe JoueurHumainConsole
        Args:
            couleur: la couleur du joueur
        """
        super().__init__(couleur, "Humain")

    def strategie_selection_attaquant(self, cases_disponibles):
        """
        Cette méthode permet à l'utilisateur de choisir une case attaquante parmi
        les cases disponibles à l'aide de la console.

          - Si le joueur entre des coordonnées au format x,y correspondant à une
          case disponible, on retourne cette case.
          - Si le joueur entre des coordonnées au format x,y ne correspondant pas à une
          case disponible (ou si les coordonnées sont en dehors du plateau), on lui indique
          d'entrer une case disponible et on redemande une case.
          - Si le joueur entre le mauvais format (ou toute autre chaîne de caractères non vide),
          on lui indique que l'entrée est invalide et on redemande une case.
          - Si le joueur n'entre rien, on retourne None.
          - Facultatif: vous pouvez afficher les coordonnées des cases disponibles.

        Exemple: Entrez les coordonnées de la case que vous souhaitez
                 sélectionner pour attaque (ou rien pour terminer le tour): salut
                 Entrée invalide. Entrez les coordonnées de la case que vous souhaitez
                 sélectionner pour attaque (ou rien pour terminer le tour): 3,4
                 Cette case n'est pas disponible pour attaque. Entrez les coordonnées de la case que vous souhaitez
                 sélectionner (ou rien pour terminer le tour): 5,6

        Args:
            cases_disponibles (dict): Les cases disponibles pour l'attaque

        Returns:
            Case: La case sélectionnée pour attaque. None si on choisit de passer notre tour.

        """
        return self.selectionner_case(cases_disponibles,
                                      "Entrez les coordonnées de la case en attaque au format x,y (ou rien pour terminer le tour) : ")

    def strategie_selection_defenseur(self, cases_disponibles, case_attaquante):
        """
        Cette méthode permet à l'utilisateur de choisir une case défenseur parmi
        les cases disponibles à l'aide de la console.

          - Si le joueur entre des coordonnées au format x,y correspondant à une
          case disponible, on retourne cette case.
          - Si le joueur entre des coordonnées au format x,y ne correspondant pas à une
          case disponible (ou si les coordonnées sont en dehors du plateau), on lui indique
          d'entrer une case disponible et on redemande une case.
          - Si le joueur entre le mauvais format (ou toute autre chaîne de caractères non vide),
          on lui indique que l'entrée est invalide et on redemande une case.
          - Si le joueur n'entre rien, on retourne None.
          - Facultatif: vous pouvez afficher les coordonnées des cases disponibles.

        Exemple: Entrez les coordonnées de la case que vous souhaitez
                 sélectionner pour défense (ou rien pour terminer le tour): salut
                 Entrée invalide. Entrez les coordonnées de la case que vous souhaitez
                 sélectionner pour défense (ou rien pour terminer le tour): 5,6
                 Cette case n'est pas disponible pour défense. Entrez les coordonnées de la case
                 que vous souhaitez sélectionner pour défense (ou rien pour terminer le tour): 5,5

        Args:
            cases_disponibles (dict): Les cases disponibles pour la défense.
            case_attaquante (Case): La case en mode attaque.
                IMPORTANT: cet argument n'est pas forcément utile. On le passe car on doit le passer
                à JoueurOrdinateur pour sa méthode du même nom. Vous pouvez donc l'ignorer ici.

        Returns:
            Case: La case sélectionnée pour attaque. None si on choisit de passer notre tour.

        """
        return self.selectionner_case(cases_disponibles,
                                      "Entrez les coordonnées de la case en défense au format x,y (ou rien pour annuler) : ")

    def selectionner_case(self, cases_disponibles, requete):
        coor = self.demander_case(requete)
        while coor is not None and coor not in cases_disponibles:
            afficher(
                "Vous devez entrer une case parmi | {} |".format(' | '.join(
                    ["{},{}".format(x, y) for x, y in cases_disponibles.keys()])))
            coor = self.demander_case(requete)
        return cases_disponibles[coor] if coor is not None else None

    def demander_case(self, requete):
        while True:
            coor = demander(requete)
            if coor == '':
                return None
            try:
                x, y = (int(i) for i in coor.split(','))
                return x, y
            except ValueError:
                afficher("Entrée invalide. ")
