#!/usr/bin/python3
# -*-coding:Utf-8 -*

from random import choice
from Modules.serveur import Serveur
from Modules.partie import Partie
from Modules.carte import Carte

print("==== Serveur Roboc ====")
partie = None
serveur = Serveur()


# Sélection de la carte
if not partie or partie.gagnee:
    carte = Carte.choixCarte()
    partie = Partie(carte.nom, carte.lab)
    print("Création d'une nouvelle partie : {0}\n".format(partie.nom))
    print(partie.lab.plan)

# Lancement du serveur roboc et attente des connexions client
serveur.demarrer()
if serveur.attendre_connexions():
    partie.en_cours = True

# Boucle principale
while partie.en_cours:

    # Calcule la position de chaque robot
    for client in serveur.clients_connectes:
        robot = choice(partie.lab.cases_libres())
        partie.lab.robots.append(robot)

    # Affichage de la carte sélectionnée
    serveur.envoyer_cartes(partie.lab)
    print(partie.lab)

    # Début de partie
    nb_joueurs = len(serveur.clients_connectes)
    joueur_index = -1

    while not partie.gagnee:

        # Passe au joueur suivant et lui demande de jouer
        joueur_index = (joueur_index + 1) % nb_joueurs
        joueur = serveur.clients_connectes[joueur_index]

        serveur.envoyer_msg(joueur, "TURN")
        print("En attente du joueur {}...".format(joueur_index + 1))

        # Notification d'attente pour les autres joueurs
        for i, client in enumerate(serveur.clients_connectes):
            if i != joueur_index:
                serveur.envoyer_msg(client, "WAIT")

        # Attend la réponse du joueur
        action = joueur.recv(serveur.taille_message).decode().rstrip()
        print(f"Commande reçue {action}...")

        # Exécute la commande
        try:
            partie.action(action, joueur_index)
        except ValueError:
            print("Commande incorrect.")
            continue

        # Affichage de la carte mise à jour
        serveur.envoyer_cartes(partie.lab)

    # La partie a été gagnée
    if partie.gagnee:
        partie.en_cours = False
        serveur.envoyer_msg_tous("Joueur {} gagne la partie!".format(joueur_index + 1))

# Arrêt du serveur
serveur.arreter()
