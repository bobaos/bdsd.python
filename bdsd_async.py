import asyncore
import socket
import os
import sys
import signal
import random
import json
import _bdsm
from pyee import EventEmitter


class BDSDClient(asyncore.dispatcher, EventEmitter):
    def __init__(self, path):
        asyncore.dispatcher.__init__(self)
        EventEmitter.__init__(self)

        self.create_socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.connect(path)

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        print(self.recv(8192))

    # def writable(self):
    #     return

    def handle_write(self):
        sent = self.send('hello')


client = BDSDClient('/run/user/1000/bdsd.sock')
print('starting async')
asyncore.loop()

