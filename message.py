from command import Command

class Message:
    def __init__(self, sender=0, reciever=0, command=Command(1), content='debug text'):
        self.sender = sender
        self.reciever = reciever
        self.command = command
        self.content = content

    def parse(self, raw_protocol):
        try:
            self.sender, self.reciever, self.command, self.content = raw_protocol.split(',', 3)
        except:
            pass

    def sendable(self):
        return('{},{},{},{}'.format(self.sender, self.reciever, self.command, self.content))
