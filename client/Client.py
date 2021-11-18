import os
import socket
import time
import json
from dotenv import load_dotenv

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

    def init(self):
        self.host = os.getenv("HOST")
        self.port = os.getenv("PORT")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()
        
    def connect(self, timeout=5):
        try:
            self.sock.connect((self.host, int(self.port)))
            print('server connected')
        except:
            print(f'connection to server {self.host}:{self.port} failed')
            time.sleep(timeout)
            self.connect(timeout)

    def send(self, data):
        try:
            self.sock.send(bytes(json.dumps({'message': data}), encoding='utf-8'))
        except:
            print("error")
    
    def receive(self):
        while 1:
            data = self.sock.recv(1024)
            if (data):
                server_data = json.loads(data.decode('utf-8'))
                print('server say', str(server_data))

# Client.getInstance().init()
# Client.getInstance().receive()