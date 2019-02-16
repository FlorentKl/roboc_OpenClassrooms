# -*-coding:Utf-8 -*

import unittest
import socket
from Modules.serveur import Serveur
from Modules.client import Client

class ServeurTest(unittest.TestCase):

    """ Test cases utilisés pour tester les fonctions du module serveur """

    def setUp(self):
        """ Initialisation des tests.
        Instanciation d'un serveur, d'un client et initialisation de 
        la connexion.
        """

        self.serveur = Serveur()
        self.client = Client("localhost", 12800)

        # Démarrage du serveur
        self.serveur.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serveur.socket.bind((self.serveur.hote, self.serveur.port))
        self.serveur.socket.listen(5)

        # Connexion du client
        self.client.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.socket.connect((self.client.port, self.client.hote,))

        # Acceptation de la connexion
        self.connexion_client, infos_connexion = self.serveur.socket.accept()


    def tearDown(self):
        """ Fermeture de la connexion et des sockets client et serveur """

        # Fermeture des connexions
        self.serveur.socket.close()
        self.client.socket.close()
        self.connexion_client.close()


    def test_envoyer_message(self):
        """ Teste la connexion par l'envoie et la reception d'un message """

        # Envoie d'un message test
        self.serveur.envoyer_msg(self.connexion_client, "test")

        # Vérification du message test reçu
        msg = self.client.recevoir()
        self.assertEqual(msg, "test")
