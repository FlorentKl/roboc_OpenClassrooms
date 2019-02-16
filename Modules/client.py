import socket
import time


class Client:
    """Client du projet Roboc"""

    taille_message = 1024

    def __init__(self, port_serveur, hote="localchost"):
        self.port = port_serveur
        self.hote = hote
        self.jeu_commence = False
        self.jeu_termine = False
        self.tour_joueur = False

    def connecter(self):
        """ Se connecte au serveur roboc """

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.hote, self.port))

        print("Connexion établie avec le serveur sur le port {}".format(self.port))

    def deconnecter(self):
        """ Se déconnecte du serveur roboc """

        print("Fermeture de la connexion")
        self.socket.close()

    def envoyer(self, msg):
        """ Envoie la saisie au serveur roboc """

        self.socket.send(msg.ljust(self.taille_message).encode())

    def recevoir(self):
        """ Recoit la réponse du serveur roboc """

        self.msg = self.socket.recv(self.taille_message).decode().rstrip()
        return self.msg
