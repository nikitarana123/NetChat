# NetConnect Server
import socket
import threading

clients = []

server =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 55555))

server.listen()

print("Server is listening...")


def handle_client(connection, address):

    print("Client connected:", address)

    username = connection.recv(1024).decode()

    print("Username:", username)

    connection.send("Welcome!".encode())

    while True:

        try:
            message = connection.recv(1024).decode()

            if not message:
                break

            print(username + ": " + message)

            #Broadcasting
            for client in clients:
                 if client != connection:
                     try:
                         client.send(
                           (username + ": " + message).encode()

                        )
                     except:
                            pass

        except:
            break

    connection.close()


while True:

    connection, address = server.accept()

    print("NEW CONNECTION:", address)

    clients.append(connection)

    thread = threading.Thread(
        target=handle_client,
        args=(connection, address)
    )

    thread.start()