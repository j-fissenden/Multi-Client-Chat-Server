import socket
import threading
import ssl
from cryptography.fernet import Fernet

class ChatServer:
    def __init__(self, aes_key, host='0.0.0.0', port=12345):
        self.clients = {}  
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server_socket.bind((host, port))
            self.server_socket.listen(5)
            print(f"Server started on {host}:{port}")

        except Exception as e:
            print(f"Error binding to {host}:{port}: {e}")
            exit(1)
        
        try:
            self.server_socket = ssl.wrap_socket(self.server_socket, certfile = 'server.crt', keyfile = 'server.key', server_side = True)
            
        except ssl.SSLError as e:
            print(f"SSL/TLS error: {e}")
            exit(1)

        self.cipher = Fernet(aes_key)

