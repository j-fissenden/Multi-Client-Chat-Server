import socket
import threading
import ssl

class ChatServer:
    def __init__(self, host = '0.0.0.0', port = 12345):
        self.clients = {}
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        print(f"Server started on {host}:{port}")

        try:
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            context.load_cert_chain(certfile = 'server.crt', keyfile = 'server.key')
            context.verify_mode = ssl.CERT_NONE
            self.server_socket = context.wrap_socket(self.server_socket, server_side = True)

        except Exception as e:
            print(f"SSL error: {e}")
            exit(1)

    def broadcast(self, message, sender = None):
        for user, client in list(self.clients.items()):

            if user != sender:

                try:
                    client.send(message.encode())

                except Exception as e:
                    print(f"Error sending to {user}: {e}")
                    client.close()
                    del self.clients[user]

    def handle_client(self, conn, addr):
        try:
            conn.send("Enter your username: ".encode())
            username = conn.recv(1024).decode().strip()
            self.clients[username] = conn
            self.broadcast(f"{username} has joined the chat.")
            print(f"{username} connected from {addr}")

            while True:
                message = conn.recv(1024).decode()
                if not message:
                    break

                if message.startswith('@'):
                    parts = message.split(' ', 1)

                    if len(parts) == 2:
                        target, msg = parts
                        target = target[1:]

                        if target in self.clients:
                            self.clients[target].send(f"(PM from {username}): {msg}".encode())

                        else:
                            conn.send("User not found.".encode())

                    else:
                        conn.send("Invalid private message format.".encode())

                else:
                    self.broadcast(f"{username}: {message}", sender=username)

        except Exception as e:
            print(f"Error with {username}: {e}")

        finally:
            conn.close()

            if username in self.clients:
                del self.clients[username]
                self.broadcast(f"{username} has left the chat.")
                print(f"{username} disconnected")

    def start(self):
        while True:
            client, addr = self.server_socket.accept()
            threading.Thread(target = self.handle_client, args=(client, addr), daemon = True).start()
