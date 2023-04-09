import asyncio
import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

# create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the Unity machine
sock.connect((HOST, PORT))

# callback = lambda message: None

# async def handle_messages(sock, callback):
#     # Infinite loop to handle incoming messages
#     while True:
#         data = await loop.sock_recv(sock, 1024)
#         if not data:
#             # Connection closed
#             break
#         # Process the incoming message
#         message = data.decode()
#         print(f"Received message from Unity: {message}")
#         callback(message)

# # Start the message handling task
# loop = asyncio.get_event_loop()
# loop.create_task(handle_messages(sock, callback))

def SendMessage(message):
    # send the message to Unity
    sock.sendall(message.encode())

def CloseSocket():
    # Stop the event loop and close the socket
    # loop.stop()
    sock.close()
    print("Socket Closed.")

# loop.run_forever()