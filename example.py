import os
import asyncore
from bdsd_async import BDSDClient

SOCKFILE = os.environ.copy()['XDG_RUNTIME_DIR'] + '/bdsd.sock'
myClient = BDSDClient(SOCKFILE)


@myClient.on('connected')
def handle_connected():
    print('myClient is connected, great then')
    request = myClient.getValue(1)

    @request.on('success')
    def success(payload):
        print(payload)

    @request.on('error')
    def handle_error(e):
        print(e)


@myClient.on('value')
def handle_broadcasted_value(data):
    print('broadcasted value')
    print(data)

myClient.loop()
