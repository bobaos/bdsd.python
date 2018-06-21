import os
import sys
import signal
import socket
import random
import json
import _bdsm
from pyee import EventEmitter



class BdsdClient(EventEmitter):
    def __init__(self, sockfile):
        # super(BdsdClient, self).__init__()
        EventEmitter.__init__(self)
        # StoppableThread.__init__(self)

        self._should_be_killed = False
        signal.signal(signal.SIGINT, self._kill)
        signal.signal(signal.SIGTERM, self._kill)

        self._requests = []
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.setblocking(0)
        self.sockfile = sockfile
        print('BdsdClient: connecting to: ' + self.sockfile)
        _connected = False
        while not _connected:
            try:
                self.sock.connect(self.sockfile)
                _connected = True
                self._processIncomingMessages()
            except socket.error as msg:
                # print(msg)
                pass
    def _kill(self, signum, frame):
        print('should be killed soon')
        self._should_be_killed = True
    def run(self):
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

    def _prosessIncomingNotify(self, response):
        payload = response['payload']
        if payload == 'bus connected':
            print('emitting connected event')
            self.emit('connected', self)

        pass
    def _processIncomingResponse(self, response):
        pass
    def _processIncomingMessages(self):
        while True:
            if self._should_be_killed:
                print('trying to kill')
                break
            try:
                data = self.sock.recv(1048)
                parsed = _bdsm.parse(data)
                print(parsed[2])
                response = json.loads(parsed[2])
                method = response['method']
                payload = response['payload']
                if method == 'notify':
                    self._prosessIncomingNotify(response)
                else:
                    self._processIncomingResponse(response)
                # TODO: parse response
                # print(response['response_id'])
                # TODO: callback from self._requests
            except socket.error:
                #print('error')
                pass
            except socket.timeout:
                #print('timeout')
                pass
            except IOError as e:
                pass


SOCKFILE = os.environ.copy()['XDG_RUNTIME_DIR'] + '/bdsd.sock'
mySock = BdsdClient(SOCKFILE)
# mySock.start()
print('hello')

def test():
    print("test")

def connected_handler(client):
    print('Connected to: ' + client.sockfile)
    mySock.setValue(101, 0, test)

print('register connected handler')
mySock.on('connected', connected_handler)


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
