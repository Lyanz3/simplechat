import socket
from threading import *

bind_ip = '127.0.0.1'
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)  # connection buffer of 5

print('Listening on {}:{}'.format(bind_ip, bind_port))

class client(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()

    def run(self):
        while 1 == 1: # while socket is alive just keep reusing it
            request = self.sock.recv(1024).decode()
            print('Recieved: {}'.format(request))
            self.sock.send(b'hey bby whats poppin')

while 1 == 1: # run loop forever
    client_sock, address = server.accept()
    print('{}:{} has connected to the server!'.format(address[0], address[1]))
    client(client_sock, address)
    #client_sock.close()
