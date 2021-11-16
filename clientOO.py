import socket
import time
import json

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 4242

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()
        
    def connect(self, timeout=5):
        try:
            self.sock.connect((self.host, self.port))
            print('server connected')
        except:
            print(f'connection to server {SERVER_HOST}:{SERVER_PORT} failed')
            time.sleep(timeout)
            self.connect(timeout)
        self.sendMessage()
    
    def sendMessage(self):
        while 1:
            message = input('message to server =')
            self.sock.sendall(bytes(json.dumps({'message': message}), encoding='utf-8'))
            data = self.sock.recv(1024)
            if (data):
                server_data = json.loads(data.decode('utf-8'))
                print('server say', server_data)
       
Client(SERVER_HOST, SERVER_PORT)