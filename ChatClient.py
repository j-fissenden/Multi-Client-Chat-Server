import socket
import ssl
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

class ChatClient:
    def __init__(self, host = '127.0.0.1', port = 12345):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            self.client_socket = context.wrap_socket(self.client_socket, server_hostname = host)
            self.client_socket.connect((host, port))

        except Exception as e:
            messagebox.showerror("Connection Error", str(e))
            exit(1)

        self.root = tk.Tk()
        self.root.title("Chat Client")
        self.root.geometry("400x500")

        self.chat_display = scrolledtext.ScrolledText(self.root, state ='disabled')
        self.chat_display.pack(expand = True, fill = 'both', padx = 10, pady = 5)

        self.entry_message = tk.Entry(self.root)
        self.entry_message.pack(fill='x', padx = 10, pady = 5)
        self.entry_message.bind('<Return>', self.send_message)

        self.send_button = tk.Button(self.root, text = 'Send', command = self.send_message)
        self.send_button.pack(pady = 5)

        threading.Thread(target = self.receive_messages, daemon = True).start()
        self.root.mainloop()

    def send_message(self, event = None):
        message = self.entry_message.get()

        if message:
            self.client_socket.send(message.encode())
            self.entry_message.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                self.chat_display.config(state = 'normal')
                self.chat_display.insert(tk.END, message + '\n')
                self.chat_display.config(state = 'disabled')
                self.chat_display.yview(tk.END)

            except:
                messagebox.showerror("Error", "Disconnected from server")
                self.client_socket.close()
                break
