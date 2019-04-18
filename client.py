import socket
from command import command
from message import message

# create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
# client.connect((target, port))
client.connect(('127.0.0.1', 9999))
# todo add multithreading
response = client.recv(4096).decode() # check for initial messages
print('from server: ', response)

while 1 == 1:
    msg = input('to server: ')
    sending_message = message(5123, 0, command(1), msg)
    client.send(sending_message.sendable().encode())
    print('-->')

    response = client.recv(4096).decode() # response from server
    recieved_message = message() # create a message object to store
    recieved_message.parse(response) # parse message into usable format

    if recieved_message.reciever == 'b':
        print('[{}]: {}'.format(recieved_message.sender, recieved_message.content))
    else:
        print('[{}->ME]: {}'.format(recieved_message.sender, recieved_message.content))
