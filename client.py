import socket
import threading
import time

HEADER = 64
PORT = 12347
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "localhost"
#SERVER = "192.168.1.10"
ADDR = (SERVER, PORT)
RESPOND = "ready_to_transfer"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def encode(enc_msg):
    message = enc_msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    # print(f"Encoded: {message}")
    message_return = (send_length, message)
    return message_return


def send(msg):
    global client
    message_enc = encode(msg)
    try:
        client.send(message_enc[0])
        client.send(message_enc[1])
    except:
        print("Failed to send message")
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
        client.send(message_enc[0])
        client.send(message_enc[1])

def listen():
    global client
    received = ""
    data = ""
    while True:
        try:
            received = client.recv(64).decode(FORMAT)
        except:
            print("Failed to receive response")
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(ADDR)
        #if received:
        print(f"Received: {received}")


def send_user_input():
    user_input = input()
    send(f"{user_input}")
    print(f"Sent: {user_input}")


'''
print(f"Received: {received}")
            if received == "name":
                data = "r1"
                send(f"{data}")
                send("r1,HMI,at_handover_pos")
                print(f"Sent: {data}")
            elif received == "part_secured":
                data = "r1,r2,complete"
                send(f"{data}")
                print(f"Sent: {data}")
            elif received == "complete":
                data = "r1,cam,r1_send_cam_data"
                send(data)
                print(f"Sent: {data}")
            elif received == "side":
                data = "r1,r2,R"
                send(f"{data}")
                print(f"Sent: {data}")
            else:
'''

thread = threading.Thread(target=send_user_input)
thread.start()
listen()
print(f"thread is alive: {thread.is_alive()}")
time.sleep(5)
if not thread.is_alive():
    print("Trying to reconnect")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    new_thread = threading.Thread(listen())
    new_thread.start()

