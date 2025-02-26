import socket
import threading
import json

VLAN_TABLE = {
    "User1": 10,
    "User2": 10,
    "User3": 20,
    "User4": 20
}

clients = {}

def load_routing_table():
    with open("vlan_routing.json", "r") as file:
        return json.load(file)

def handle_client(client_socket, username):
    vlan = VLAN_TABLE.get(username, None)
    if not vlan:
        print(f"[ERROR] Invalid username: {username}")
        client_socket.send("Invalid VLAN assignment.\n".encode())
        client_socket.close()
        return

    print(f"[CONNECTED] {username} joined VLAN {vlan}")
    client_socket.send(f"Welcome {username}! You are in VLAN {vlan}.\n".encode())

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            print(f"[MESSAGE RECEIVED] {username}: {message}")

            to_username, msg = message.split(":", 1)
            if to_username in clients:
                to_vlan = VLAN_TABLE.get(to_username)
                routing_table = load_routing_table()

                if vlan == to_vlan or routing_table.get(f"{vlan}_{to_vlan}", False):
                    clients[to_username].send(f"{username}: {msg}".encode())
                else:
                    client_socket.send("VLAN Restriction: Cannot communicate with this user.\n".encode())
            else:
                client_socket.send("User not found.\n".encode())

        except Exception as e:
            print(f"[ERROR] {username} disconnected: {e}")
            break

    print(f"[DISCONNECTED] {username}")
    del clients[username]
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 5555))
    server.listen(5)
    print("[SERVER STARTED] Listening for connections...")

    while True:
        client_socket, addr = server.accept()
        print(f"[NEW CONNECTION] {addr} connected.")

        client_socket.send("Enter your username: ".encode())
        username = client_socket.recv(1024).decode().strip()
        
        if username in VLAN_TABLE:
            clients[username] = client_socket
            client_socket.send("Connected successfully!\n".encode())
            threading.Thread(target=handle_client, args=(client_socket, username)).start()
        else:
            client_socket.send("Invalid username.\n".encode())
            client_socket.close()

start_server()
