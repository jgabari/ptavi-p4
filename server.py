#!/usr/bin/python3
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        print('Cliente en IP: ' + str(self.client_address[0]) + ', puerto: ' + str(self.client_address[1]))
        self.wfile.write(b"SIP/2.0 200 OK")
        for line in self.rfile:
            print("El cliente nos manda ", line.decode('utf-8'))


if __name__ == "__main__":
    # Listens at localhost ('') port puerto
    # and calls the EchoHandler class to manage the request
    try:
        puerto = int(sys.argv[1])
    except NameError:
        print('Usage: server.py puerto')
    serv = socketserver.UDPServer(('', puerto), SIPRegisterHandler)

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
