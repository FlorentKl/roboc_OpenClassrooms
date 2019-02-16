# coding:utf8

import pickle
import re

from Modules.obstacle import Mur, Porte

# from Modules.labyrinthe import Labyrinthe


class Partie:
    """
    Controle du robot par le joueur,
    Sauvegarder état de la partie
    """

    haut = "n"
    bas = "s"
    gauche = "o"
    droit = "e"
    murer = "m"
    percer = "p"
    save = "q"

    # Gestion des pattern regex
    # in fine : pattern = "^q|([nsoe][0-9]*)|[pm][nsoe]$"
    cmdMvt = haut + bas + gauche + droit
    pattern = (
        "^"
        + save
        + "|(["
        + cmdMvt
        + "][0-9]*)|"
        + "["
        + percer
        + murer
        + "]"
        + "["
        + cmdMvt
        + "]$"
    )

    def __init__(self, nom, labyrinthe):
        self.nom = nom
        self.lab = labyrinthe
        self.gagnee = False
        self.en_cours = False

    def sauvegarde(self):
        """Sauvegarde la partie"""
        with open("sauvegarde", "wb") as fichier:
            sauvPickler = pickle.Pickler(fichier)
            sauvPickler.dump(self)

        self.en_cours = False

    @staticmethod
    def suppr_sauvegarde():
        """
        Supprime la sauvegarde, dans le cas d'une victoire
        """

        # donnee = []
        with open("sauvegarde", "wb") as fichier:
            supprPickler = pickle.Pickler(fichier)
            supprPickler.dump(None)

    @staticmethod
    def conversion(direction):
        """
        Conversion numérique de la direction en tuple pour modifier coordonnées (x,y)
        """

        if direction == Partie.haut:
            direction = (0, -1)
        elif direction == Partie.bas:
            direction = (0, 1)
        elif direction == Partie.gauche:
            direction = (-1, 0)
        elif direction == Partie.droit:
            direction = (1, 0)
        else:
            direction = (0, 0)

        return direction

    def deplacer_robot(self, cmd, robot=0):
        """Déplacement du robot du joueur.
        Change les coordonnées du robot en fonction de la direction données
        Si le robot est sur la sortie, fin de la partie"""

        direction = self.conversion(cmd[0])
        deplacement = 1 if cmd[1:] == "" else int(cmd[1:])

        ancienneCoord = self.lab.robots[robot]

        for i in range(deplacement):

            # Calcul de la position
            pos = tuple(p + q for p, q in zip(self.lab.robots[robot], direction))

            obstacle = self.lab.obstacles.get((pos))
            if obstacle is None or obstacle.traversable:
                self.lab.robots[robot] = pos
                if obstacle:
                    obstacle.arriver(self)

            elif not obstacle.traversable:
                self.lab.robots[robot] = ancienneCoord

        return True

    def percer_mur(self, cmd, robot=0):
        """Permet de transformer un mur "O" en porte "."
        En fonction de la direction donnée par le robot
        Verifie que ce n'est pas effectué sur le bord de la carte"""

        direction = self.conversion(cmd[1])
        pos = tuple(p + q for p, q in zip(self.lab.robots[robot], direction))
        obstacle = self.lab.obstacles.get((pos))

        if (
            0 < pos[0] < self.lab.largeur - 1
            and 0 < pos[1] < self.lab.hauteur - 1
            and isinstance(obstacle, Mur)
        ):
            self.lab.obstacles[pos[0], pos[1]] = Porte(pos[0], pos[1])

        else:
            raise ValueError

    def murer_porte(self, cmd, robot=0):
        """Permet de transformer une porte "." en mur "O"
        En fonction de la direction donnée par le robot
        Verifie que ce n'est pas effectué sur le bord de la carte"""

        direction = self.conversion(cmd[1])
        pos = tuple(p + q for p, q in zip(self.lab.robots[robot], direction))
        obstacle = self.lab.obstacles.get((pos))

        if (
            0 < pos[0] < self.lab.largeur - 1
            and 0 < pos[1] < self.lab.hauteur - 1
            and isinstance(obstacle, Porte)
        ):
            self.lab.obstacles[pos[0], pos[1]] = Mur(pos[0], pos[1])
        else:
            raise ValueError

    def action(self, cmd, robot=0):
        """En fonction de la commande reçu, conditionne comportement du robot.
        Si ne match pas avec le regex, provoque ValueError
        """
        cmd = cmd.lower()
        if not re.match(self.pattern, cmd):
            raise ValueError(f"Commande entrée inconnue. Attendu {self.pattern}")

        if re.match("^[" + self.cmdMvt + "]$", cmd[0]):
            self.deplacer_robot(cmd, robot)

        elif re.match("^" + self.percer + "$", cmd[0]):
            self.percer_mur(cmd, robot)

        elif re.match("^" + self.murer + "$", cmd[0]):
            self.murer_porte(cmd, robot)

        elif re.match("^" + self.save + "$", cmd[0]):
            self.sauvegarde()
