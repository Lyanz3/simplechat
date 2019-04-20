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
        for i in range(0, Server.message_queue.qsize()):
            message = Server.message_queue.get()
            if message.sender == str(self.addr[1]):
                Server.message_queue.put(message)
                continue
            elif message.reciever == '0':
                self.sock.send(message.sendable().encode()) # encode and send
                Server.message_queue.put(message)
                continue
            elif message.reciever == str(self.addr[1]):
                self.sock.send(message.sendable().encode()) # encode and send
                continue # dont put it back in


    def recieve(self):
        request = self.sock.recv(4096).decode()
        recieved_message = Message() # create a message object to store
        recieved_message.parse(request) # parse message into usable format
        Server.message_queue.put(recieved_message) # put the message into the queue
        print('[{}->{}]: {}'.format(recieved_message.sender, recieved_message.reciever, recieved_message.content))

    def run(self):
        t_recieve = Thread(target = self.recieve, args = [])
        t_recieve.start()
        while not Server.quit:
            self.send()
            if not t_recieve.is_alive():
                t_recieve = Thread(target = self.recieve, args = [])
                t_recieve.start()

if  __name__ =='__main__':
    max_clients = 5

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((Server.bind_ip, Server.bind_port))
    server_socket.listen(max_clients)  # connection buffer of 5
    print('Listening on {}:{}'.format(Server.bind_ip, Server.bind_port))

    while True:
        client_socket, address = server_socket.accept()
        connection = Connection(client_socket, address)

    server_socket.close()
