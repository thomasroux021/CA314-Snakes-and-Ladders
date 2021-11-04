#!/usr/bin/env python3

import socket
import selectors
import types
import json

HOST = "127.0.0.1"
PORT = 4242

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print('accepted connection from', addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            print('closing connection to', data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            sock_data = json.loads(data.outb.decode('utf-8'))
            print('echoing', repr(sock_data), 'to', data.addr)
            sent = sock.send(bytes(json.dumps({'response': sock_data['message']}), encoding='utf-8'))  # Should be ready to write
            data.outb = data.outb[len(data.outb):]

print("starting server...")
sel = selectors.DefaultSelector()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen()
print(f"server running on {HOST}:{PORT}")
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, data=None)

while True:
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj)
        else:
            service_connection(key, mask)