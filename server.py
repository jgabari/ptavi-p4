#!/usr/bin/python3
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import json
import time


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    diccionario = {}
    format = '%Y-%m-%d %H:%M:%S'

    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """

        # imports the dictionary from a json file if it exists
        self.json2registered()

        # look for expired clients
        self.expiration()

        print('Cliente en IP:' + str(self.client_address[0]) +
              ', puerto:' + str(self.client_address[1]) +
              ' manda:\r')
        print(self.rfile.read().decode('utf-8'))
        for line in self.rfile:
            word_list = line.decode('utf-8').split()
            if word_list[0] == 'REGISTER':
                client = word_list[1].split(':')[1]
                address = str(self.client_address[0])
                self.diccionario[client] = {'address': address}
                self.register2json()
                # if the client already exists it is updated else it is added
                print('Añadido ' + client + 'al diccionario.\r')
            elif word_list[0] == 'Expires:':
                expires_value = int(word_list[1].split('\r')[0])
                if expires_value == 0:
                    del self.diccionario[client]
                    print('Eliminado ' + client + 'por expiración.\r')
                    self.register2json()
                else:
                    expire_time = time.gmtime(time.time() + expires_value)
                    expires = time.strftime(self.format, expire_time)
                    self.diccionario[client]['expires'] = expires
                    self.register2json()
        self.wfile.write(b"SIP/2.0 200 OK")

    def expiration(self):
        """
        Look for and delete expired clients
        """
        for client in self.diccionario:
            c_time = time.strftime(self.format, time.gmtime(time.time()))
            if self.diccionario[client]['expires'] <= c_time:
                del self.diccionario[client]
                print('Eliminado ' + client + 'por expiración.\r')
                self.register2json()

    def register2json(self):
        """
        Saves the dictionary in a json file
        """
        with open('registered.json', 'w') as jsonfile:
            json.dump(self.diccionario, jsonfile, indent=4)

    def json2registered(self):
        """
        Import the dictionary from a json file if it exists
        """
        try:
            with open('registered.json', 'r') as jsonfile:
                self.diccionario = json.load(jsonfile)
        except FileNotFoundError:
            self.diccionario = self.diccionario




if __name__ == "__main__":
    # Listens at localhost ('') port puerto
    # and calls the EchoHandler class to manage the request
    try:
        puerto = int(sys.argv[1])
    except NameError:
        sys.exit('Usage: server.py puerto')
    serv = socketserver.UDPServer(('', puerto), SIPRegisterHandler)

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
