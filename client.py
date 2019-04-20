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
        if not Client.sendable_queue.empty():
            sending_message = Client.sendable_queue.get() # get the next sendable message from the queue
            self.sock.send(sending_message.sendable().encode()) # encode and send

    def recieve(self):
        response = self.sock.recv(4096).decode() # response from server
        recieved_message = Message() # create a message object to store
        recieved_message.parse(response) # parse message into usable format
        Client.recieved_queue.put(recieved_message) # add the message to the message queue

    def run(self): # some weird stuff with more threads because .recv blocks
        t_recieve = Thread(target = self.recieve, args = [])
        t_recieve.start()
        while not Client.quit:
            self.send()
            if not t_recieve.is_alive():
                t_recieve = Thread(target = self.recieve, args = [])
                t_recieve.start()

if  __name__ =='__main__':
    # create an ipv4 socket object using the tcp
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 9999))
    init_response = client_socket.recv(4096).decode() # check for initial messages
    Client.client_id = int(init_response) # first message sent from server after connect is id
    print('Connected to server as [{}]'.format(Client.client_id))

    connection = Connection(client_socket)
    connection.setName('Server Connection')

    while not Client.quit:
        if not Client.recieved_queue.empty(): # update messages from queue
            message = Client.recieved_queue.get()
            print('[{}]: {}'.format(message.sender, message.content))

        user_input = input('-> ') # get user input
        if user_input == '/leave':
            Client.sendable_queue.put(Message(Client.client_id, 0, Command(4), '{} is leaving the server!'.format(Client.client_id)))
            Client.quit = True
            print('Quit Sucessful!')
            continue
        elif user_input == '/users': #displays all usernames
            Client.sendable_queue.put(Message(Client.client_id, 70000, Command(3),'giff message'))
            print('Getting user list from server...')
            continue
        elif user_input.split(' ')[0] == '/w': # if the first part of a string separated by spaces is /w
            reciever = user_input.split(' ')[1]  # use to find reciever
            payload = ' '.join(user_input.split(' ')[2:]) #get everything after the reciever
            Client.sendable_queue.put(Message(Client.client_id, reciever, Command(2), payload))
            continue

        message = Message(Client.client_id, 0, Command(1), user_input)
        Client.sendable_queue.put(message)

    connection.join()
    client_socket.close()
    print('Exiting...')
