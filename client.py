# NetConnect Client
import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 55555))

username=input("Enter username:")
client.send(username.encode())

while True:
    message =input("Enter your message: ")

    if message.upper() == "EXIT":
        print("Exiting...")
        break

    client.send(message .encode())

client.close()
print("Disconnected")

    

