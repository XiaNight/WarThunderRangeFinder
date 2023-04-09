import asyncio
import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

# create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the Unity machine
sock.connect((HOST, PORT))

def SendMessage(message):
    # send the message to Unity
    sock.sendall(message.encode())

def CloseSocket():
    # close the socket
    sock.close()
    print("Socket Closed.")