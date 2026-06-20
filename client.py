# NetConnect Client
import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 55555))
client.send("Hello" .encode())
print("Connected to server")
