import socket
import threading
import sched, time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

serverName ='localhost'
serverPort = 4242

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP SOCKET

x=False

def f(f_stop):
    # do something here ...


    if not f_stop.is_set():
        message="HELLO"
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        modifiedMessage, serverAddress = clientSocket.recvfrom(1024)
        # print(modifiedMessage.decode())
        threading.Timer(5, f, [f_stop]).start()


def receive():
    f_stop = threading.Event()
    f(f_stop)
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
                message = client.recv(1024).decode('ascii')
                if message == 'NICK':
                    global nickname
                    nickname = input("Choose your nickname:")
                    password = input("Choose your password:")
                    full = nickname + " " + password
                    client.send(full.encode('ascii'))
                else:
                    print(message)
                    write_thread = threading.Thread(target=write)
                    write_thread.start()
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break

# Sending Messages To Server
def write():
    while True:
        try:
            message = '{}: {}'.format(nickname, input('enter message: '))
            client.send(message.encode('ascii'))
        except:
            pass


# Handling Peer to Peer
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISC"



# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()


