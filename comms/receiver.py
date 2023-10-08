import comm_head
import socket
import messagehandler # TODO: remove
import thread

#thread.start_new_thread(--method--,--vars--)

# The next port that will be used for commucation
gNextCommPort = 4000

# Open a new connection with the next incoming request
def Connect_User():
  # Get needed gobals
  global gNextCommPort

  # Make the socket
  sock = socket.socket()
  
  # Bind the socket to the incoming port
  sock.bind(('', comm_head.NEW_CONNECTION_PORT))

  # Tell the socket to listen
  sock.listen(5)

  # Wait for a request to accept
  print("Waiting for connection") # TODO: remove
  cont, addr = sock.accept()

  # Make the socket that will be used for chatting
  chat_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  # Get the next available port TODO: after port 5000 everything will break
  for port in range(gNextCommPort, 5000):
    # connect_ex returns 0 if the port is not available
    if chat_sock.connect_ex(('127.0.0.1', port)) != 0:
      gNextCommPort = port
      chat_sock.close()
      break
  
  print ('Got connection from: ', addr, '\nPort choosen:', gNextCommPort) # TODO: remove

  # Tell the connecter the choosen port to connect back to
  cont.send(str(gNextCommPort).encode())
  # Close the main line connection
  cont.close()

  # Setup the comm channel on the choosen port
  Open_Comm_Channal(gNextCommPort)

# Will setup the receiving end of a comm channal
def Open_Comm_Channal(port):

  # Make the socket
  sock = socket.socket()
  
  # Bind the socket to the incoming port
  sock.bind(('', port))

  # Tell the socket to listen
  sock.listen(5)

  # Set the timeout (low so it will go though the sockets quickly)
  socket.setdefaulttimeout(.1)

  # Wait for a request to accept
  print("Waiting for comm connection") # TODO: remove
  cont, addr = sock.accept()
  cont.send('CONNECTION MADE'.encode()) # TODO: remove
  comm_head.gComm_Channels.append(cont)
  messagehandler.Receiver()

Connect_User()