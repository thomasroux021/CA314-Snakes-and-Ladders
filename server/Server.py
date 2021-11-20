import os, sys
import socket
import selectors
import time
import types
import json
from typing import List
from dotenv import load_dotenv

load_dotenv()

class Server:
    __instance = None

    @staticmethod 
    def getInstance():
        """ Static access method. """
        if Server.__instance == None:
            Server()
        return Server.__instance
    
    def __init__(self):
        """ Virtually private constructor. """
        if Server.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Server.__instance = self

    def init(self, removeFct = None, listeningFct = []):
        self.host: str = os.getenv("HOST")
        self.port: str = os.getenv("PORT")
        self.removeFct = removeFct
        self.listeningFct: List[any] = listeningFct
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sel = selectors.DefaultSelector()
        self.start_server()

    def start_server(self, timeout = 5):
        try:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((self.host, int(self.port)))
            self.sock.setblocking(False)
            self.sock.listen()
            print(f"server running on {self.host}:{self.port}")
            self.sel.register(self.sock, selectors.EVENT_READ, data=None)
        except:
            time.sleep(timeout)
            self.start_server(timeout)
    
    def accept_connection(self, sock):
        conn, addr = sock.accept()  # Should be ready to read
        print('accepted connection from', addr)
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(conn, events, data=data)
        conn.send(bytes(json.dumps({'event': 'ME', 'data': {"uid": addr[1]}}), encoding='utf-8'))

    def service_connection(self, key: selectors.SelectorKey, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                data.outb += recv_data
            else:
                if (self.removeFct):
                    self.removeFct(None, data.addr[1])
                print('closing connection to', data.addr)
                self.sel.unregister(sock)
                sock.close()
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                sock_data = json.loads(data.outb.decode('utf-8'))
                print('echoing', repr(sock_data), 'to', data.addr, data.addr[1])
                self.listeningFct[0](sock_data, data.addr[1], sock)
                data.outb = data.outb[len(data.outb):]
   
    @staticmethod
    def send(data, sock):
        sock.send(bytes(json.dumps(data), encoding='utf-8'))
    
    def sendToAll(self, data):
        try:
            for socket, _ in self.sel.select(timeout=None):
                print("socket = ", socket)
                socket.fileobj.send(bytes(json.dumps(data), encoding='utf-8'))
                time.sleep(0.1)
        except:
            print("error")

    def close(self):
        self.sock.close()
        self.sel.close()
    
    def addListeningFct(self, fct):
        self.listeningFct.append(fct)

    def listenEvent(self):
        try:
            while True:
                events = self.sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        self.accept_connection(key.fileobj)
                    else:
                        self.service_connection(key, mask)
        except KeyboardInterrupt:
            sys.exit(0)