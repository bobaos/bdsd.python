import os
import sys
import socket
import random
import json
import _bdsm


# import _set_timeout


class BdsdClient:
    def __init__(self, sockfile, callback):
        self._requests = []
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sockfile = sockfile
        self.connectedCallback = callback
        print('BdsdClient: connecting to: ' + sockfile)
        connected = False
        while not connected:
            try:
                self.sock.connect(self.sockfile)
                connected = True
            except socket.error as msg:
                # print(msg)
                pass
        self._processIncomingMessages()

    def _sendData(self, data):
        msg = _bdsm.compose(data)
        self.sock.sendall(msg)

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
        request = msg['request_id'], cb
        self._requests.append(request)
        print(request)
        print(request)
        # TODO: register callback in self._requests
        msgStr = json.dumps(msg)
        self._sendData(msgStr)

    def _processIncomingMessages(self):
        while True:
            try:
                data = self.sock.recv(2048)
                parsed = _bdsm.parse(data)
                print(parsed[2])
                response = json.loads(parsed[2])
                print(response['method'])

                # print(response['response_id'])
                # TODO: callback from self._requests
            except IOError as e:
                pass


def processSetValue(err, res):
    print(err)
    print(res)


def connected(client):
    print('Connected to: ' + client.sockfile)
    client.setValue(101, False, processSetValue)


SOCKFILE = os.environ.copy()['XDG_RUNTIME_DIR'] + '/bdsd.sock'
mySock = BdsdClient(SOCKFILE, connected)

# def setValue(id, value):
#     request_id = random.random()*1000
#     method = 'set value'
#     payload = {}
#     payload['id'] = id
#     payload['value'] = value
#     jsonObj = {}
#     jsonObj['request_id'] = request_id
#     jsonObj['method'] = method
#     jsonObj['payload'] = payload
#     jsonStr = json.dumps(jsonObj)
#     msg = composeBDSMFrame(jsonStr)
#     print(msg)
#     sock.sendall(msg)
