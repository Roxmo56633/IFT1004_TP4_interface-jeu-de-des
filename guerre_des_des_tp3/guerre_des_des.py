"""
Contien la classe GuerreDesDes, qui contient le déroulement global d'une partie de guerre des dés
"""

from guerre_des_des_tp3.case import Case
from guerre_des_des_tp3.de import De
from guerre_des_des_tp3.afficheur import afficher


class GuerreDesDes:
    def __init__(self, joueurs, carte):
        """
        Constructeur de la classe GuerreDesDes

        Args:
            joueurs (list): Les joueurs qui s'affrontent
            carte (Carte): La carte du jeu
        """
        self.joueurs = joueurs
        self.carte = carte

    def afficher_joueurs(self):
        """
        Cette méthode affiche la liste des joueurs.
        """
        afficher("Liste des joueurs:")
        for joueur in self.joueurs:
            joueur.afficher_information()

    def deroulement_global(self):
        """
        Cette méthode effectue la totalité du déroulement d'une partie.
        Référez-vous à l'énoncé du TP3 pour en comprendre le détail.
        """

        while not self.partie_terminee():
            for joueur in self.joueurs:
                if not joueur.est_elimine(self.carte):
                    joueur.afficher_tour()
                    tour_termine = False
                    while not tour_termine:
                        self.carte.tout_deselectionner()
                        self.carte.afficher()
                        attaquant = joueur.selectionner_attaquant(self.carte)
                        if attaquant is None:
                            tour_termine = True
                        else:
                            self.carte.afficher()
                            defenseur = joueur.selectionner_defenseur(self.carte, attaquant)
                            if defenseur is not None:
                                self.carte.afficher()
                                self.attaquer(attaquant, defenseur)
                                if self.conquete(joueur):
                                    tour_termine = True
                    self.fin_du_tour(joueur)
        self.determiner_gagnant().afficher_victoire()

    def attaquer(self, attaquant, defenseur):
        """
        Cette méthode effectue le lancer de dés de l'attaquant et du défenseur, affiche les
        données de la bataille puis enclenche le processus résultant de l'attaque.

        Args:
            attaquant (Case): La case en attaque
            defenseur (Case): La case en défense

        Returns:
            int: La force de l'attaquant
            int: La force du défenseur
                Note: ces valeurs de retour ne sont utiles qu'au TP4.

        """
        afficher("-" * 30 + "\nATTAQUE!!!")
        afficher("Attaquant: ")
        force_attaquant = attaquant.lancer_des()
        afficher("Défenseur: ")
        force_defenseur = defenseur.lancer_des()
        self.resultat_attaque(attaquant, force_attaquant, defenseur, force_defenseur)
        afficher("-" * 30)
        return force_attaquant, force_defenseur

    def resultat_attaque(self, attaquant, force_attaquant, defenseur, force_defenseur):
        """
        Cette méthode déclenche un succès (GuerreDesDes.attaque_succes) si la force
        de l'attaquant est plus grande que la force du défenseur, et un échec
        sinon (GuerreDesDes.attaque_echec)

        Attention: Selon les règles du jeu, dans le cas d'une égalité des forces,
        le défenseur l'emporte.

        Args:
            attaquant (Case): La case qui attaque
            force_attaquant (int): La force avec laquelle elle attaque
            defenseur (Case): La case qui se défend
            force_defenseur (int): La force avec laquelle elle se défend
        """
        if force_attaquant > force_defenseur:
            self.attaque_succes(attaquant, defenseur)
        else:
            self.attaque_echec(attaquant)

    def attaque_succes(self, attaquant, defenseur):
        """
        Cette méthode effectue deux actions:
         - changer l'appartenance de la case en défense pour celle de la case
            en attaque (Case.definir_appartenance).
         - enlever tous les dés sauf un de la case attaque, et remplacer les dés
            de la case défense par les dés enlevés (Case.remplacer_des).
        Vous pouvez définir des sous-méthodes si cela vous facilite le travail.

        Args:
            attaquant (Case): La case ayant réussi son attaque.
            defenseur (Case): La case ayant échoué sa défense.
        """
        afficher("SUCCÈS")
        attaquant_des_restants, attaquant_des_perdus = attaquant.des[:1], attaquant.des[1:]
        attaquant.remplacer_des(attaquant_des_restants)
        defenseur.remplacer_des(attaquant_des_perdus)
        defenseur.definir_appartenance(attaquant.appartenance)

    def attaque_echec(self, attaquant):
        """
        Cette méthode supprime tous les dés de la case attaquante sauf un (Case.remplacer_des).

        Args:
            attaquant: La case ayant échoué son attaque.
        """
        afficher("ÉCHEC")
        attaquant.remplacer_des(attaquant.des[:1])

    def fin_du_tour(self, joueur):
        """
        Cette méthode obtient le nombre n de dés à distribuer pour le joueur en argument,
        qui correspond à la taille de son plus grand territoire
        (Carte.taille_plus_grand_territoire). Il crée les n dés (constructeur de De), les
        attribue au joueur (Joueur.ajouter_n_des) et engendre la distribution des dés sur
        les cases du joueur (Joueur.distribuer_surplus).

        Args:
            joueur Joueur: le joueur qui vient de terminer son tour
        """
        n_nouveaux_des = self.carte.taille_plus_grand_territoire(joueur)
        nouveaux_des = []
        for _ in range(n_nouveaux_des):
            nouveaux_des.append(De())
        joueur.ajouter_n_des(nouveaux_des)
        joueur.distribuer_surplus(self.carte)

    def partie_terminee(self):
        """
        Cette méthode indique si la partie est terminé, i.e. s'il existe un
        gagnant (GuerreDesDes.determiner_gagnant).
        """
        return self.determiner_gagnant() is not None

    def determiner_gagnant(self):
        """
        Cette méthode retourne le joueur ayant conquis (GuerreDesDes.conquete), ou None
        si aucun n'a conquis.

        Returns:
            Joueur: Le joueur ayant conquis (None si aucun)

        """
        for joueur in self.joueurs:
            if self.conquete(joueur):
                return joueur
        return None

    def conquete(self, joueur):
        """
        Cette méthode indique si le joueur en paramètre a conquis, c'est-à-dire qu'il
        possède toutes les cases du jeu.

        Args:
            joueur (Joueur): Le joueur dont on veut savoir s'il a conquis.

        Returns:
            bool: True si toutes les cases appartiennent au joueur, False sinon.

        """
        return all([case.appartenance == joueur for case in self.carte.cases.values()])
