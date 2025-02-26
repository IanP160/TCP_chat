import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print("\n" + message)  # Display messages from the server
        except:
            print("\n[ERROR] Connection lost.")
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 5555))

    # Receive and display the "Enter your username" message from server
    server_message = client_socket.recv(1024).decode()
    print(server_message)  

    username = input("Enter your username: ")
    client_socket.send(username.encode())

    # Start receiving messages
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    while True:
        try:
            message = input()
            if message.lower() == "exit":
                break
            client_socket.send(message.encode())
        except KeyboardInterrupt:
            break

    client_socket.close()

if __name__ == "__main__":
    start_client()
