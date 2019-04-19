import socket
from threading import *
from message import Message
from command import Command
import queue

class Server():
    bind_ip = '127.0.0.1' #127.0.0.1:9999
    bind_port = 9999
    message_queue = queue.Queue()
    quit = False

class Connection(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.sock.send('{}'.format(self.addr[1]).encode()) # send id to client
        print('{}:{} has connected to the server!'.format(address[0], address[1]))
        self.start()

    def send(self):
        for m in Server.message_queue.queue:
            if m.sender == self.addr[1] or m.sender == 0:
                self.sock.send(m.sendable().encode())

    def recieve(self):
        request = self.sock.recv(1024).decode()
        recieved_message = Message() # create a message object to store
        recieved_message.parse(request) # parse message into usable format
        Server.message_queue.put(recieved_message) # put the message into the queue

    def run(self):
        while not Server.quit: # while socket is alive just keep reusing it
            self.send()
            self.recieve()

if  __name__ =='__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((Server.bind_ip, Server.bind_port))
    server_socket.listen(5)  # connection buffer of 5
    print('Listening on {}:{}'.format(Server.bind_ip, Server.bind_port))
    client_socket, address = server_socket.accept()

    connection = Connection(client_socket, address)
    connection.join()

    server_socket.close()
