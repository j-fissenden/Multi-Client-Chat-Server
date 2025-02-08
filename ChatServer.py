import socket
import threading
import ssl
from cryptography.fernet import Fernet

class ChatServer:
    def __init__(self, aes_key, host = '0.0.0.0', port = 12345):
        self.clients = {}
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.server_socket = ssl.wrap_socket(self.server_socket, certfile = 'server.crt', keyfile = 'server.key', server_side = True)
        
        self.cipher = Fernet(aes_key)
        print(f"Server started on {host}:{port}")
