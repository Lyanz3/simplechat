from command import command

class message:
    def __init__(self, sender=0, reciever=0, command=command(1), content='debug text'):
        self.sender = sender
        self.reciever = reciever
        self.command = command
        self.content = content

    def parse(self, raw_protocol):
        self.sender, self.reciever, self.command, self.content = raw_protocol.split(',', 3)

    def sendable(self):
        return('{},{},{},{}'.format(self.sender, self.reciever, self.command, self.content))
