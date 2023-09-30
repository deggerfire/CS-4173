import comm_head
import socket
import time

# The list of connections
gComm_Channels = {}

# Try to open a connection with the ip
def Connect(ip):
    # Make the socket
    sock = socket.socket()
    # Try to connect to the given ip
    sock.connect((ip, comm_head.NEW_CONNECTION_PORT))

    # The reply will be the port that commucation will be done on
    port = sock.recv(1024).decode()
    print(sock.recv(1024).decode())

    # Close the socket
    sock.close()

    # Give the receiver a half second to setup the comm port
    time.sleep(.5)
    sock2 = socket.socket()
    # Try and connect to the comm port
    sock2.connect((ip, int(port)))
    print(sock2.recv(1024).decode())
    sock2.send('Hi'.encode())
    print(sock2.recv(1024).decode())
    sock2.close()

Connect('127.0.0.1')