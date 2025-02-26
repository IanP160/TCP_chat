import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

def receive_messages(client_socket, text_area):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            text_area.config(state=tk.NORMAL)
            text_area.insert(tk.END, message + "\n")
            text_area.config(state=tk.DISABLED)
        except:
            break

def send_message():
    message = entry.get()
    client_socket.send(message.encode())
    entry.delete(0, tk.END)

def start_client():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 5555))

    username = input("Enter your username: ")
    client_socket.send(username.encode())

    root = tk.Tk()
    root.title(f"Chat - {username}")

    text_area = scrolledtext.ScrolledText(root, state=tk.DISABLED, width=50, height=15)
    text_area.pack()

    entry_frame = tk.Frame(root)
    entry_frame.pack()

    global entry
    entry = tk.Entry(entry_frame, width=40)
    entry.pack(side=tk.LEFT)

    send_button = tk.Button(entry_frame, text="Send", command=send_message)
    send_button.pack(side=tk.RIGHT)

    threading.Thread(target=receive_messages, args=(client_socket, text_area)).start()
    root.mainloop()

start_client()
