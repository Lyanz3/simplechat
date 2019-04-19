import socket
from queue import Queue
from threading import Thread
from command import Command
from message import Message

# flag to shutdown client
quit = False
# queues for keeping track of messages
sendable_queue = Queue()
recieved_queue = Queue()

class Connection(Thread):
    __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address

    def send(self):
        sending_message = sendable_queue.get() # get the next sendable message from the queue
        self.sock.send(sending_message.sendable().encode()) # encode and send

    def recieve(self):
        response = self.sock.recv(4096).decode() # response from server
        recieved_message = Message() # create a message object to store
        recieved_message.parse(response) # parse message into usable format
        recieved_queue.put(recieved_message) # add the message to the message queue

    def run(self):
        while not quit:
            self.send()
            self.recieve()

class Client(Thread, id):
    __init__(self):
        Thread.__init__(self)
        self.id = id

    def update():
        message = recieved_queue.get()
        print('[{}]: {}'.format(message.sender, message.content))

    def run(self):
        while not quit:
            self.update()
            user_input = input('-> ')
            message = Message(id,,, user_input)
            if user_input == '/leave':
                message.command = Command(4) # leave command
                quit = True
            sendable_queue.put(message)

if  __name__ =='__main__':
    # create an ipv4 socket object using the tcp
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 9999))
    init_response = client_socket.recv(4096).decode() # check for initial messages
    client_id = int(init_response) # first message sent from server after connect is id

    client = Client(client_id)
    client.setName('User Interface')

    connection = Connection(client_socket, client_socket.address)
    connection.setName('Server Connection')

    client.start()
    connection.start()

    client.join()
    connection.join()

    print('Exiting...')
