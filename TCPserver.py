import socket
import threading
# Connection Data
host = '127.0.0.1'
port = 55555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []
connecteds=[]

accounts={}
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
# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname

        while True:
            #Asking for valid nickname until its correct
            client.send('NICK'.encode('ascii'))
            message = client.recv(1024).decode('ascii')
            print(message)
            if(message.split(" ")[0] not in accounts.keys()):
                break

        nicknames.append(message)
        clients.append(client)

        accounts[message.split(" ")[0]] = message.split(" ")[1]
        # Print And Broadcast Nickname
        print("Nickname is {}".format(message.split(" ")[0]))
        broadcast("{} joined!".format(message.split(" ")[0]).encode('ascii'))
        x=message.split(" ")[0]
        client.send(x.encode()+' '.encode()+'Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()