import socket
import threading
import sys
from random import randint


HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISC"

global is_connected
is_connected = False # Flag

def get_free_port():
    value = randint(2000, 9000)
    not_in_use = True
    while not_in_use:
        value = randint(2000, 9000)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            not_in_use = s.connect_ex(('localhost', value)) == 0
    return value


PORT = get_free_port()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))


def send_client(conn):
    while True:
        msg = input("Enter Message: ")
        if msg == DISCONNECT_MESSAGE:
            break
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        conn.send(send_length)
        conn.send(message)
    print("Closing connection...")
    conn.close()
    sys.exit() # Kill Thread

def recieve_client(conn):
    while True:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f"{msg}")
            if msg == DISCONNECT_MESSAGE:
                break
    print("Client disconnected")
    sys.exit()  # kill thread

def start_server(contact_thread):
    server.listen()
    print(f"Listening on {SERVER} with port {PORT}")
    while True:
        conn, addr = server.accept()
        print("CONNECTION ESTABLISHED")
        contact_thread.join()
        listening_thread = threading.Thread(target=recieve_client, args=(conn,))
        listening_thread.start()
        messaging_thread = threading.Thread(target=send_client, args=(conn,))
        messaging_thread.start()


def connect_client():
    add = input("Enter Ip address: ")
    port = int(input("Enter Port: "))
    client.connect((add, port))
    print("CONNECTION ESTABLISHED")
    messaging_thread = threading.Thread(target=send_client, args=(client,))
    messaging_thread.start()
    server.close() # Close listening server when connection is established



client_connect_thread = threading.Thread(target=connect_client)
client_connect_thread.start()

start_server(client_connect_thread)