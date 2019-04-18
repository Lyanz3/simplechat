import socket

# create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
# client.connect((target, port))
client.connect(('127.0.0.1', 9999))

while 1 == 1:
    msg = input('to server: ')
    client.send(msg.encode())
    response = client.recv(4096).decode()
    print('from server: ', response)
