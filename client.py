import socket
from queue import Queue
from threading import Thread
from command import Command
from message import Message

class Client():
    client_id = 0 # the id given to the client by the Server
    quit = False # flag to shutdown client
    sendable_queue = Queue() # queues for keeping track of messages
    recieved_queue = Queue()

class Connection(Thread):
    def __init__(self, socket):
        Thread.__init__(self)
        self.sock = socket
        self.start()

    def send(self):
        sending_message = Client.sendable_queue.get() # get the next sendable message from the queue
        self.sock.send(sending_message.sendable().encode()) # encode and send

    def recieve(self):
        response = self.sock.recv(4096).decode() # response from server
        recieved_message = Message() # create a message object to store
        recieved_message.parse(response) # parse message into usable format
        Client.recieved_queue.put(recieved_message) # add the message to the message queue

    def run(self):
        while not Client.quit:
            self.send()
            self.recieve()

class Interface(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.start()

    def update(self):
        message = Client.recieved_queue.get()
        print('[{}]: {}'.format(message.sender, message.content))

    def run(self):
        while not Client.quit:
            self.update()
            user_input = input('-> ')
            message = Message(Client.client_id, 0, Command(1), user_input)
            if user_input == '/leave':
                message.command = Command(4) # leave command
                Client.quit = True
            Client.sendable_queue.put(message)

if  __name__ =='__main__':
    # create an ipv4 socket object using the tcp
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 9999))
    init_response = client_socket.recv(4096).decode() # check for initial messages
    Client.client_id = int(init_response) # first message sent from server after connect is id
    print('Connected to server as [{}]'.format(Client.client_id))

    interface = Interface()
    interface.setName('User Interface')

    connection = Connection(client_socket)
    connection.setName('Server Connection')

    interface.join() # dont close until all threads are done
    connection.join()

    client_socket.close()

    print('Exiting...')
