import socket
import sys

HOST, PORT = "localhost", 8000
big = "0"*4096
data = (
    "GET /wiki/страница HTTP/1.1\r\n"
    "Host: ru.wikipedia.org\r\n"
    "User-Agent: Mozilla/5.0 (X11; U; Linux i686; ru; rv:1.9b5) Gecko/2008050509 Firefox/3.0b5\r\n"
    f"X-Very-Big-Data: {big}\r\n"
    "Connection: close\r\n"
    "\r\n"
)

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(bytes(data, "utf-8"))
    sock.sendall(b"\n")

    # Receive data from the server and shut down
    received = str(sock.recv(4000), "utf-8")

print("Sent:    ", data)
print("Received:", received)