import socket
import threading
import ssl
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

BLOCK_SIZE = 16  # AES block size

class ChatServer:
    def __init__(self, aes_key, host='0.0.0.0', port=12345):
        self.aes_key = aes_key
        self.clients = {}  

        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((host, port))
            self.server_socket.listen(5)
            print(f"Server started on {host}:{port}")

        except Exception as e:
            print(f"Error binding to {host}:{port}: {e}")
            exit(1)

        try:
            self.server_socket = ssl.wrap_socket(self.server_socket, certfile='server.crt', keyfile='server.key', server_side=True)
            
        except ssl.SSLError as e:
            print(f"SSL/TLS error: {e}")
            exit(1)

    def pad(self, msg):
        padding_length = BLOCK_SIZE - len(msg) % BLOCK_SIZE

        return msg + (chr(padding_length) * padding_length).encode()

    def unpad(self, msg):
        return msg[:-ord(msg[-1:])]

    def encrypt_msg(self, message):
        iv = get_random_bytes(16)
        cipher = AES.new(self.aes_key, AES.MODE_CBC, iv)
        encrypted = cipher.encrypt(self.pad(message.encode()))

        return base64.b64encode(iv + encrypted).decode()

    def decrypt_msg(self, encrypted_message):
        encrypted_message = base64.b64decode(encrypted_message)
        iv = encrypted_message[:16]
        cipher = AES.new(self.aes_key, AES.MODE_CBC, iv)
        decrypted = self.unpad(cipher.decrypt(encrypted_message[16:]))

        return decrypted.decode()

    def broadcast(self, message, sender=None):
        encrypted_msg = self.encrypt_msg(message)

        for user, client in list(self.clients.items()):
            try:
                if user != sender:
                    client.send(encrypted_msg.encode())
            except Exception as e:
                print(f"Error sending message to {user}: {e}")
                client.close()
                del self.clients[user]

    def handle_client(self, conn, addr):
        try:
            conn.send(self.encrypt_msg("Enter your username: ").encode())
            username = self.decrypt_msg(conn.recv(1024).decode())
            self.clients[username] = conn
            print(f"{username} joined from {addr}")
            self.broadcast(f"{username} has joined the chat.")

            while True:
                try:
                    message = self.decrypt_msg(conn.recv(1024).decode())
                    if not message:
                        break

                    if message.startswith('@'):
                        target, msg = message.split(' ', 1)
                        target = target[1:]

                        if target in self.clients:
                            self.clients[target].send(self.encrypt_msg(f"(PM) from {username}: {msg}").encode())
                        else:
                            conn.send(self.encrypt_msg("User not found.").encode())
                    else:
                        self.broadcast(f"{username}: {message}", sender=username)

                except Exception as e:
                    print(f"Error handling message from {username}: {e}")
                    break

        finally:
            print(f"{username} disconnected")
            conn.close()
            del self.clients[username]
            self.broadcast(f"{username} has left the chat.")

    def start(self):
        while True:
            try:
                client, addr = self.server_socket.accept()
                threading.Thread(target=self.handle_client, args=(client, addr), daemon=True).start()

            except Exception as e:
                print(f"Error accepting new client: {e}")
