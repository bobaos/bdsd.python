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

    def _handleIncomingNotify(self, response):
        payload = response['payload']
        if payload == 'bus connected':
            self.emit('connected')
    def _handleIncomingValue(self, response):
        payload = response['payload']
        self.emit('value', payload)
    def _handleIncomingResponse(self, response):
        # TODO: find origin request and callback
        pass

    def handle_read(self):
        data = self.recv(8192)
        print(data)
        parsed = _bdsm.parse(data)
        print(parsed[2])
        response = json.loads(parsed[2])
        method = response['method']
        if method == 'notify':
            self._handleIncomingNotify(response)
        elif method == 'cast value':
            self._handleIncomingValue(response)
        else:
            self._handleIncomingResponse(response)

    # def writable(self):
    #     return

    def handle_write(self):
        sent = self.send('hello')

    # BDSD Client methods
    def _sendData(self, data):
        msg = _bdsm.compose(data)
        self.send(msg)

    def _composeDataStr(self, method, payload):
        data = {}
        data['request_id'] = round(random.random() * 1000)
        data['method'] = method
        data['payload'] = payload
        return data

    def setValue(self, id, value, cb):
        # define request
        print('set value')
        method = 'set value'
        payload = {}
        payload['id'] = id
        payload['value'] = value
        # compose and send
        msg = self._composeDataStr(method, payload)
        # request = msg['request_id'], cb
        # self._requests.append(request)
        # print(request)
        # print(request)
        # TODO: register callback in self._requests
        msgStr = json.dumps(msg)
        self._sendData(msgStr)

SOCKFILE = os.environ.copy()['XDG_RUNTIME_DIR'] + '/bdsd.sock'
myClient = BDSDClient(SOCKFILE)
print('starting async')


@myClient.on('connected')
def handle_connected():
    print('myClient is connected, great then')
    myClient.setValue(103, False, 1)


@myClient.on('value')
def handle_broadcasted_value(data):
    print('broadcasted value')
    print(data)


asyncore.loop()
