from ChatServer import ChatServer
from ChatClient import ChatClient
import sys
from Crypto.Random import get_random_bytes

def generate_aes_key():
    return get_random_bytes(32)

if __name__ == "__main__":
    try:
        aes_key = generate_aes_key()

        choice = input("Start server (s) or client (c)? ").strip().lower()
        
        if choice == 's':
            try:
                server = ChatServer(aes_key)
                server.start()
            except Exception as e:
                print(f"Error starting the server: {e}")
                sys.exit(1)

        elif choice == 'c':
            try:
                client = ChatClient(aes_key)

            except Exception as e:
                print(f"Error starting the client: {e}")
                sys.exit(1)

        else:
            print("Invalid choice. Please enter 's' to start the server or 'c' to start the client.")
            sys.exit(1)

    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)