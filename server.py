import socket
from threading import *
from message import message
from command import command
import queue

bind_ip = '127.0.0.1' #127.0.0.1:9999
bind_port = 9999
message_queue = queue.Queue()

#socket server;
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)  # connection buffer of 5

print('Listening on {}:{}'.format(bind_ip, bind_port))

class connection(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()

    def run(self):
        self.sock.send('You are {}'.format(self.addr[1]).encode())
        while 1 == 1: # while socket is alive just keep reusing it
            request = self.sock.recv(1024).decode()
            recieved_message = message() # create a message object to store
            recieved_message.parse(request) # parse message into usable format
            message_queue.put(recieved_message) # put the message into the queue
            print('recieved message')

            message_queue.join() # send all messages that are listed to host
            for m in message_queue:
                if m.sender == self.addr[1] or m.sender == 0:
                    self.sock.send(m.sendable().encode())
            message_queue.task_done() # mutex for thread safety

while 1 == 1: # run loop forever
    client_sock, address = server.accept()
    print('{}:{} has connected to the server!'.format(address[0], address[1]))
    connection(client_sock, address)
    if message_queue.qsize() > 100: # limit message queue to 100 messages
        message_queue.pop()
    #client_sock.close()
