import socket
import threading

try:
    serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
except:
    print("Unable to create socket")

hostName = "0.0.0.0"
port = 12345
serverSocket.bind((hostName,port))
serverSocket.listen()

clients = []
nicknames = []

def sendInfo(payLoad):
    for client in clients:
        client.send(bytes(payLoad,'utf-8'))
        
def handleClients(clientSocket):
    while True:
        try:
            data = clientSocket.recv(1024)
            sendInfo(data.decode('utf-8'))
        except:
            index = clients.index(clientSocket)
            clients.remove(clientSocket)
            clientSocket.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            sendInfo('{} has left the chat!'.format(nickname))
            print("{} has disconnected".format(nickname))
            break

def receive():
    while True:
        clientSocket,addr = serverSocket.accept()
        print("Connected to " + str(addr))
        clientSocket.send(bytes("Nickname",'utf-8'))
        nickname = clientSocket.recv(1024)
        clients.append(clientSocket)
        nicknames.append(nickname)
        sendInfo('{} has joined the chat'.format(nickname))
        
        thread = threading.Thread(target=handleClients,args=(clientSocket,))
        thread.start()
    
receive()