import os
import socket
import time
import json
from dotenv import load_dotenv
import sys

load_dotenv()

class Client:
    __instance = None

    @staticmethod 
    def getInstance():
        """ Static access method. """
        if Client.__instance == None:
            Client()
        return Client.__instance
    
    def __init__(self):
        """ Virtually private constructor. """
        if Client.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Client.__instance = self

    def init(self, fct):
        self.host = os.getenv("HOST")
        self.port = os.getenv("PORT")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_event_fct = fct
        self.connect()
        
    def connect(self, timeout=5):
        try:
            self.sock.connect((self.host, int(self.port)))
            self.sock.settimeout(0.06)
        except:
            print(f'connection to server {self.host}:{self.port} failed')
            time.sleep(timeout)
            self.connect(timeout)

    def send(self, data):
        try:
            self.sock.send(bytes(json.dumps(data), encoding='utf-8'))
        except:
            print("error")
    
    def set_event_fct(self, fct):
        self.set_event_fct = fct
    
    def receive(self):
        try:
            data = self.sock.recv(4096)
            if (data):
                server_data = json.loads(data.decode('utf-8'))
                print('server say', str(server_data))
                if self.set_event_fct:
                    self.set_event_fct(server_data)
        except socket.timeout:
            pass
        except socket.error:
            print("socket error")
        else:
            if len(data) == 0:
                print('orderly shutdown on server end')
                sys.exit(0)

# Client.getInstance().init()
# Client.getInstance().receive()