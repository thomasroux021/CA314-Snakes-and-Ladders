#!/usr/bin/env python3

import socket
import time
import json

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 4242

def connect(timeout=5):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((SERVER_HOST, SERVER_PORT))
        print('server connected')
        return sock
    except:
        print(f'connection to server {SERVER_HOST}:{SERVER_PORT} failed')
        time.sleep(timeout)
        connect(timeout)
    
sock = connect()

while 1:
    message = input('message to server =')
    sock.sendall(bytes(json.dumps({'message': message}), encoding='utf-8'))
    data = sock.recv(1024)
    if (data):
        server_data = json.loads(data.decode('utf-8'))
        print('server say', server_data)