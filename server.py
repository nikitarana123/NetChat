# NetConnect Server
import socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 55555))
server.listen()
print("Server is listening...")

connection, address = server.accept()
print("Client connected:",address)
message = connection.recv(1024).decode()
print(message)
connection.send("Welcome!" .encode())
