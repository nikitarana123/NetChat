# NetConnect Client
import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 55555))

username=input("Enter username:")
client.send(username.encode())

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            print(message)
        except:
            break

thread = threading.Thread(target=receive_messages)
thread.daemon = True
thread.start()

while True:
    message = input("Enter your message: ")

    if message.upper() == "EXIT":
        print("Exiting...")
        break

    client.send(message .encode())

client.close()
print("Disconnected")



    

