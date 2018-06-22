import asyncore
import socket
import random
import json
import _bdsm
from pyee import EventEmitter


class BDSDClient(asyncore.dispatcher, EventEmitter):
    def __init__(self, path):
        asyncore.dispatcher.__init__(self)
        EventEmitter.__init__(self)

        self._requests = []
        self.create_socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.connect(path)
    def loop(self):
        asyncore.loop()
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
        for responseEmitter in self._requests:
            if responseEmitter.id == response['response_id']:
                index = self._requests.index(responseEmitter)
                # TODO: check for errors
                if response['success']:
                    responseEmitter.emit('success', response['payload'])
                else:
                    responseEmitter.emit('error', response['error'])
            self._requests.pop(index)
        pass

    def handle_read(self):
        data = self.recv(8192)
        parsed = _bdsm.parse(data)
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

    def getDatapoints(self):
        # define request
        method = 'get datapoints'
        payload = {}
        # compose and send
        msg = self._composeDataStr(method, payload)
        responseEmitter = EventEmitter()
        responseEmitter.id = msg['request_id']
        self._requests.append(responseEmitter)
        msgStr = json.dumps(msg)
        self._sendData(msgStr)
        return responseEmitter
    def getDescription(self, id):
        method = 'get description'
        payload = {}
        payload['id'] = id
        msg = self._composeDataStr(method, payload)
        responseEmitter = EventEmitter()
        responseEmitter.id = msg['request_id']
        self._requests.append(responseEmitter)
        msgStr = json.dumps(msg)
        self._sendData(msgStr)
        return responseEmitter
    def setValue(self, id, value):
        # define request
        method = 'set value'
        payload = {}
        payload['id'] = id
        payload['value'] = value
        # compose and send
        msg = self._composeDataStr(method, payload)
        responseEmitter = EventEmitter()
        responseEmitter.id = msg['request_id']
        self._requests.append(responseEmitter)
        msgStr = json.dumps(msg)
        self._sendData(msgStr)
        return responseEmitter
    def getValue(self, id):
        method = 'get value'
        payload = {}
        payload['id'] = id
        msg = self._composeDataStr(method, payload)
        responseEmitter = EventEmitter()
        responseEmitter.id = msg['request_id']
        self._requests.append(responseEmitter)
        msgStr = json.dumps(msg)
        self._sendData(msgStr)
        return responseEmitter
    def getStoredValue(self, id):
        method = 'get stored value'
        payload = {}
        payload['id'] = id
        msg = self._composeDataStr(method, payload)
        responseEmitter = EventEmitter()
        responseEmitter.id = msg['request_id']
        self._requests.append(responseEmitter)
        msgStr = json.dumps(msg)
        self._sendData(msgStr)
        return responseEmitter
    def readValue(self, id):
        method = 'read value'
        payload = {}
        payload['id'] = id
        msg = self._composeDataStr(method, payload)
        responseEmitter = EventEmitter()
        responseEmitter.id = msg['request_id']
        self._requests.append(responseEmitter)
        msgStr = json.dumps(msg)
        self._sendData(msgStr)
        return responseEmitter


