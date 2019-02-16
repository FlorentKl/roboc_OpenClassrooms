# -*-coding:Utf-8 -*

import unittest
from Modules.partie import Partie
from Modules.labyrinthe import Labyrinthe
from Modules.obstacle import *


class PartieTest(unittest.TestCase):
    def setUp(self):
        """Initialisation des tests"""

        with open("./Tests/test_carte.txt", "r") as carte:
            self.carte = carte.read()
        self.lab = Labyrinthe(self.carte)
        self.partie = Partie("test", self.lab)
        self.lab.obstacles

        self.initial = (1, 1)
        self.attenduHaut = (1, 0)
        self.attenduBas = (1, 2)
        self.attenduGauche = (0, 1)
        self.attenduDroit = (2, 1)

        Mur.traversable = True  # Eviter problèmes de déplacement du robot

    def test_conversion_type(self):
        """Test le calcul de la fonction conversion quand direction vers le haut"""

        # calc nouvelle position vers le haut
        self.assertIsInstance(self.partie.conversion(direction=Partie.haut), tuple)

    def test_deplacer_robot_haut(self):
        """Test deplacement du robot vers le haut"""

        self.lab.robots.append(self.initial)
        self.partie.deplacer_robot(self.partie.haut)

        self.assertEqual(self.lab.robots[0], self.attenduHaut)

    def test_deplacer_robot_bas(self):
        """Test deplacement robot vers le bas"""

        self.lab.robots.append(self.initial)
        self.partie.deplacer_robot(self.partie.bas)

        self.assertEqual(self.lab.robots[0], self.attenduBas)

    def test_deplacer_robot_gauche(self):
        """Test deplacement robot vers la gauche"""

        self.lab.robots.append(self.initial)
        self.partie.deplacer_robot(self.partie.gauche)

        self.assertEqual(self.lab.robots[0], self.attenduGauche)

    def test_deplacer_robot_droit(self):
        """Test deplacement robot vers la droite"""

        self.lab.robots.append(self.initial)
        self.partie.deplacer_robot(self.partie.droit)

        self.assertEqual(self.lab.robots[0], self.attenduDroit)

    def test_deplacer_robot_fail(self):
        """Test echecs du deplacement du robot quand un obstacle est rencontrer.
        Un mur se trouve au nord (1,0) de la position initiale du robot (1,1)"""

        self.lab.robots.append(self.initial)
        # On rend le mur non traversable
        Mur.traversable = False
        self.partie.deplacer_robot(self.partie.haut)

        self.assertEqual(self.lab.robots[0], self.initial)

    def test_percer_mur(self):
        """Test de la fonction permettant à un robot de percer un mur.
        On perce le mur à gauche (2,1) du robot"""

        self.lab.robots.append(self.initial)
        # "p" permet entrée correct dans la fonction percer_mur
        self.partie.percer_mur("p" + self.partie.droit)

        self.assertEqual(self.lab.obstacles[2, 1].symbole, ".")

    def test_murer_porte(self):
        """Test de la fonction permettant à un robot de percer un mur.
        On perce le mur en bas (1,2) du robot"""
        self.lab.robots.append(self.initial)
        # "m" permet entrée correct dans la fonction murer_porte
        self.partie.murer_porte("m" + self.partie.bas)

        self.assertEqual(self.lab.obstacles[2, 1].symbole, "O")
