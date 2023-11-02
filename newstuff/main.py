import socket

# Define the host and port to listen on
host = "0.0.0.0"  # Listen on all available network interfaces
port = 3000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((host, port))

server_socket.listen(5)

print(f"Listening on {host}:{port}")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")

    data = client_socket.recv(1024)
    if not data:
        break
    received_data = data.decode("utf-8")
    print(f"Received data: {received_data}")

    response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nfuck you!"

    client_socket.send(response.encode("utf-8"))

    client_socket.close()

# Close the server socket when done
server_socket.close()
