import socket
import threading
import time


HEADER = 64
PORT = 12347
SERVER = "127.0.0.1"  # socket.gethostbyname(socket.gethostname())
ADDR = ("", PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
CLIENT_TRACKING = {}
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


def robot_status_to_HMI(name):
    if name and "HMI" in CLIENT_TRACKING:
        if name == "r1":
            transfer(CLIENT_TRACKING["HMI"], "r1_active")
        elif name == "r2":
            transfer(CLIENT_TRACKING["HMI"], "r2_active")
    elif name not in CLIENT_TRACKING and "HMI" in CLIENT_TRACKING:
        if name == "r1":
            transfer(CLIENT_TRACKING["HMI"], "r1_faulted")
        elif name == "r2":
            transfer(CLIENT_TRACKING["HMI"], "r2_faulted")


def is_open(conn, addr):
    global CLIENT_TRACKING
    while True:
        try:
            conn.send(b" ")
            # print(f"connected {addr}")
            time.sleep(1)
        except:
            print("failed")
            print(f"list length is {len(CLIENT_TRACKING)}")
            break


def greet(conn, addr):
    global CLIENT_TRACKING
    conn.send(b"name")
    msg_length = int(conn.recv(HEADER).decode(FORMAT))
    greet_resp = conn.recv(msg_length).decode(FORMAT)
    print(f"Greet resp: {greet_resp} from {addr}")
    # if greet_resp in CLIENT_TRACKING:
    #     CLIENT_TRACKING[greet_resp].close()
    #     CLIENT_TRACKING.pop(greet_resp)
    #     print(f"Current list: {CLIENT_TRACKING}")
    CLIENT_TRACKING.update({f"{greet_resp}": conn})
    transfer(CLIENT_TRACKING[greet_resp], "complete")
    # print(CLIENT_TRACKING)
    print("Greeting complete")
    return greet_resp


def handle_client(conn, addr):
    global CLIENT_TRACKING
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    conn_name = greet(conn, addr)
    timer = threading.Timer(0.1, is_open, args=(conn, addr))
    timer.start()
    robot_status_to_HMI(conn_name)
    while connected:
        robot_status_to_HMI(conn_name)
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
                transfer(CLIENT_TRACKING[dest], command)
                print(f"[{addr}] {msg}")
        except:
            print("Failed to receive data")
            break
    # remove_obj = [item for item in CLIENT_TRACKING if item[0] == source]
    conn.close()
    CLIENT_TRACKING.pop(conn_name)
    print(f"[Connection closed] {addr}")
    print(CLIENT_TRACKING)



def transfer(dest, command):
    conn = dest
    text = command.encode(FORMAT)
    try:
        conn.send(text)
        print(f"Transferred: {text} to {dest}")
    except:
        print("something went wrong, check sockets")
    print(f"{dest}, {text}")


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
