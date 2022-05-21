"""
Module contenant la classe FenetreIntroduction et ses classes
utilitaires FrameCarte et FrameJoueurs.
"""

from tkinter import IntVar, Radiobutton, Button, Label, Entry, Frame, filedialog, END, messagebox, RIDGE, Toplevel

from guerre_des_des_tp3.afficheur import couleurs_interface
from guerre_des_des_tp3.carte_autogeneree import CarteAutogeneree
from ia.joueur_ordinateur_ameliore import JoueurOrdinateurAmeliore
from interface.carte_televersee import CarteTeleversee
from interface.joueur_humain_tk import JoueurHumainTk


class FrameCarte(Frame):
    def __init__(self, parent):
        """
        Constructeur de la classe FrameCarte. Cette classe gère le menu
        de création de carte. Soit par dimensions (CarteAutogeneree) ou avec un
        fichier (CarteTeleversee).

        Args:
            parent (Frame): Le widget TKinter dans lequel la frame s'intègre.
        """
        super().__init__(parent, borderwidth=1, relief=RIDGE)

        self.choix_mode = IntVar()
        self.radio_generer = Radiobutton(self, text="Générer une carte",
                                         variable=self.choix_mode, value=1,
                                         command=self.selection_mode)
        self.radio_importer = Radiobutton(self, text="Importer une carte",
                                          variable=self.choix_mode, value=2,
                                          command=self.selection_mode)

        self.frame_generer = Frame(self)
        self.label_hauteur = Label(self.frame_generer, text="Hauteur: ")
        self.entry_hauteur = Entry(self.frame_generer, width=5)
        self.label_largeur = Label(self.frame_generer, text="Largeur: ")
        self.entry_largeur = Entry(self.frame_generer, width=5)
        self.label_nb_trous = Label(self.frame_generer, text="Nombre de trous: ")
        self.entry_nb_trous = Entry(self.frame_generer, width=5)
        self.label_hauteur.grid(row=0, column=0)
        self.entry_hauteur.grid(row=0, column=1)
        self.label_largeur.grid(row=1, column=0)
        self.entry_largeur.grid(row=1, column=1)
        self.label_nb_trous.grid(row=2, column=0)
        self.entry_nb_trous.grid(row=2, column=1)

        self.frame_importer = Frame(self)
        self.entry_fichier = Entry(self.frame_importer, text="")
        self.bouton_fichier = Button(self.frame_importer, text="Sélectionner...", command=self.choisir_fichier)
        self.bouton_fichier.grid(row=0, column=0, padx=5, pady=5)
        self.entry_fichier.grid(row=0, column=1, padx=5, pady=5)

        self.radio_generer.grid(row=0, column=0, padx=5, pady=2)
        self.frame_generer.grid(row=1, column=0, padx=5, pady=2)
        self.radio_importer.grid(row=2, column=0, padx=5, pady=2)
        self.frame_importer.grid(row=3, column=0, padx=5, pady=2)

        self.choix_mode.set(1)
        self.selection_mode()

    def choisir_fichier(self):
        """
        Cette méthode ouvre une fenêtre de dialogue pour choisir un fichier
        et met inscrit le nom du fichier choisi dans la zone dédiée à cette fin.
        """
        self.entry_fichier.delete(0, END)
        self.entry_fichier.insert(0, filedialog.askopenfilename())

    def selection_mode(self):
        """
        Cette méthode gère le mode de choix de carte, en fonction des boutons radio.
        """
        if self.choix_mode.get() == 1:
            mode_importer = 'disable'
            mode_generer = 'normal'
        else:
            mode_importer = 'normal'
            mode_generer = 'disable'
        for child in self.frame_importer.winfo_children():
            child.configure(state=mode_importer)
        for child in self.frame_generer.winfo_children():
            child.configure(state=mode_generer)

    def obtenir_carte(self):
        """
        Cette méthode crée une carte en fonction des paramètres déterminés dans le frame.

        Returns:
            carte: La carte créée.
        """
        if self.choix_mode.get() == 1:
            try:
                hauteur = int(self.entry_hauteur.get())
                largeur = int(self.entry_largeur.get())
                nb_trous = int(self.entry_nb_trous.get())
            except ValueError:
                raise ValueError("Les paramètres doivent être des entiers!")
            return CarteAutogeneree(hauteur, largeur, nb_trous)

        else:
            nom_fichier = self.entry_fichier.get()
            return CarteTeleversee(nom_fichier)


