import socket
import sys
import threading
import time
import random
import keyboard
from _thread import interrupt_main

HEADER = 64
PORT = 12347
SERVER = "127.0.0.1"  # socket.gethostbyname(socket.gethostname())
ADDR = ("", PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
CLIENT_TRACKING = []
Temp_data_storage = ''
QUIT = ''

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


'''def close_server():
    while True:
        try:
            if keyboard.is_pressed("q"):
                print("The 'q' is pressed")
                time.sleep(1)
                QUIT = "q"
                interrupt_main()
        except:
            continue'''


def isopen(conn, addr):
    while True:
        try:
            conn.sendall(b"ping")
            #print(f"connected {addr}")
            time.sleep(0.5)
        except:
            print("failed")
            print(f"list length is {len(CLIENT_TRACKING)}")
            break


def greet(conn, addr):
    conn.sendall(b"name")
    msg_length = int(conn.recv(HEADER).decode(FORMAT))
    greet_resp = conn.recv(msg_length).decode(FORMAT)
    print(f"Greet resp: {greet_resp} from {addr}")
    number = random.randint(1000, 99999)
    for i in range(len(CLIENT_TRACKING)):
        temp = CLIENT_TRACKING[i][1]
        if temp == greet_resp:
            CLIENT_TRACKING.pop(i)
    CLIENT_TRACKING.append((number, greet_resp, conn))
    print(f"Conn# {number}")
    transfer(greet_resp, "complete")
    print("Greeting complete")
    return number


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    conn_pos = greet(conn, addr)
    timer = threading.Timer(0.1, isopen, args=(conn, addr))
    timer.start()
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                print(f"received msg: {msg}")
                msg_split = msg.split(',')
                dest = msg_split[1]
                command = msg_split[2]
                if command == DISCONNECT_MESSAGE:
                    break
                if dest == "r1" or "r2" or "cam" or "HMI":
                    transfer(dest, command)
                print(f"[{addr}] {msg}")
        except:
            print("Failed to receive data")
            break
    # remove_obj = [item for item in CLIENT_TRACKING if item[0] == source]
    print(f"[Connection closed] {addr}")
    i = 0
    while True:
        if i == len(CLIENT_TRACKING):
            i = 0
        stat = CLIENT_TRACKING[i][0]
        if stat == conn_pos:
            CLIENT_TRACKING.pop(i)
            print("list of clients" + str(CLIENT_TRACKING))
            break
        i += 1
    conn.close()


def transfer(dest, command):
    while True:
        selected = [item for item in CLIENT_TRACKING if item[1] == dest]
        text = command.encode(FORMAT)
        if selected:
            conn = selected[0][2]
            try:
                conn.sendall(text)
                print(f"Transferred: {text} to {dest}")
            except:
                print("something went wrong, check sockets")
            print(f"{dest}, {text}")
            break


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {socket.gethostbyname(socket.gethostname())}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


'''thread = threading.Thread(target=close_server)
thread.start()'''
print("[STARTING] Server is starting")
start()