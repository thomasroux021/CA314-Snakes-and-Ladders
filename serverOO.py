import socket
import selectors
import types
import json

from server import HOST, PORT

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sel = selectors.DefaultSelector()

        self.sock.bind(self.host, self.port)
        self.sock.setblocking(False)
        self.sock.listen()
        print(f"server running on {self.host}:{self.port}")
        self.sel.register(self.sock, selectors.EVENT_READ, data=None)
        self.listenEvent()
    
    def accept_wrapper(self, sock):
        conn, addr = self.sock.accept()  # Should be ready to read
        print('accepted connection from', addr)
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(conn, events, data=data)

    def service_connection(self, key, mask):
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
    
    def close(self):
        self.sock.close()
        self.sel.close()

    def listenEvent(self):
        while True:
            events = self.sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    self.accept_wrapper(key.fileobj)
                else:
                    self.service_connection(key, mask)


Server(HOST, PORT)