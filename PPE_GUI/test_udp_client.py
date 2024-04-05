import socket
import threading

# Set the server's IP address and port number
server_host = '192.168.225.4'  # Replace with the actual server IP address
server_port = 9999  # Replace with the actual server port number


# Set the message to send
message = "#10:04:20#5#"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (server_host, server_port)


def receive():
    while True:
        try:
            message, _ = client_socket.recvfrom(1024)
            print(message.decode())
        except:
            pass

t = threading.Thread(target=receive)
t.start()

# Send the message to the server
client_socket.sendto(message.encode(), server_address)

