CFLAGS= -g
LDFLAGS=
LDFLAGS1=
CC=g++

all: client server

# To make an executable
client: client.o
	$(CC) $(LDFLAGS) -o client client.o

server: server.o
	$(CC) $(LDFLAGS1) -o server server.o

# To make an object from source
.c.o:
	$(CC) $(CFLAGS) -c $*.c

# clean out the dross
clean:
	-rm client server *.o
