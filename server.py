import socket, threading

host = "192.168.0.30"
port = 8000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
usernames = []
keys = []


def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            username=usernames[clients.index(client)]
            key=keys[clients.index(client)]
            clients.remove(client)
            client.close()
            broadcast('{} has left the chatroom.'.format(username).encode('ascii'))
            usernames.remove(username)
            keys.remove(key)
            break

def receive():
    clientA, address = server.accept()
    print("Connection received from {}".format(str(address)))
    username = clientA.recv(1024).decode('ascii')
    usernames.append(username)
    publicKeyA=clientA.recv(1024).decode()
    keys.append(publicKeyA)
    print(publicKeyA)
    clients.append(clientA)
    print("Username set as {}".format(username))
    

    clientB, address = server.accept()
    print("Connection received from {}".format(str(address)))
    username = clientB.recv(1024).decode('ascii')
    usernames.append(username)
    publicKeyB=clientB.recv(1024).decode()
    keys.append(publicKeyB)
    clients.append(clientB)
    print("Username set as {}".format(username))

    clientB.send(publicKeyA.encode())
    clientA.send(publicKeyB.encode())
    

    for c in clients:
        thread = threading.Thread(target=handle, args=(c,))
        thread.start()

receive()
