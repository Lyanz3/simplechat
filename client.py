import socket

# create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
# client.connect((target, port))
client.connect(('127.0.0.1', 9999))
response = client.recv(4096).decode() # check for initial messages
print('from server: ', response)

while 1 == 1:
    msg = input('to server: ')
    client.send(msg.encode())

    response = client.recv(4096).decode()
    sender, reciever, command, payload = response.split(',', 3)
    print('from server: ', response)

# hi shawn