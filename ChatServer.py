import socket
import threading
import ssl
from cryptography.fernet import Fernet

class ChatServer:
    def __init__(self, aes_key, host = '0.0.0.0', port = 12345):
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

    def broadcast(self, message, sender = None):
        encrypted_msg = self.cipher.encrypt(message.encode())
        for user, client in self.clients.items():
            try:
                if user != sender:
                    client.send(encrypted_msg)
            except Exception as e:
                print(f"Error sending message to {user}: {e}")
                client.close()
                del self.clients[user]

    def handle_client(self, conn, addr):
        try:
            conn.send(self.cipher.encrypt("Enter your username: ".encode()))
            username = self.cipher.decrypt(conn.recv(1024)).decode()
            self.clients[username] = conn
            print(f"{username} joined from {addr}")
            self.broadcast(f"{username} has joined the chat.")

        except Exception as e:
            print(f"Error handling new client {addr}: {e}")
            conn.close()

            return

        while True:
            try:
                message = self.cipher.decrypt(conn.recv(1024)).decode()
                if not message:
                    break

                if message.startswith('@'):
                    target, msg = message.split(' ', 1)
                    target = target[1:]

                    if target in self.clients:
                        self.clients[target].send(self.cipher.encrypt(f"(PM) from {username}: {msg}".encode()))
                    
                    else:
                        conn.send(self.cipher.encrypt("User not found.".encode()))

                else:
                    self.broadcast(f"{username}: {message}", sender = username)
            
            except Exception as e:
                print(f"Error handling message from {username}: {e}")
                break

            try:
                conn.close()

            except Exception as e:
                print(f"Error closing connection with {username}: {e}")
            
            finally:
                del self.clients[username]
                self.broadcast(f"{username} has left the chat.")

    def start(self):
        while True:
            try:
                client, addr = self.server_socket.accept()
                client_thread = threading.Thread(target = self.handle_client, args = (client, addr))
                client_thread.start()
            
            except Exception as e:
                print(f"Error accepting new client: {e}")
                continue