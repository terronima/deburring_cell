import time

from PyQt5 import QtCore


#
# # test splitting sequence (0-8 are rights, 9-17 are lefts)
# camera_data = [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1]
# only_left = 0
# only_right = 0
# intermittent = 1
# side_by_side = 0
#
# if only_left:
#     cntr = 0
#     for i in camera_data[0:int(len(camera_data) / 2)]:
#         if i == 1:
#             print(f"Only left selected, pick pos: {cntr}")
#         cntr += 1
# elif only_right:
#     cntr = 9
#     for i in camera_data[int(len(camera_data) / 2)::]:
#         if i == 1:
#             print(f"Only right selected, pick pos: {cntr}")
#         cntr += 1
# elif intermittent:
#     pick_el_1 = 0
#     pick_el_2 = 0
#     string_of_picks = ""
#     for i in range(0, int(len(camera_data) / 2)):
#         pick_el_1 = i
#         pick_el_2 = i + int(len(camera_data) / 2)
#         if camera_data[pick_el_1] == 1:
#             string_of_picks += str(i) + ','
#         if camera_data[pick_el_2] == 1:
#             string_of_picks += str(pick_el_2) + ','
#     print(f"parts to be picked {string_of_picks}")
# elif side_by_side:
#     cntr = 0
#     for i in camera_data[0:int(len(camera_data) / 2)]:
#         if i == 1:
#             print(f"Only left selected, pick pos: {cntr}")
#         cntr += 1
#     for i in camera_data[int(len(camera_data) / 2)::]:
#         if i == 1:
#             print(f"Only right selected, pick pos: {cntr}")
#         cntr += 1
# # flipping certain number of elements of the array
# arr_1 = [0, 1, 2, 3, 4]
# arr_2 = []
# step = 5
# ctr = 1
# j = min(step - 1, len(arr_1) - 1)
# step_over = 0
# for i in range(0, int(len(arr_1))):
#     if j > len(arr_1) - 1 and step_over:
#         break
#     if j >= len(arr_1):
#         j = j - (j - (len(arr_1) - 1))
#         step_over = 1
#     print(f"j value: {j}")
#     arr_2.append(arr_1[j])
#     j -= 1
#     if j == (step * ctr) - (step + 1):
#         j = step * ctr + step - 1
#         ctr += 1
#
# print(arr_2)
# # map = "00000"
# # if not int(map):
# #     map[1] = "1"
# #     print(f"the map variable is {map}")
# # else:
# #     print(map)
#
# lis = [(1, 2, 3)]
# print(f'selected element: {lis[0][1]}')
#
# import socket
# import threading
# import time
#
# HEADER = 64
# PORT = 12347
# FORMAT = "utf-8"
# DISCONNECT_MESSAGE = "!DISCONNECT"
# SERVER = "localhost"
# # SERVER = "192.168.1.10"
# ADDR = (SERVER, PORT)
# RESPOND = "ready_to_transfer"
#
# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(ADDR)
#
#
# def encode(enc_msg):
#     message = enc_msg.encode(FORMAT)
#     msg_length = len(message)
#     send_length = str(msg_length).encode(FORMAT)
#     send_length += b' ' * (HEADER - len(send_length))
#     # print(f"Encoded: {message}")
#     message_return = (send_length, message)
#     return message_return
#
#
# def send(msg):
#     global client
#     message_enc = encode(msg)
#     try:
#         client.send(message_enc[0])
#         client.send(message_enc[1])
#     except:
#         print("Failed to send message")
#         client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         client.connect(ADDR)
#         client.send(message_enc[0])
#         client.send(message_enc[1])
#
#
# def listen():
#     global client
#     received = ""
#     data = ""
#     while True:
#         try:
#             received = client.recv(64).decode(FORMAT)
#         except:
#             print("Failed to receive response")
#             client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             client.connect(ADDR)
#         if received != "ping":
#             print(f"Received: {received}")
#             user_input = input()
#             send(f"{user_input}")
#             print(f"Sent: {user_input}")
#
#
# '''
# print(f"Received: {received}")
#             if received == "name":
#                 data = "r1"
#                 send(f"{data}")
#                 send("r1,HMI,at_handover_pos")
#                 print(f"Sent: {data}")
#             elif received == "part_secured":
#                 data = "r1,r2,complete"
#                 send(f"{data}")
#                 print(f"Sent: {data}")
#             elif received == "complete":
#                 data = "r1,cam,r1_send_cam_data"
#                 send(data)
#                 print(f"Sent: {data}")
#             elif received == "side":
#                 data = "r1,r2,R"
#                 send(f"{data}")
#                 print(f"Sent: {data}")
#             else:
# '''
#
# # thread = threading.Thread(target=send_user_input)
# # thread.start()
# listen()
# # print(f"thread is alive: {thread.is_alive()}")
# # time.sleep(5)
# # if not thread.is_alive():
# #     print("Trying to reconnect")
# #     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# #     client.connect(ADDR)
# #     new_thread = threading.Thread(listen())
# #     new_thread.start()
# # start_time = time.time()
# # time.sleep(5)
# # stop_time = time.time()
# # time_past = int(stop_time - start_time)
# # print(f"{time_past}")
def timer(trig):
    timer = time.time()
    while trig:
        crnt_tmr = time.time()
        diff = crnt_tmr - timer
        print(str("%.2f" % diff))
        time.sleep(0.01)
        # if diff >= 20:
        #     break
    print("complete")


