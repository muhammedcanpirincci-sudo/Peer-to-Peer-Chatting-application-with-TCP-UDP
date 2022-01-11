import socket
import threading
# Connection Data
host = '127.0.0.1'
port = 5050

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = {}  # Nickname: ClientSocket
nicknames = {} # Nickname: Address
connecteds=[]  # Connected users

accounts={}  # Accounts

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

def connect_with(client):
    while True:
        message = client.recv(1024)
        for nickname in nicknames:
            if nickname == message.decode():
                add = nicknames[nickname]
                client.send(f"\n{message.decode()} is available. His/Her info is:\n{add}\n".encode())
        


# Receiving / Listening Function
def receive():
    print("TCP is running")
    while True:
        # Accept Connection
        client, address = server.accept()
        print(f"TCP: Connected with {str(address)}")

        # Request And Store Nickname
        while True:
            # Username validation
            client.send('NICK'.encode('ascii'))
            message = client.recv(1024).decode('ascii')
            print(f"TCP: {message}")
            if(message.split(" ")[0] not in accounts.keys()):
                client.send("SOCKDET".encode())
                sockdet = client.recv(1024).decode('ascii')
                break
        nicknames[message.split(" ")[0]] = sockdet
        clients[address] = client
        accounts[message.split(" ")[0]] = message.split(" ")[1]

        # Print And Broadcast Nickname
        print("TCP: Nickname is {}".format(message.split(" ")[0]))
        x=message.split(" ")[0]
        client.send(x.encode()+' '.encode()+'Connected to server!'.encode('ascii'))
        connecting_thread = threading.Thread(target=connect_with, args=(client,))
        connecting_thread.start()
        # # Start Handling Thread For Client
        # thread = threading.Thread(target=handle, args=(client,))
        # thread.start()


