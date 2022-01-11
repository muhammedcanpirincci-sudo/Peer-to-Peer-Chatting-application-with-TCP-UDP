import socket
import threading

HEADER = 64
PORT = 8958
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISC"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

while True:
    msg = input("send message: ")
    send(msg)
    if msg == DISCONNECT_MESSAGE:
        break