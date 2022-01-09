import threading
import socket
import logging


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 4242))
clients_list = []

def talkToClient(ip):
    print("UDP: Sending 'OK' to %s", ip)
    sock.sendto('!OK'.encode(), ip)

def listen_clients():
    print("UDP is running")
    while True:
        msg, client = sock.recvfrom(1024)
        print('UDP: Received data from client %s: %s', client, msg)
        t = threading.Thread(target=talkToClient, args=(client,))
        t.start()
