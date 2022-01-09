import socket
import threading
from random import randint


HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISC"

is_connected = False # Flag

def get_free_port():
    value = randint(2000, 9000)
    not_in_use = True
    while not_in_use:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            not_in_use = s.connect_ex(('localhost', value)) == 0
    return value


PORT = get_free_port()


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

def recieve_client(conn):
    is_connected = True
    while is_connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f"{msg}")
            if msg == DISCONNECT_MESSAGE:
                is_connected = False
    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER, PORT))
    server.listen()
    print(f"Listening on {SERVER} with port {PORT}")
    while True:
        conn, addr = server.accept()
        print("CONNECTION ESTABLISHED")
        listening_thread = threading.Thread(target=recieve_client, args=(conn,))
        listening_thread.start()
        messaging_thread = threading.Thread(target=send_client, args=(conn,))
        messaging_thread.start()

def connect_client(add, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((add, port))
    print("CONNECTION ESTABLISHED")
    listening_thread = threading.Thread(target=recieve_client, args=(client,))
    listening_thread.start()
    messaging_thread = threading.Thread(target=send_client, args=(client,))
    messaging_thread.start()


listening_thread = threading.Thread(target=start_server)
listening_thread.start()

# The problem is that the listening Client thread is still waiting for a response from the user
# to fix this, once the user establishes a connection, that thread should be killed

if not is_connected:
    add = input("enter add:" )
    port = int(input("enter port: "))
    connect_client(add, port)
    is_connected = True