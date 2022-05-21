"""
Module contenant la classe FenetrePrincipale et ses classes utilitaires FrameAttaque
et FrameJoueurActif. Cette fenêtre permet de jouer au jeu.
"""

from tkinter import Tk, Frame, Button, Label, messagebox, Scale

from guerre_des_des_tp3.afficheur import desactiver_affichage, couleurs_interface
from guerre_des_des_tp3.guerre_des_des import GuerreDesDes
from interface.canvas_carte import CanvasCarte
from interface.fenetre_introduction import FenetreIntroduction
from guerre_des_des_tp3.joueur_ordinateur import JoueurOrdinateur

# Le temps entre chaque décision de l'ordinateur et pour chaque bataille, en millisecondes.
TEMPS_ATTENTE = 100
def vitesse(var):
    global TEMPS_ATTENTE
    TEMPS_ATTENTE=var



class FrameAttaque(Frame):
    def __init__(self, parent):
        """
        Constructeur de la classe FrameAttaque. Affiche les informations relatives
        aux attaques.

        Args:
            parent (Tk): La fenêtre dans laquelle ce frame s'insert.
        """
        super().__init__(parent)
        self.label_joueur_attaque = Label(self, text="")
        self.label_force_attaque = Label(self, text="")
        self.label_joueur_defense = Label(self, text="")
        self.label_force_defense = Label(self, text="")

        self.label_joueur_attaque.grid(row=0, column=0)
        self.label_force_attaque.grid(row=0, column=1)
        self.label_joueur_defense.grid(row=1, column=0)
        self.label_force_defense.grid(row=1, column=1)

    def populer(self, joueur_attaque, force_attaque, joueur_defense, force_defense):
        """
        Cette méthode affiche les informations d'une attaque.

        Args:
            joueur_attaque (Joueur): Le joueur qui attaque
            force_attaque (int): La somme des dés de l'attaquant
            joueur_defense (Joueur): Le joueur qui se défend
            force_defense (int): La somme des dés du défenseur
        """
        self.label_joueur_attaque['fg'] = joueur_attaque.couleur
        self.label_joueur_attaque['text'] = "Attaquant: "

        self.label_force_attaque['fg'] = joueur_attaque.couleur
        self.label_force_attaque['text'] = force_attaque

        self.label_joueur_defense['fg'] = joueur_defense.couleur
        self.label_joueur_defense['text'] = "Défenseur: "

        self.label_force_defense['fg'] = joueur_defense.couleur
        self.label_force_defense['text'] = force_defense

    def vider(self):
        """
        Cette méthode enlève l'affichage des attaques.
        """
        self.label_joueur_attaque['text'] = ""
        self.label_force_attaque['text'] = ""
        self.label_joueur_defense['text'] = ""
        self.label_force_defense['text'] = ""


class FrameJoueurActif(Frame):
    def __init__(self, parent):
        """
        Constructeur de la classe FrameJoueurActif. Affiche les informations relatives au
        joueur dont c'est le tour.

        Args:
            parent (Tk): La fenêtre dans laquelle ce frame s'insert.
        """
        super().__init__(parent)

        self.label_nom_joueur = Label(self, text="Joueur actif")
        self.label_des_surplus_fixe = Label(self, text="Dés en surplus: ")
        self.label_des_surplus_variable = Label(self, text="0")
        self.bouton = Button(self, text="-", width=20, command=self.clic_bouton)
        self.scale = Scale(self, from_=10, to=500, orient='horizontal',  command=vitesse,)

        self.label_nom_joueur.grid(row=0, column=0)
        self.label_des_surplus_fixe.grid(row=1, column=0)
        self.label_des_surplus_variable.grid(row=1, column=1)
        self.bouton.grid(row=1, column=2)
        self.scale.grid(row=2, column=1)
    def populer(self, joueur):
        """
        Cette méthode affiche les informations du joueur actif.

        Args:
            joueur (Joueur): le joueur actif
        """
        self.label_nom_joueur['fg'] = joueur.couleur
        self.label_des_surplus_variable['text'] = str(len(joueur.des_en_surplus))
        self.bouton['state'] = 'disable'

    def clic_bouton(self):
        """
        Cette méthode engendre la fin du tour.
        """
        self.sur_fin_tour(None)

    def permettre_fin_tour(self, suite):
        """
        Cette méthode active le bouton de fin du tour.

        Args:
            suite (function): La fonction à exécuter lorsqu'on clique sur le bouton.
        """
        self.bouton['state'] = 'normal'
        self.bouton['text'] = 'Terminer le tour'
        self.sur_fin_tour = suite

    def permettre_annuler_selection(self, suite):
        """
        Cette méthode active le bouton qui annule le choix de l'attaquant.

        Args:
            suite (function): La fonction à exécuter lorsqu'on clique sur le bouton.
        """
        self.bouton['state'] = 'normal'
        self.bouton['text'] = 'Annuler la sélection'
        self.sur_fin_tour = suite


