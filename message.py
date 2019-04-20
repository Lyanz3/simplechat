from command import Command

class Message:
    def __init__(self, sender=0, reciever=0, command=Command(1), content='debug text'):
        self.sender = sender
        self.reciever = reciever
        self.command = command
        self.content = content

    def parse(self, raw_protocol):
        try:
            parts = raw_protocol.split(',', 3)
            self.sender = parts[0]
            self.reciever = parts[1]
            if 'Command.NONE' == parts[2]:
                self.command = Command(1)
            if 'Command.WHISPER' == parts[2]:
                self.command = Command(2)
            if 'Command.USERS' == parts[2]:
                self.command = Command(3)
            if 'Command.LEAVE' == parts[2]:
                self.command = Command(4)
            self.content = parts[3]
        except:
            pass

    def sendable(self):
        return('{},{},{},{}'.format(self.sender, self.reciever, self.command, self.content))