import threading

# trig = 0
# while True:
#     f = threading.Thread(target=timer(trig))
#     trig = input("enter 0 or 1 to start timer:")
#     f.start()


from PyQt5.QtCore import QObject, QThread, pyqtSignal
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import socket
import sys

# Snip...


HEADER = 64
PORT = 12347
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "localhost"
# SERVER = "192.168.1.10"
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
    while True:
        message_enc = encode(msg)
        try:
            client.send(message_enc[0])
            client.send(message_enc[1])
            break
        except:
            print(f"Exception captured")


# Step 1: Create a worker class
class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)

    def run(self):
        """Long-running task."""
        recv = ""
        while True:
            try:
                recv = client.recv(64).decode("utf-8")
                recv = recv.strip("z")
                if recv != "z" and len(recv) > 0:
                    print(f"received: {recv}")
            except:
                print("failed")
            if len(recv) > 1:
                self.progress.emit(recv)
            if recv == "name":
                send("test")
            if recv == "break":
                break
        self.finished.emit()


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clicksCount = 0
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Freezing GUI")
        self.resize(300, 150)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        # Create and connect widgets
        self.clicksLabel = QLabel("Counting: 0 clicks", self)
        self.clicksLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.stepLabel = QLabel("Long-Running Step: 0")
        self.stepLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.countBtn = QPushButton("Click me!", self)
        self.countBtn.clicked.connect(self.countClicks)
        self.longRunningBtn = QPushButton("Long-Running Task!", self)
        self.longRunningBtn.clicked.connect(self.runLongTask)
        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.clicksLabel)
        layout.addWidget(self.countBtn)
        layout.addStretch()
        layout.addWidget(self.stepLabel)
        layout.addWidget(self.longRunningBtn)
        self.centralWidget.setLayout(layout)

    def countClicks(self):
        self.clicksCount += 1
        self.clicksLabel.setText(f"Counting: {self.clicksCount} clicks")

    def reportProgress(self, n):
        self.stepLabel.setText(f"Long-Running Step: {n}")
        if n == "hello":
            send("test,r1,world")

    def runLongTask(self):
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.reportProgress)
        # Step 6: Start the thread
        self.thread.start()

        # Final resets
        self.longRunningBtn.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.longRunningBtn.setEnabled(True)
        )
        self.thread.finished.connect(
            lambda: self.stepLabel.setText("Long-Running Step: 0")
        )


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