class FenetrePrincipale(Tk):
    def __init__(self):
        """
        Constructeur de la classe FenetrePrincipale.
        Cette classe gère l'instance de Guerre des dés, les joueurs et la carte.
        """
        super().__init__()

        self.title("Guerre des dés")
        self.label_bienvenue = Label(text="Bienvenue à la Guerre des dés!")
        self.bouton_commencer = Button(text="Commencer", width=20, command=self.lancer_fenetre_introduction)
        self.label_bienvenue.grid(row=0, column=0, padx=10, pady=10)
        self.bouton_commencer.grid(row=1, column=0, padx=10, pady=10)

    def lancer_fenetre_introduction(self):
        fenetre_introduction = FenetreIntroduction(self)
        self.wait_window(fenetre_introduction)
        carte, joueurs = fenetre_introduction.obtenir_donnees()
        if carte is not None and joueurs is not None:
            self.demarrer(carte, joueurs)

    def demarrer(self, carte, joueurs):
        """
        Lance une partie.

        Args:
            carte (Carte): La carte de la partie
            joueurs (list): La liste des joueurs
        """
        desactiver_affichage()
        self.label_bienvenue.destroy()
        self.bouton_commencer.destroy()

        self.guerre_des_des = GuerreDesDes(joueurs, carte)
        self.joueurs = joueurs
        self.carte = carte

        carte.diviser_territoires(joueurs)
        self.canvas_carte = CanvasCarte(self, carte)
        self.canvas_carte.grid(row=0, column=0, padx=20, pady=20)

        self.frame_attaque = FrameAttaque(self)
        self.frame_attaque.grid(row=1, column=0, padx=10, pady=10)

        self.frame_joueur = FrameJoueurActif(self)
        self.frame_joueur.grid(row=2, column=0, padx=10, pady=10)

        self.joueur_index = 0
        self.joueur_actuel = joueurs[self.joueur_index]


        self.deroulement_debut_tour()

    def incrementer_joueur(self):
        """
        Cette méthode permet de passer au prochain joueur.
        """
        self.joueur_index = (self.joueur_index + 1) % len(self.joueurs)
        self.joueur_actuel = self.joueurs[self.joueur_index]

    def est_joueur_ordi(self):
        """
        Cette méthode indique s'il s'agit d'un joueur ordinateur

        Returns:
            bool: True s'il s'agit d'un ordinateur, False si joueur humain
        """
        return isinstance(self.joueur_actuel, JoueurOrdinateur)

    def redessiner(self, suite):
        """
        Cette méthode active le redessinage de la carte, et déclenche
        la suite.

        Args:
            suite (fonction): La fonction à exécuter suite au redessinage
        """

        self.canvas_carte.dessiner_canvas()
        self.frame_attaque.vider()

        if self.est_joueur_ordi():
            temps_attente = TEMPS_ATTENTE
            print(temps_attente)
        else:
            temps_attente = 0
        self.after(temps_attente, suite)

    def afficher_joueur(self, joueur, suite):
        """
        Cette méthode affiche le joueur en cours

        Args:
            joueur (Joueur): Le joueur à afficher
            suite (fonction): La fonction à exécuter suite à l'affichage du joueur
        """
        self.frame_joueur.populer(joueur)
        self.redessiner(suite)

    def afficher_attaque(self, joueur_attaque, force_attaque, joueur_defense, force_defense, suite):
        """
        Cette méthode permet d'afficher les informations sur une attaque. <

        Args:
            joueur_attaque: Le joueur qui attaque
            force_attaque: La somme des dés de l'attaquant
            joueur_defense: Le joueur qui se défend
            force_defense: La somme des dés du défenseur
            suite (fonction): La fonction à exécuter suite à l'affichage
        """
        self.frame_attaque.populer(joueur_attaque, force_attaque, joueur_defense, force_defense)
        self.after(TEMPS_ATTENTE, lambda: self.redessiner(suite))

    def deroulement_debut_tour(self):
        """
        DÉROULEMENT, partie 1.
        Débute le tour
        """
        if self.est_joueur_ordi():
            self.canvas_carte.permettre_clics(None)
        self.afficher_joueur(self.joueur_actuel, self.deroulement_choix_attaquant)

    def deroulement_choix_attaquant(self):
        """
        DÉROULEMENT, partie 2.
        Permet le choix de l'attaquant.
        """
        if self.guerre_des_des.partie_terminee():
            self.afficher_gagnant()
        else:
            self.carte.tout_deselectionner()
            if self.est_joueur_ordi():
                attaquant = self.joueur_actuel.selectionner_attaquant(self.carte)
                self.deroulement_fin_selection_attaquant(attaquant)
            else:
                self.frame_joueur.permettre_fin_tour(lambda _: self.deroulement_fin_selection_attaquant(None))
                self.canvas_carte.permettre_clics(lambda coor:
                                                  self.deroulement_choix_attaquant_humain(coor))

    def deroulement_choix_attaquant_humain(self, coor):
        """
        DÉROULEMENT, partie 3.
        Permet le choix de l'attaquant par un joueur humain

        Args:
            coor (tuple): Les coordonnées sur lesquelles on a cliqué
        """
        attaquant = self.joueur_actuel.selectionner_attaquant(self.carte, coor)
        if attaquant is None:
            self.deroulement_choix_attaquant()
        else:
            self.deroulement_fin_selection_attaquant(attaquant)

    def deroulement_fin_selection_attaquant(self, attaquant):
        """
        DÉROULEMENT, partie 4.
        Termine le tour ou permet de choisir un défenseur.

        Args:
            attaquant (Case): La case qui attaque. Si None, c'est la fin du tour.
         """

        if attaquant is None:
            self.guerre_des_des.fin_du_tour(self.joueur_actuel)
            self.incrementer_joueur()
            self.deroulement_debut_tour()
        else:
            self.redessiner(lambda: self.deroulement_choix_defenseur(attaquant))

    def deroulement_choix_defenseur(self, attaquant):
        """
        DÉROULEMENT, partie 5.
        Permet de choisir le défenseur.

        Args:
            attaquant (Case): la case qui attaque
        """
        if self.est_joueur_ordi():
            defenseur = self.joueur_actuel.selectionner_defenseur(self.carte, attaquant)
            self.redessiner(self.deroulement_choix_defenseur_fin(attaquant, defenseur))
        else:
            suite = lambda coor_def: self.deroulement_choix_defenseur_humain(attaquant, coor_def)
            self.frame_joueur.permettre_annuler_selection(suite)
            self.canvas_carte.permettre_clics(suite)

    def deroulement_choix_defenseur_humain(self, attaquant, coor_def):
        """
        DÉROULEMENT, partie 6.
        Séelectionne la case en fonction des coordonnées.

        Args:
            attaquant (Case): la case qui attaque.
            coor_def (tuple): les coordonnées de la case sélectionnée pour défense
        """
        defenseur = self.joueur_actuel.selectionner_defenseur(self.carte, attaquant, coor_def)
        if attaquant is None:
            self.deroulement_choix_attaquant()
        else:
            self.redessiner(self.deroulement_choix_defenseur_fin(attaquant, defenseur))

    def deroulement_choix_defenseur_fin(self, attaquant, defenseur):
        """
        DÉROULEMENT, partie 7.
        Annule le choix de l'attaquant ou effectue une attaque.

        Args:
            attaquant (Case): La case qui attaque.
            defenseur (Case): La case qui se défend. Si None on retourne au choix de l'attaquant.

        Returns:

        """
        if defenseur is None:
            self.deroulement_choix_attaquant()
        else:
            self.redessiner(lambda: self.deroulement_attaque(attaquant, defenseur))

    def deroulement_attaque(self, attaquant, defenseur):
        """
        DÉROULEMENT, partie 8.
        Effectue une attaque.

        Args:
            attaquant (Case): La case qui attaque
            defenseur (Case): La case qui se défend
        """
        defenseur_appartenance_avant = defenseur.appartenance
        force_attaquant, force_defenseur = self.guerre_des_des.attaquer(attaquant, defenseur)
        self.carte.tout_deselectionner()
        self.afficher_attaque(attaquant.appartenance, force_attaquant,
                              defenseur_appartenance_avant, force_defenseur,
                              self.deroulement_choix_attaquant)

    def afficher_gagnant(self):
        """
        Affiche le gagnant de la partie.
        """
        gagnant = self.guerre_des_des.determiner_gagnant()
        messagebox.showinfo("Fin de la partie", "Victoire du joueur " + couleurs_interface[gagnant.couleur])
        self.canvas_carte.permettre_clics(None)
        self.frame_joueur.populer(gagnant)
        self.destroy()
        self.__init__()
