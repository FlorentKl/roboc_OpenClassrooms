# coding:utf8

import os
from Modules.labyrinthe import Labyrinthe


class Carte:
    """Objet de transition entre un fichier et un labyrinthe. 
    
    Cet objet nous permet notamment de sélectionner une carte parmis celles 
    disponibles et instancie le labyrinthe correspondant.
    """

    def __init__(self, nom, chaine):
        self.nom = nom
        self.lab = Labyrinthe(chaine)

    def __repr__(self):
        return "<Carte {}>".format(self.nom)

    @staticmethod
    def choixCarte():
        """
        Prend en entrée une liste de carte disponibles
        Propose au joueur le choix de la carte
        Retourne le labyrinthe choisi
        """

        cartes = list()

        for nom_fichier in os.listdir("./cartes/"):
            if nom_fichier.endswith(".txt"):
                chemin = os.path.join("cartes", nom_fichier)
                # [0] : On met première lettre en majuscule, [1:-4] minuscule + suppression extension du fichier
                nom_carte = nom_fichier[0].upper() + nom_fichier[1:-4].lower()
                with open(chemin, "r") as fichier:
                    contenu = fichier.read()
                    carte = Carte(nom_carte, contenu)
                    cartes.append(carte)

        print("Cartes existantes : ")
        for i, carte in enumerate(cartes):
            print(f"  {i + 1} - {carte.nom}")

        while True:
            try:
                choixCarte = int(input("Quelle carte choissez-vous ?"))
                # On donne a choisir un carte selon le nombre de cartes disponible +1, car index commence à 0
                if choixCarte not in range(1, len(cartes) + 1):
                    print("Erreur : La cartes choisies n'existe pas.")
                    continue
            except ValueError:
                print("Erreur : Veuillez saisir un nombre.")
                continue
            else:
                carteChoisie = cartes[choixCarte - 1]  # choix -1 car index commence à 0
                break

        print("Vous avez choisie la carte : " + carteChoisie.nom)
        # carteChoisie.affichage()

        return carteChoisie
