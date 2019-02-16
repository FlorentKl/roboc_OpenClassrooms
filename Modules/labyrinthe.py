# coding:utf8

from Modules import obstacle as ob


class Labyrinthe:
    """Représente un labyrinthe.

    Coordonnées du robot, et schema de la carte sous formes de liste de listes.
    """

    def __init__(self, carte):
        """Constructeur de labyrinthe.
        Via carte (str).
        """
        self.chaine = carte  # str
        self.plan = self.chaine.replace("X", " ")  # str
        self.position_element = self.position(carte)  # (robot), (victoire), (obstacles)
        self.robots = list()
        self.robot_initial = self.position_element[0]  # tuple pos robot dans .txt
        self.victoire = self.position_element[1]  # tuple pos sortie
        self.obstacles = {}

        self.largeur = len(carte.split("\n")[0])
        self.hauteur = len(carte.split("\n"))

        # Remplissage de self.obstacles
        for obstacle in self.position_element[2]:
            if (obstacle.x, obstacle.y) in self.obstacles:
                raise ValueError(
                    f"les coordonnées x={obstacle.x} y={obstacle.y} "
                    f"sont déjà utilisées dans cette grille"
                )
            self.obstacles[obstacle.x, obstacle.y] = obstacle

    def __repr__(self):
        """ Représentation du labyrinthe avec des informations de taille """

        carte = str()
        for i, ligne in enumerate(self.position_element):
            for j, case in enumerate(ligne):
                carte += str(case)
            carte += "\n"

        return "{}Hauteur:{}, Largeur:{}\n".format(
            carte, len(self.position_element), len(self.position_element[0])
        )

    def __str__(self):
        """ Représentation générique de la grille du labyrinthe """
        return self.plan

    @staticmethod
    def position(projection):
        """
        Retourne la position
            -robot (x, y) tuple
            -victoire (x, y) tuple
            -obstacles [(x, y), (), ()] liste de tuple
        """

        symboles = {
            ob.Mur.symbole: ob.Mur,
            ob.Sortie.symbole: ob.Sortie,
            ob.Porte.symbole: ob.Porte,
        }

        robot = tuple()
        victoire = tuple()
        obstacles = list()

        # enumerate() necessaire pour parcourir duplicat dans liste et avoir index correct
        for index_y, valeur_y in enumerate(projection.split("\n")):
            for index_x, valeur_x in enumerate(valeur_y):
                if valeur_x == "X":
                    robot = (index_x, index_y)
                elif valeur_x == " ":
                    pass
                else:
                    classe = symboles[valeur_x]
                    objet = classe(index_x, index_y)
                    obstacles.append(objet)

        return robot, victoire, obstacles

    def carte_individuelle(self, robot=0):
        """Représentation de la carte en fonction du joueur
        X robot principal(joueur)
        x robot des autres joueurs
        
        Renvoi un représentation du labyrinthe
        """

        grille = ""
        y = 0
        while y < self.hauteur:
            x = 0
            while x < self.largeur:
                case = self.obstacles.get((x, y))
                if case:
                    grille += case.symbole
                else:
                    grille += " "
                x += 1
            grille += "\n"
            y += 1

        # Chaque chaine est séparé en liste, afin d'avoir une liste de liste

        print("robots[robot] : ", self.robots[robot])
        print("robots : ", self.robots)
        plan = grille.split("\n")
        for y, ligne in enumerate(plan):
            for x, case in enumerate(ligne):
                if (x + 1, y) in self.robots:
                    print("ENCORE UN TESTS ")
                if (x, y) == self.robots[robot]:
                    print("-----TEST-----")
                    plan[y] = list(plan[y])
                    plan[y][x] = "X"
                elif (x, y) in self.robots:
                    plan[y] = list(plan[y])
                    plan[y][x] = "x"
                plan[y] = "".join(plan[y])
        # On remet tout sous forme de chaine
        carte = "\n".join(plan)
        return f"\n{carte}\n"

    def cases_libres(self):
        """Renvoie une liste contenant les coordonnées des cases libre du labyrinthe.
        """
        cases = list()
        plan = self.plan.split("\n")
        for y, ligne in enumerate(plan):
            for x, case in enumerate(ligne):
                if case == " ":
                    cases.append((x, y))

        return cases
