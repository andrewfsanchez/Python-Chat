import socket, threading, re, random
from AESCipher import AESCipher

username = input("Input username: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #socket initialization
client.connect(('192.168.0.30', 8000))                             #connecting client to server

p = 23
g = 5

client.send(username.encode('ascii'))
privateKey=random.randrange(1,p)
print(privateKey)
publicKey= g ** privateKey % p
print(publicKey)
client.send(str(publicKey).encode())
peerPublicKey = int(client.recv(1024).decode())
print(peerPublicKey)
secret = peerPublicKey ** privateKey % p
print(secret)
cipher = AESCipher(str(secret))

def receive():
    while True:                                                 #making valid connection
        try:
            encodedMessage=client.recv(1024)
            message = cipher.decrypt(encodedMessage)
            print(message)
        except:                                                 #case on wrong ip/port details
           1+1
def write():
    while True:                                                 #message layout
        message = '{}: {}'.format(username, input(''))
        cipher = AESCipher(str(secret))
        message = cipher.encrypt(message)
        client.send(message)

receive_thread = threading.Thread(target=receive)               #receiving multiple messages
receive_thread.start()
write_thread = threading.Thread(target=write)                   #sending messages 
write_thread.start()