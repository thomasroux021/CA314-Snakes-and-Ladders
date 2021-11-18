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
        sock.setblocking(False)
        print('server connected')
        return sock
    except:
        print(f'connection to server {SERVER_HOST}:{SERVER_PORT} failed')
        time.sleep(timeout)
        connect(timeout)
    
sock = connect()

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

while 1:
    message = input('message to server =')
    sock.sendall(bytes(json.dumps({'type': 'ADD_PLAYER', 'data': {'name': 'Rémi'}}), encoding='utf-8'))
    #sock.sendall(bytes(json.dumps({'type': 'ADD_PIECE', 'data': {'colour': 'red'}}), encoding='utf-8'))
    print("ouiiiiii")
    # data = recvall(sock, 20)
    fulldata = ''
    while True:
        data = sock.recv(4)
        if len(data) <= 0:
            break
        fulldata += data.decode("utf-8")
    print(fulldata)
    server_data = json.loads(fulldata)
    print('server say', server_data)
    # 
    # if (data):
    #     server_data = json.loads(data.decode('utf-8'))
    #     print('server say', server_data)