#!/usr/bin/python3

import socket
import threading
from scylla_dependencies.WAF.analizer.analizer import Analizer  # firewall class
from scylla_dependencies.WAF.parser.parsepetition import *


class Proxy:

    def __init__(self, local_addr, lport, remote_addr, rport,
                 maxlength, learn):  # constructor, proxy and server connection info
        self.local_addr = local_addr
        self.lport = lport
        self.remote_addr = remote_addr
        self.rport = rport
        self.maxlength = int(maxlength)  # max legth of bytes received from server
        self.CLIENT2SERVER = 0  # used as constant, data from client to server
        self.SERVER2CLIENT = 1
        self.analizer = Analizer(learn)
        self.parser = Parsepetition()  # class used to parse petitions

    def receive_send_data(self, sock2, client, con_data):

        received = client.recv(1024)  # data from client (browser)
        if any(self.parser.parse_get(received)) or any(self.parser.parse_post(received)) or self.parser.get_method(received) not in ["GET","POST"]:  # if parameters in get or post
            sock2.send(self.analizer.scylla(received, self.CLIENT2SERVER, con_data))  # analyse and send
            out = sock2.recv(self.maxlength)  # received from server

            client.send(self.analizer.scylla(out, self.SERVER2CLIENT, con_data))  # analyse and send
            client.close()

        else:  # if not parameters, does not analyse
            if self.analizer.blockIP(received, con_data[0]):
                sock2.send(bytes(
                "GET / HTTP/1.1\r\nHost: 127.0.0.1:4440\r\nUser-Agent: curl/7.64.0\r\nAccept: */*\r\n\r\n",
                encoding='utf8'))
            else:
                sock2.send(received)  # send to server

            out = sock2.recv(self.maxlength)  # received from server
            client.send(out)  # send to client ( browser )
            client.close()

    def startproxy(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # avoid address alredy in use
        sock.bind((self.local_addr, int(self.lport)))
        sock.listen(1)

        print('[*] Listening on {0} {1}'.format(self.local_addr, self.lport))  # proxy listener, up to 10 clients
        print("Client () -> Proxy ({}:{}) -> Server ({}:{})".format(self.local_addr,self.lport, self.remote_addr, self.rport))

        while True:
            try:
                # print("[*] Conecting to {0} {1}".format(self.remote_addr, self.rport))
                sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock2.connect((self.remote_addr, int(self.rport)))  # server connection
            except:
                print("[!] Error connecting to server.")
                exit()

            client, addr = sock.accept()  # accept clients

            # print('Accepted connection {0} {1}'.format(addr[0], addr[1]))

            try:
                t = threading.Thread(target=self.receive_send_data, args=(sock2, client, addr))  # creates a thread
                t.start()
                t.join()
            except:
                print("[!] Unable to start thread")
