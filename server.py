# NetConnect Server
import socket
import threading
import logging
import json

logging.basicConfig(
    filename="logs/server.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)
with open("config.json", "r") as file:
    config = json.load(file)

HOST = config["host"]
PORT = config["port"]
BUFFER_SIZE = config["buffer_size"]
DEFAULT_ROOM = config["default_room"]
clients = []
usernames = {}

rooms = {
    DEFAULT_ROOM: []
}
user_rooms = {}
    
server =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

print("Server is listening...")


def handle_client(connection, address):

    print("Client connected:", address)
    logging.info(f"Client connected: {address}")

    username = connection.recv(1024).decode()

    print("Username:", username)
    logging.info(f"Username: {username}")
    usernames[connection] = username    
    user_rooms[connection] = DEFAULT_ROOM
    connection.send("Welcome!".encode())

    while True:

        try:
            message = connection.recv(1024).decode()

            if not message:
                break

            print(username + ": " + message)
            logging.info(username + ": " + message)
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
                 logging.info(f"Room created: {room_name}")

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
                 logging.info(f"{username} joined room: {room_name}")

                 connection.send(
                    ("Joined room: " + room_name).encode()
                 )

               else:

                     connection.send(
                         ("Room does not exist").encode()
                     )
               continue
            
            #Broadcasting

            current_room = user_rooms[connection]
            for client in rooms[current_room]:

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

    rooms[DEFAULT_ROOM].append(connection)

    thread = threading.Thread(
        target=handle_client,
        args=(connection, address)
    )

    thread.start()