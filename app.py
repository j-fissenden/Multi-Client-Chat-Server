import sys
from ChatServer import ChatServer
from ChatClient import ChatClient

if __name__ == "__main__":
    try:
        choice = input("Start server (s) or client (c)? ").strip().lower()
        
        if choice == 's':

            try:
                server = ChatServer()
                server.start()

            except Exception as e:
                print(f"Error starting the server: {e}")
                sys.exit(1)

        elif choice == 'c':

            try:
                client = ChatClient()

            except Exception as e:
                print(f"Error starting the client: {e}")
                sys.exit(1)
                
        else:
            print("Invalid choice. Please enter 's' or 'c'.")
            sys.exit(1)

    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)