# coding:utf8

from Modules.partie import Partie
from Modules.carte import Carte
import pickle

partie = None
partieSauvegarder = None

# --- Verification si présence d'un fichier de sauvegarde ----#
try:  # On stock le contenu de sauvegarde dans une variable
    with open("sauvegarde", "rb") as fichier:
        partieSauvegarder = pickle.load(fichier)
except FileNotFoundError:  # Si le fihcier n'existe pas, on le crée vide
    with open("sauvegarde", "wb") as fichier:
        x = pickle.Pickler(fichier)
        x.dump(list())
    partieSauvegarder = None

if partieSauvegarder:
    while True:
        continuer = input(
            f"Voulez-vous continuer la partie en cours "
            f"sur la carte {partieSauvegarder.nom} (o/n) ?"
        )
        continuer.lower()
        if continuer == "o":
            partie = partieSauvegarder
            partie.en_cours = True
            print(partieSauvegarder.lab.carte_individuelle())
            break
        elif continuer == "n":
            partieSauvegarder = None
            break

if not partie:
    carte = Carte.choixCarte()
    partie = Partie(carte.nom, carte.lab)
    robot = partie.lab.robot_initial
    partie.lab.robots.append(robot)
    print(partie.lab.carte_individuelle())
    partie.en_cours = True

while partie.en_cours:

    action = input("Action : ")
    try:
        partie.action(action)
    except ValueError:
        print("Commande incorrect.")
        continue

    print(partie.lab.carte_individuelle())

if partie.gagnee:
    print("C'est gagné !!!!")
    Partie.suppr_sauvegarde()
else:
    print("Au revoir !")
