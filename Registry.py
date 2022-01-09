from threading import Thread
import servers.TCPserver as tcp_server
import servers.UDPServer as udp_server

if __name__ == '__main__':
    Thread(target = tcp_server.receive).start()
    Thread(target = udp_server.listen_clients).start()