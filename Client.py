import socket
import threading
import sys
import random

HEADER = 1024  # Buffer Sizes
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"  # Disconnecting message 

registry = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Socket to connect to registry TCP
registry.connect(('127.0.0.1', 5050))

registryName ='localhost'
registryPort = 4242

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP SOCKET 

connected_to_peer = False
x=False

def get_free_port(): # generates unused ports for client
    value = random.randint(2000, 9000)
    not_in_use = True
    while not_in_use:
        value = random.randint(2000, 9000)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            not_in_use = s.connect_ex(('localhost', value)) == 0
    return value

listening_server = socket.gethostbyname(socket.gethostname())  # server for listening (gets users ip)
listening_port = get_free_port()        # port for listening
 
peer_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Peer server (listening)
peer_server.bind((listening_server,listening_port))

peer_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Peer client (connecting with peer)


def f(f_stop):  # communicate with udp
    if not f_stop.is_set():
        message="HELLO"
        udp_socket.sendto(message.encode(), (registryName, registryPort))
        modifiedMessage, serverAddress = udp_socket.recvfrom(1024)
        # print(modifiedMessage.decode())
        threading.Timer(6, f, [f_stop]).start()  # Send HELLO every 6 seconds

def receive_registry():  # recieves messages from registry server
    f_stop = threading.Event()
    f(f_stop)
    while True:
        try:
        # Receive Message From Server
        # If 'NICK' Send Nickname
            message = registry.recv(1024).decode('ascii')
            if message == 'NICK':
                global nickname
                nickname = input("Choose your nickname:")
                password = input("Choose your password:")
                full = nickname + " " + password
                registry.send(full.encode('ascii'))
            elif message == "SOCKDET":
                add, port = (listening_server, listening_port)
                add_port = f"({add}, {port})".encode()
                registry.send(add_port)
                menu_thread = threading.Thread(target=menu_options)
                menu_thread.start()
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            registry.close()
            break


def connect_with():  # asks about connecting with peer
    connect_with = input("Who would you like to connect with: ")
    try:
        registry.send(connect_with.encode())
    except:
        print(f"{connect_with} is unavaliable")  # username does not exist

def menu_options(): 
    while True:
        if connected_to_peer:
            break
        print("1. Search by username\n2. Connect To Peer")
        choice = input("Choice: ")
        if choice == '1':
            connect_with()
        elif choice == '2':
            ip_add = input("Ip address: ")
            port = int(input("port: "))
            peer_client.connect((ip_add, port))
            sending_thread = threading.Thread(target=send_peer, args=(peer_client,))
            sending_thread.start()
            receive_peer(peer_client)
            break
        else:
            print("Invalid Input")

def receive_peer(conn): # recieves messages from peer
    while True: 
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f"{msg}")
            if msg == DISCONNECT_MESSAGE:
                break
    print("Client disconnected")


def send_peer(conn):  # sends messages to peer
    while True:
        msg = input("Enter Message: ")
        msg = f"{nickname}: {msg}"
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


def start_peer_server(): # peer listing server
    while True:
        peer_server.listen()
        global connected_to_peer
        try:
            if not connected_to_peer:
                conn, addr = peer_server.accept()
            else:  # if an error occurs, socket is busy
                print("BUSY")
                continue
        except:
            print("BUSY")
        print("CONNECTION ESTABLISHED")
        connected_to_peer = True
        sending_thread = threading.Thread(target=send_peer, args=(conn,))
        sending_thread.start()
        receive_peer(conn)





# Starting Thread for listening from Registry
receive_reg_thread = threading.Thread(target=receive_registry)
receive_reg_thread.start()

# Start peer server
peer_server_thread = threading.Thread(target=start_peer_server)
peer_server_thread.start()



