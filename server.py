# NetConnect Server
import socket
import threading

clients = []
usernames = {}

rooms = {
    "General": []
}
user_rooms = {}
    
server =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 55555))

server.listen()

print("Server is listening...")


def handle_client(connection, address):

    print("Client connected:", address)

    username = connection.recv(1024).decode()

    print("Username:", username)
    usernames[connection] = username    
    user_rooms[connection] = "General"
    connection.send("Welcome!".encode())

    while True:

        try:
            message = connection.recv(1024).decode()

            if not message:
                break

            print(username + ": " + message)
            if message == "ROOMS":
               
               room_list = ", ".join(rooms.keys())

               connection.send(
                  ("Available rooms: " + room_list).encode()
               )

               continue
            if message.startswith("CREATE_ROOM|"):

              room_name = message.split("|")[1]

              if room_name not in rooms:
                 rooms[room_name] = []

                 connection.send(
                  ("Room created: " + room_name).encode()
                )

              else:
                 connection.send(
                    ("Room already exists").encode()
                )

              continue
            if message.startswith("JOIN_ROOM|"):

               room_name = message.split("|")[1]

               if room_name in rooms:

                 old_room = user_rooms[connection]

                 if connection in rooms[old_room]:
                       rooms[old_room].remove(connection)

                 rooms[room_name].append(connection)

                 user_rooms[connection] = room_name

                 connection.send(
                    ("Joined room: " + room_name).encode()
                 )

                else:

                     connection.send(
                         ("Room does not exist").encode()
                     )
                continue
            
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

    rooms["General"].append(connection)

    thread = threading.Thread(
        target=handle_client,
        args=(connection, address)
    )

    thread.start()