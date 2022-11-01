import socket
from server_multiple import MyTCPHandler
import socketserver
import threading
from threadstest import myThread

# test splitting sequence (0-8 are rights, 9-17 are lefts)
camera_data = [1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0]
only_left = 0
only_right = 0
intermittent = 1
side_by_side = 0

if only_left:
    cntr = 0
    for i in camera_data[0:int(len(camera_data) / 2)]:
        if i == 1:
            print(f"Only left selected, pick pos: {cntr}")
        cntr += 1
elif only_right:
    cntr = 9
    for i in camera_data[int(len(camera_data) / 2)::]:
        if i == 1:
            print(f"Only right selected, pick pos: {cntr}")
        cntr += 1
elif intermittent:
    pick_el_1 = 0
    pick_el_2 = 0
    string_of_picks = ""
    for i in range(0, int(len(camera_data) / 2)):
        pick_el_1 = i
        if camera_data[pick_el_1] == 1:
            string_of_picks += str(i) + ','
        pick_el_2 = i + int(len(camera_data) / 2)
        if camera_data[pick_el_2] == 1:
            string_of_picks += str(pick_el_2) + ','
    print(f"parts to be picked {string_of_picks}")
elif side_by_side:
    cntr = 0
    for i in camera_data[0:int(len(camera_data) / 2)]:
        if i == 1:
            print(f"Only left selected, pick pos: {cntr}")
        cntr += 1
    for i in camera_data[int(len(camera_data) / 2)::]:
        if i == 1:
            print(f"Only right selected, pick pos: {cntr}")
        cntr += 1

arr_1 = [0, 1, 2, 3, 4, 5, 6, 7, 8]
arr_2 = []
j = 2
ctr = 1
next_step = 0
for i in range(0, int(len(arr_1))):
    arr_2.append(arr_1[j])
    j -= 1
    if j == -1:
        j = 5
    elif j == 2:
        j = 8


print(arr_2)
