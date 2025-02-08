import socket
import ssl
import tkinter as tk
from tkinter import scrolledtext, messagebox
from cryptography.fernet import Fernet

class ChatClient:
    def __init__(self, aes_key, host = '127.0.0.1', port  = 12345):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.client_socket = ssl.wrap_socket(self.client_socket, certfile = 'client.crt', keyfile = 'client.key')
            self.client_socket.connect((host, port))
            print(f"Connected to {host}:{port}")

        except ssl.SSLError as e:
            print(f"SSL/TLS error {e}")
            messagebox.showerror("Connection Error", f"SSL/TLS error: {e}")
            exit(1)

        except socket.error as e:
            print(f"Socket connection error: {e}")
            messagebox.showerror("Connection Error", f"Socket connection error: {e}")
            exit(1)
        

    def encrypt_msg(self, msg):
        return self.cipher.encrypt(msg.encoded())
    
    def decrypt_msg(self, msg):
        try:
            return self.cipher.decrypt(msg).decode()
        
        except Exception as e:
            print(f"Error decrypting message: {e}")
            return "Error: Unable to decrypt message"
        
    def send_message(self, event = None):
        pass

    def receive_messages(self):
        pass
            