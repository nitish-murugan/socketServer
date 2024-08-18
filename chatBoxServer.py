import socket
import threading
import os

# Predefined secret key for the client
SECRET_KEY = "key321"

try:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except Exception as e:
    print(f"Unable to create socket: {e}")
    exit(1)

hostName = "0.0.0.0"
port = int(os.environ.get('PORT', 8000))
serverSocket.bind((hostName, port))
serverSocket.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except Exception as e:
            print(f"Error sending message: {e}")
            remove_client(client)

def handle_client(clientSocket):
    while True:
        try:
            message = clientSocket.recv(1024)
            if message:
                broadcast(message)
            else:
                remove_client(clientSocket)
                break
        except Exception as e:
            print(f"Error handling client: {e}")
            remove_client(clientSocket)
            break

def remove_client(clientSocket):
    if clientSocket in clients:
        index = clients.index(clientSocket)
        clients.remove(clientSocket)
        nickname = nicknames[index]
        nicknames.remove(nickname)
        clientSocket.close()
        broadcast(f'{nickname.decode("utf-8")} has left the chat!'.encode('utf-8'))
        print(f"{nickname.decode('utf-8')} has disconnected")

def receive():
    while True:
        try:
            clientSocket, addr = serverSocket.accept()
            print(f"Connected to {addr}")

            # Expect the secret key from the client
            clientSocket.send("Secret Key:".encode('utf-8'))
            client_key = clientSocket.recv(1024).decode('utf-8')

            if client_key == SECRET_KEY:
                clientSocket.send("Nickname".encode('utf-8'))
                nickname = clientSocket.recv(1024)

                if nickname:
                    nicknames.append(nickname)
                    clients.append(clientSocket)
                    print(f"Nickname of the client is {nickname.decode('utf-8')}")
                    broadcast(f'{nickname.decode("utf-8")} has joined the chat!'.encode('utf-8'))
                    
                    thread = threading.Thread(target=handle_client, args=(clientSocket,))
                    thread.start()
                else:
                    clientSocket.close()
            else:
                print("Client provided incorrect secret key. Connection refused.")
                clientSocket.send("Invalid secret key. Connection refused.".encode('utf-8'))
                clientSocket.close()
        except Exception as e:
            print(f"Error accepting connections: {e}")

receive()
