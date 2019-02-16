import socket
import select
import pickle
import time


class Serveur:
    """Serveur du projet Roboc"""

    taille_message = 1024

    def __init__(self):
        self.hote = ""
        self.port = 12800
        self.clients_connectes = list()

    def demarrer(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.hote, self.port))
        self.socket.listen(5)

        print("Serveur en écoute sur {}:{}".format(self.hote, self.port))

    def arreter(self):
        """ Déconnecte les clients et stope le serveur roboc """

        print("\nEnvoie de la requête de déconnexion...")
        self.envoyer_msg_tous("STOP")
        time.sleep(0.5)

        print("Fermeture des connexions client")
        for client in self.clients_connectes:
            client.close()

        print("Fermeture du socket serveur")
        self.socket.close()

        input("\nTapez un touche pour quitter.")

    def attendre_connexions(self):
        """ Attend les connexions clients
        Le serveur enregistre les connexions client tant que le le message
        de fin d'enregistrement (le caractère 'c') n'a pas été reçu.
        """

        print("En attente des connexions client...")
        nb_clients = 0
        nouvelle_connexion = False

        while True:

            # Ecoute les connexions entrantes pour une durée de 0.05s
            connexions, wlist, xlist = select.select([self.socket], [], [], 0.05)

            for connexion in connexions:

                conn, info = connexion.accept()
                self.clients_connectes.append(conn)
                nb_clients = len(self.clients_connectes)
                nouvelle_connexion = True

                print("Client {} connecté".format(info))

                self.envoyer_msg_tous("Connexion du joueur {}".format(nb_clients))

            if nouvelle_connexion and nb_clients >= 2:
                self.envoyer_msg_tous("{} joueurs sont connectés.".format(nb_clients))
                self.envoyer_msg_tous("Vous pouvez commencer la partie en tapant 'c'.")

            nouvelle_connexion = False

            # Lecture des commandes client
            clients_a_lire = []
            try:
                clients_a_lire, wlist, xlist = select.select(
                    self.clients_connectes, [], [], 0.05
                )
            except select.error:
                pass
            else:
                for client in clients_a_lire:
                    msg = client.recv(self.taille_message).decode().rstrip()

                    if msg.upper() == "C" and nb_clients >= 2:
                        print("Lancement de la partie")
                        self.envoyer_msg_tous("START")
                        return True

                    if msg.upper() == "Q":
                        print("Interruption de la partie")
                        return False

                    if nb_clients < 2:
                        self.envoyer_msg(client, "WAIT")
                    else:
                        self.envoyer_msg(client, "CAN_START")

    def envoyer_msg(self, conn, msg):
        """ Envoie une chaine de caractères vers le client """
        conn.send(msg.ljust(self.taille_message).encode())

    def envoyer_msg_tous(self, msg):
        """ Envoie une chaine de caractère vers tous les clients """
        for conn in self.clients_connectes:
            conn.send(msg.ljust(self.taille_message).encode())

    def envoyer_cartes(self, lab):
        """ Envoie la représentation du labyrinthe vers tous les clients """
        for key, conn in enumerate(self.clients_connectes):
            print(key)
            self.envoyer_msg(conn, lab.carte_individuelle(key))
