"""
Ce module contient la classe CanvasCarte, qui permet de dessiner l'ensemble de la carte
et de gérer les clics.
"""

from tkinter import Canvas, ALL

# Cette constante donne la hauteur totale de la carte, en pixels.
DIMENSION_BASE = 300


class CanvasCarte(Canvas):
    def __init__(self, parent, carte):
        """
        Constructeur de la classe CanvasCarte. Attribue les dimensions en pixels
        en fonction des dimensions de la carte, dessine la carte dans l'interface
        et associe le clic de souris à la méthode selectionner_case.

        Args:
            parent (Tk): Le widget TKinter dans lequel le canvas s'intègre.
            carte (Carte): La carte de la guerre des dés à afficher.
        """
        self.font_size_dict = {}
        self.carte = carte
        ratio = self.carte.hauteur / self.carte.largeur
        self.hauteur_canvas = DIMENSION_BASE
        self.largeur_canvas = int(DIMENSION_BASE // ratio)
        super().__init__(parent, width=self.largeur_canvas + 1, height=self.hauteur_canvas + 1,
                         borderwidth=0, highlightthickness=0)

        self.suite_clic = None
        self.hauteur_case = self.hauteur_canvas // self.carte.hauteur
        self.largeur_case = self.largeur_canvas // self.carte.largeur
        self.bind("<Button-1>", self.selectionner_case)
        self.dessiner_canvas()
        self.bind("<Motion>", self.changer_taille_police)
    def case_vers_coordonnees(self, case):
        """
        prend une case en argument et retourne ses coordonnes
        for cle in t:
            print (cle) -> obtenir les clées
            print (t[cle]) -> obtenir les valeurs en utilisant la clée
            mydict = {'george':16,'amber':19}
            res = dict((v,k) for k,v in mydict.items())
            print(res[16]) # Prints george
        """


        recherche = dict((v, k) for k, v in self.carte.cases.items())

        return recherche[case]


    def changer_taille_police(self, event):
        """
        Cette méthode appelle une fonction récursive,
        elle utilise event.x et event.y pour connaitre les pixels de la souris.
        Convertit les pixels en case avec coor = self.pixel_vers_coordonnees
        puis case_sous_la_souris = self.carte.case[coor]
        PUIS crée un dict de font_size vide. self.font_size = {}
        appelle la fonction recursive self.fct_recursive(case_sous_la_souris, 30)
        appelle dessiner_canvas pour que ça dessine tout de suite
        """
        coor_y, coor_x = event.x, event.y
        coor = self.pixel_vers_coordonnees(coor_x, coor_y)
        if coor in self.carte.cases:
            case_sous_la_souris = self.carte.cases[coor]

            self.font_size_dict = {}
            self.fct_recursive(case_sous_la_souris, 50)
            self.dessiner_canvas()


    def fct_recursive(self, case, font_size):
        """
        Créer la fonction récursive

        Prend comme argument une case et une font_size
        Ajoute la font_size au dictionnaire, avec comme clé les coordonnées de la case en cours.
        Rappelle la fonction récursive pour chaque voisin,

        si le voisin n'est pas dans le dictionnaire
        ou

        qu'il est dans le dictionnaire mais que la font_size qui est là est plus petite que la font_size que
        vous lui donneriez avec cet appel

        La deuxième condition décrite ci-haut est nécessaire car sinon ce genre de situation peut arriver:
        [30] [25]
        [15] [20]
        car le chemin que la récursivité a prise est, en partant d'en haut à gauche: droite bas gauche. Le ou
        vous permettra d'aller remplacer le 15 par un 25.

        L'appel récursif a comme argument le voisin et le font_size en argument soustrait par 5..

        """

        if font_size < 20:
            return None
        self.font_size_dict[case.coordonnees] = font_size
        for case in case.voisins:
            if case.coordonnees not in self.font_size_dict.keys() or self.font_size_dict[case.coordonnees] < font_size:
                self.fct_recursive(case, int(font_size) - 5)


    def pixel_vers_coordonnees(self, x, y):
        """
        Cette méthode convertit la position d'un clic en coordonnées de la carte.

        Args:
            x: La position du clic, en x (de haut en bas)
            y: La position du clic, en y (de gauche à droite)

        Returns:
            tuple: Les coordonnées de la case cliquée.
        """
        return x // self.hauteur_case, y // self.largeur_case

    def coordonnees_vers_pixels(self, x, y):
        """
        Cette méthode des coordonnées de la carte en position en pixels

        Args:
            x: La coordonnée en x
            y: La coordonnée en y

        Returns:
            tuple: La position en pixels.
        """
        return x * self.hauteur_case, y * self.largeur_case

    def selectionner_case(self, event):
        """
        Cette méthode prend en argument un clic de souris sur le canvas, et actionne
        la fonction définie comme devant faire suite au clic (self.suite_clic), dont
        l'argument est en coordonnées plutôt qu'en pixels.

        Args:
            event (tkinter.Event): L'événement correspondant au clic

        """
        x, y = event.y, event.x  # nos coordonnées sont transposées par rapport aux pixels
        if self.suite_clic is not None:
            self.suite_clic(self.pixel_vers_coordonnees(x, y))

    def dessiner_canvas(self):
        """
        Cette méthode dessine la carte.

            Dans dessiner_canvas, vous pouvez faire quelque chose comme:

            if len(self.font_size_dict) > 0:
                font_size = self.font_size_dict[(x, y)]
            else:
                font_size = 20

            Puis en argument à create_text, ajouter:
            font="Times {} bold".format(font_size)
        """
        self.delete(ALL)
        for (x, y), case in self.carte.cases.items():
            if len(self.font_size_dict) > 0:
                # print(self.font_size_dict[(x,y)])
                if (x, y) in self.font_size_dict:
                    font_size = self.font_size_dict[(x, y)]
                else:
                    font_size = 20 - 5
            else:
                font_size = 20

            if case.mode == 'attaque':
                outline, width = 'gray', 4
            elif case.mode == 'defense':
                outline, width = 'lightgray', 4
            elif case.mode == 'disponible':
                outline, width = 'black', 3
            else:
                outline, width = 'black', 1

            haut, gauche = self.coordonnees_vers_pixels(x, y)
            bas, droite = self.coordonnees_vers_pixels(x + 1, y + 1)
            self.create_rectangle(gauche, haut, droite, bas, fill=case.appartenance.couleur,
                                  outline=outline, width=width)
            self.create_text((gauche + droite) // 2, (haut + bas) // 2, fill='black',
                             font="Times {} bold".format(font_size), text=len(case.des))
    def permettre_clics(self, suite_clic):
        """
        Cette méthode associe une fonction à exécuter à ce qui doit arriver suite
        à un clic.
        """
        self.suite_clic = suite_clic
