import comm_head
import socket
import time
import messagehandler # TODO: remove

# The list of connections
#gComm_Channels = []

# Try to open a connection with the ip
def Connect(ip):
    # Make the socket
    sock = socket.socket()
    # Try to connect to the given ip
    sock.connect((ip, comm_head.NEW_CONNECTION_PORT))

    # The reply will be the port that commucation will be done on
    port = sock.recv(1024).decode()

    # Close the socket
    sock.close()

    # Give the receiver a half second to setup the comm port
    time.sleep(.5)

    # Make a socket for the comm channel
    sock2 = socket.socket()

    # Set the timeout (low so it will go though the sockets quickly)
    #sock2.setdefaulttimeout(.1)

    # Try and connect the comm port to the given port
    sock2.connect((ip, int(port)))

    print(sock2.recv(1024).decode()) # TODO: remove

    # Add the channel to the comm list
    comm_head.gCommChannels.append(sock2)

    messagehandler.Message_Sim_DEBUG() # TODO: remove

Connect('127.0.0.1')