class FrameJoueurs(Frame):
    def __init__(self, parent):
        """
        Constructeur de la classe FrameJoueurs. Cette classe gère le menu
        du choix des joueurs.

        Args:
            parent (Frame): Le widget TKinter dans lequel la frame s'intègre.
        """
        super().__init__(parent, borderwidth=1, relief=RIDGE)
        label_joueurs = Label(self, text="Sélectionnez les joueurs")
        label_joueurs.grid(row=0, column=0, padx=10, pady=10)
        self.boutons_joueur = []
        self.couleurs = list(couleurs_interface.keys())
        frame_boutons = Frame(self)
        frame_boutons.grid(row=1, column=0)
        for i in range(6):
            bouton_joueur = Button(frame_boutons, text="Inactif", width=8, font='sans 12',
                                   command=lambda c=i: self.changer_type_joueur(c))
            bouton_joueur.grid(row=i // 2, column=i % 2, padx=5, pady=5)
            bouton_joueur['background'] = self.couleurs[i]
            bouton_joueur['activebackground'] = self.couleurs[i]
            self.boutons_joueur.append(bouton_joueur)

    def obtenir_joueurs(self, carte):
        """
        Cette méthode crée les joueurs en fonction du contenu des boutons.

        Returns:
            list: La liste des joueurs
        """
        joueurs = []
        for bouton_joueur in self.boutons_joueur:
            if bouton_joueur['text'] == "Humain":
                joueurs.append(JoueurHumainTk(bouton_joueur['background']))
            elif bouton_joueur['text'] == "Ordinateur":
                joueurs.append(JoueurOrdinateurAmeliore(bouton_joueur['background'], carte))
        if len(joueurs) < 2:
            raise ValueError("Trop peu de joueurs!")
        return joueurs

    def changer_type_joueur(self, i):
        """
        Cette fonction permet de modifier le contenu du bouton dont
        le numéro est en paramètres.

        Args:
            i (int): Le numéro du bouton à modifier
        """
        if self.boutons_joueur[i]['text'] == "Inactif":
            self.boutons_joueur[i]['text'] = "Humain"
        elif self.boutons_joueur[i]['text'] == "Humain":
            self.boutons_joueur[i]['text'] = "Ordinateur"
        else:
            self.boutons_joueur[i]['text'] = "Inactif"


class FenetreIntroduction(Toplevel):
    def __init__(self, parent):
        """
        Constructeur de la classe FenetreIntroduction. Cette classe permet
        de choisir les paramètres de la partie et de démarrer la partie.
        """
        super().__init__(parent)
        self.parent = parent
        self.transient(parent)
        self.grab_set()

        self.title("Paramètres de la partie...")
        self.carte = None
        self.joueurs = None

        self.label_introduction = Label(self, text="Bienvenue à la Guerre des dés!")

        self.label_introduction.grid(row=0, column=0, padx=10, pady=10)

        self.frame_frame = Frame(self)
        self.frame_carte = FrameCarte(self.frame_frame)
        self.frame_carte.grid(row=0, column=0, padx=10, pady=10)
        self.frame_joueurs = FrameJoueurs(self.frame_frame)
        self.frame_joueurs.grid(row=0, column=1, padx=10, pady=10)
        self.frame_frame.grid(row=1, column=0)

        self.bouton_commencer = Button(self, text="Commencer!", command=self.commencer)
        self.bouton_commencer.grid(row=2, column=0, padx=10, pady=10)

    def commencer(self):
        """
        Cette méthode crée la fenêtre principale en fonction des paramètres dans les frames.
        """
        try:
            self.carte = self.frame_carte.obtenir_carte()
            self.joueurs = self.frame_joueurs.obtenir_joueurs(self.carte)
            self.grab_release()
            self.parent.focus_set()
            self.destroy()

        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    def obtenir_donnees(self):
        return self.carte, self.joueurs
