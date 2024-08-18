import socket
import threading

try:
    clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
except:
    print("Unable to create socket")
    
nickname = input("Enter your nickname: ")
    
hostName = input("Enter the hostname : ")
port = int(input("Enter the port number : "))

clientSocket.connect((hostName,port))

def receive():
    while True:
        data = clientSocket.recv(1024)
        if(data.decode('utf-8') == "Nickname"):
            clientSocket.send(bytes(nickname,'utf-8'))
        else:
            print(data)

def send():
    while True:
        msg = "{} : {}".format(nickname,input(""))
        clientSocket.send(bytes(msg,'utf-8'))

receiveThread = threading.Thread(target=receive)
receiveThread.start()

sendThread = threading.Thread(target=send)
sendThread.start()