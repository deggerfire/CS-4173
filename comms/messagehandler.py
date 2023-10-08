import comm_head
import time
import socket

# Reveiver incoming messages
def Receiver():
    # Loop and reciver messages from all of the comm channels
    for channel in comm_head.gCommChannels:
        # Timing out causes an error that will crash the program
        try:
            # Split the message on NULL chars (because we can get merged messages) TODO: might cause issues with encoding
            messages = channel.recv(1024).decode().split(chr(0))
            for message in messages:
                if message != '':
                    comm_head.gMessageBufList.append(message)
            time.sleep(.5) # TODO: remove
        # If there is a time out error we don't care
        except socket.timeout:
            pass

    print(comm_head.gMessage_Buf_List) # TODO: remove
    print("---") # TODO: remove

    Receiver() # TODO: 10/10 good code (aka kill asap)

    Close_Comm_Channals()

# Debug message for sending messages
def Message_Sim_DEBUG():
    Send_message("test1")
    Send_message("test2")
    Send_message("test3")
    time.sleep(5)
    Send_message("test4")
    Send_message("test5")
    Send_message("test6")
    Close_Comm_Channals()

# Sends a message to all of the connections
def Send_Message(message):
    print("Sending: ", message)
    for channel in comm_head.gCommChannels:
        # Send the message and add on a NULL char at the end of the message
        channel.send((message + chr(0)).encode())

# Close all of the comm channals
def Close_Comm_Channals():
  for channel in comm_head.gCommChannels:
    channel.close()