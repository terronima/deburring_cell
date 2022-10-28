import socket
import threading

HEADER = 64
PORT = 12347
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.1.10"
ADDR = (SERVER, PORT)
RESPOND = "part_secured"

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
    message_enc = encode(msg)
    client.send(message_enc[0])
    client.send(message_enc[1])


def listen():
    while True:
        received = client.recv(1024).decode(FORMAT)
        if received:
            print(f"Received: {received}")
            if received == "name":
                data = "r2"
                send(data)
                send("r2,cam,r2_send_cam_data")
                print(f"Sent: {data}")
            elif received == "at_handover_pos":
                data = f"r2,r1,{RESPOND}"
                send(data)
                print(f"Sent: {data}")
            else:
                print(str(received))


thread = threading.Thread(listen())
thread.start()
send("r2,r1,r2_send_positions")
send("r2,cam,r2_send_positions")
