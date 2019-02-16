# coding: Utf-8

"""
Ici sont regroupés les classes des différents éléments
du labyrinthe.
"""


class Element:
    """
    Un élément du labyrinthe
    """

    nom = "element"
    traversable = True
    symbole = ""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "<{nom} (x={x}, y={y})>".format(nom=self.nom, x=self.x, y=self.y)

    def __str__(self):
        return "{nom} ({x}.{y})".format(nom=self.nom, x=self.x, y=self.y)

    def arriver(self, labyrinthe):
        """Méthode appelée quand le robot arrive sur la case.

        Il peut être utile de redéfinir cette méthode dans certaines
        circonstances.

        """
        pass


class Mur(Element):
    """
    Un mur
    """

    nom = "mur"
    traversable = False
    symbole = "O"


class Porte(Element):
    """
    Une porte
    """

    nom = "porte"
    traversable = True
    symbole = "."


class Sortie(Element):
    """
    La sortie
    """

    nom = "sortie"
    traversable = True
    symbole = "U"

    def arriver(self, partie):
        """Le robot arrive sur la sortie.

        La partie est gagnée !

        """
        partie.gagnee = True
        partie.en_cours = False
