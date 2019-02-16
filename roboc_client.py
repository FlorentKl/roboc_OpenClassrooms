#!/usr/bin/python3
# -*-coding:Utf-8 -*

import time
import sys
import re
from threading import Thread, RLock
from Modules.client import Client

lock = RLock()

# -------------------------- Méthodes multithreadées ---------------------------

def messages_serveur():
    """ Thread d'écoute des messages serveur """

    while not client.jeu_termine:
        msg = client.recevoir()
        if msg == "START":
            print("=== Début de la partie ! ===")
            client.jeu_commence = True
        elif msg == "STOP":
            print("Fin de la partie ! Tapez une touche pour vous déconnecter.")
            client.deconnecter()
            client.jeu_termine = True
        elif msg == "WAIT":
            print("En attente des autres joueurs...")
        elif msg == "CAN_START":
            print("Tapez 'c' pour commencer la partie.")
        elif msg == "TURN":
            print("A votre tour de jouer ! Vous pouvez taper 'Q' pour quitter.")
            client.mon_tour = True
        else:
            print(msg)


def commandes_utilisateur():
    """ Thread de commandes utilisateur """

    while not client.jeu_termine:
        msg = input()

        if not client.jeu_commence:
            # La partie n'a pas commencé, on envoie le message au serveur.
            client.envoyer(msg)
        elif client.mon_tour:
            # C'est au joueur de jouer, on autorise l'envoie de message.
            if re.match("^['M','P']?['N','S','E','O']{1}[1-9]*$", msg.upper()):
                client.envoyer(msg)
                client.mon_tour = False
            elif msg.upper() == "Q":
                client.envoyer(msg)
                client.mon_tour = False
            else:
                print("Commande invalide.")
        else:
            # Ce n'est pas au joueur de jouer.
            pass


# ---------------------------- Programme principal -----------------------------


print("==== Bienvenue dans Roboc! ====")

client = Client(12800, "localhost")
msg = str()


# Tentative de connexion au serveur
while True:
    try:
        client.connecter()
        break
    except:
        print(
            "Erreur: connexion impossible avec le serveur. "
            "Nouvel essai dans 3 secondes..."
        )
        time.sleep(3)


# Message de bienvenue
print("---------------------------------------------------")
print("Coups autorisés :")
print("  Q pour quitter.")
print("  NESO pour déplacer votre robot.")
print("  Vous pouvez préciser un nombre après la direction")
print("  pour déplacer votre robot plus vite. Exemple n3")
print()
print("  P[+direction] pour détruire un mur")
print("  M[+direction] pour détruire une porte")
print("---------------------------------------------------")
print(client.recevoir())


# Initialisation des threads
commandes_utilisateur_t = Thread(target=commandes_utilisateur)
messages_serveur_t = Thread(target=messages_serveur)

# Lancement des threads
commandes_utilisateur_t.start()
messages_serveur_t.start()

# Les thread se terminent après l'envoie d'un message serveur
# Le jeu est terminé
commandes_utilisateur_t.join()
messages_serveur_t.join()
