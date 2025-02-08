import socket
import threading
import ssl
import tkinter as tk
from tkinter import scrolledtext, messagebox
from Crypto.Cipher import AES
import base64

BLOCK_SIZE = 16  

class ChatClient:
    def __init__(self, aes_key, host='127.0.0.1', port=12345):
        self.aes_key = aes_key
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.client_socket = ssl.wrap_socket(self.client_socket, certfile='client.crt', keyfile='client.key')
            self.client_socket.connect((host, port))
            print(f"Connected to {host}:{port}")
            
        except Exception as e:
            print(f"Connection error: {e}")
            messagebox.showerror("Connection Error", str(e))
            exit(1)

        self.root = tk.Tk()
        self.root.title("Chat Client")
        self.root.geometry("400x500")

        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.chat_display.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
        self.chat_display.config(state=tk.DISABLED)

        self.entry_message = tk.Entry(self.root)
        self.entry_message.pack(padx=10, pady=5, fill=tk.X)
        self.entry_message.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

        threading.Thread(target=self.receive_messages, daemon=True).start()
        self.root.mainloop()

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

    def send_message(self, event=None):
        message = self.entry_message.get()
        self.client_socket.send(self.encrypt_msg(message).encode())
        self.entry_message.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                message = self.decrypt_msg(self.client_socket.recv(1024).decode())
                self.chat_display.config(state=tk.NORMAL)
                self.chat_display.insert(tk.END, message + "\n")
                self.chat_display.config(state=tk.DISABLED)
                self.chat_display.yview(tk.END)

            except:
                messagebox.showerror("Error", "Disconnected from server")
                self.client_socket.close()
                break
