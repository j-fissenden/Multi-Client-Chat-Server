import socket
import ssl
import tkinter as tk
from tkinter import scrolledtext, messagebox
from cryptography.fernet import Fernet

class ChatClient:
    def __init__(self, aes_key, host = '127.0.0.1', port  = 12345):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


        # Add GUI and connection SSL
        pass

    def encrypt_msg(self, msg):
        return self.cipher.encrypt(msg.encoded())
    
    def decrypt_msg(self, msg):
        try:
            return self.cipher.decrypt(msg).decode()
        
        except Exception as e:
            print(f"Error decrypting message: {e}")
            return "Error: Unable to decrypt message"
            