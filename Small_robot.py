import socket
import sys
import threading

HOST = "192.168.1.10"  # The server's hostname or IP address
PORT = 12347  # The port used by the server
FORMAT = "utf-8"
HEADER = 64
ADDR = (HOST, PORT)
CLIENT_NAME = "small"
GREETING_SENT = False
set_tool("no_part")
SIDE = "R"
F1_USR_CORD = 101
SURFACE_1 = [Global_sur_1_j_cent, Global_sur_1_cent, Global_sur_1_p1, Global_sur_1_p2, Global_sur_1_p3, Global_sur_1_p4,
             Global_sur_1_p5, Global_sur_1_p6, Global_sur_1_p7]
SURFACE_2 = [Global_sur_2_j_cent, Global_sur_2_cent, Global_sur_2_p1, Global_sur_2_p2, Global_sur_2_p3, Global_sur_2_p4,
             Global_sur_2_p5, Global_sur_2_p6]
SURFACE_3 = [Global_sur_3_j_cent, Global_sur_3_cent, Global_sur_3_p1, Global_sur_3_p2, Global_sur_3_p3, Global_sur_3_p4,
             Global_sur_3_p5]
SURFACE_4 = [Global_sur_4_j_cent, Global_sur_4_cent, Global_sur_4_p1, Global_sur_4_p2, Global_sur_4_p3, Global_sur_4_p4,
             Global_sur_4_p5]
SURFACE_5 = [Global_sur_5_j_cent, Global_sur_5_cent, Global_sur_5_p1, Global_sur_5_p2, Global_sur_5_p3]
SURFACE_6 = [Global_sur_6_j_cent, Global_sur_6_cent, Global_sur_6_p1, Global_sur_6_p2, Global_sur_6_p3]
deburr_vel = [200, 200]
safe_acc = [300, 300]
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def greet():
    while True:
        received = client.recv(HEADER).decode(FORMAT)
        if received:
            tp_log("Received: " + received)
            if received == "name":
                data = "r2"
                send(data, 1)
                tp_log("Sent: " + data)
                break


def send(msg, resp_req):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * ((HEADER) - len(send_length))
    client.send(send_length)
    client.send(message)
    while resp_req:
        data = client.recv(1024).decode(FORMAT)
        if data != "ping":
            tp_log(str(data))
            return (data)


def deburr(pos, ref_c):
    F1_List = []
    set_velx(200, 200)
    set_accx(300)
    movej(Global_deburr_safe)
    L_F_j_position = pos[0]
    L_F_centre_position = pos[1]
    # movej(Global_deburr_safe)
    movej(pos[0])  # joint move to pos above
    movel(pos[1])  # linear move to pos before creating local coord sys
    set_ref_coord(ref_c)
    k_d1 = [1500.0, 1500.0, 1500.0, 1000.0, 1000.0, 1000.0]  # set compliance stiffness
    task_compliance_ctrl(k_d1)
    force_desired = 10  # set desired force
    f_d = [0.0, 0.0, -force_desired, 0.0, 0.0, 0.0]  # set force direction
    f_dir = [0, 0, 1, 0, 0, 0]
    set_desired_force(f_d, f_dir)
    while (1):  # loop to check that force is achieved
        force_condition = check_force_condition(DR_AXIS_Z, max=force_desired)
        if force_condition == 1:
            break
    release_compliance_ctrl()
    new_centre_position = get_current_posx()  # ref = L_F1_USR_CORD)
    new_centre_position = new_centre_position[0]
    L_F1_NEW_USR_CORD = set_user_cart_coord(new_centre_position, ref=DR_BASE)
    tp_log(str(L_F1_NEW_USR_CORD))
    set_ref_coord(L_F1_NEW_USR_CORD)
    for i in range(2, len(pos) - 1):
        F1_List.append(coord_transform(pos[i], DR_BASE, L_F1_NEW_USR_CORD))
    movesx(F1_List, vel=deburr_vel, acc=safe_acc)
    tp_log("movesx_complete")
    above_pos = trans(F1_List[len(F1_List) - 1], [0, 100, 0, 0, 0, 0], ref=DR_BASE)
    tp_log(str(above_pos))
    movel(above_pos)
    # l_F1_point1_above = trans(L_F1_point1,[0,0,-100,0,0,0], DR_TOOL)
    # movel(l_F1_point1_above)
    # movel(L_F1_point1)
    # k_d2 = [100.0, 100.0, 50.0, 100.0, 100.0, 100.0]   #set compliance stiffness
    # task_compliance_ctrl(k_d2)
    # movel(L_F1_point2)
    wait(0.5)
    release_force
    # release_compliance_ctrl()                                                  #remove force from the axis
    set_ref_coord(DR_BASE)


def dip_part():
    if get_digital_input(level_sensor_low):
        send("r2,HMI,r2_faulted", 0)
    else:
        Global_above_basin_l = trans(Global_basin_l, [0, 0, 300, 0, 0, 0], ref=DR_BASE)
        set_velx(deburr_vel)
        set_accx(safe_acc)
        movej(Global_above_basin_j)
        movel(Global_above_basin_l)
        movel(Global_basin_l)
        wait(1)
        movel(Global_above_basin_l)
        movej(Global_above_basin_j)
        movej(Global_standby)



def place():
    stiffness = [500, 500, 500, 1000, 1000, 1000]
    force_desired = 50.0  # set desired force
    f_d = [0.0, 0.0, -force_desired, 0.0, 0.0, 0.0]  # set force direction
    f_dir = [0, 0, 1, 0, 0, 0]  # set axis at which force would be applied (x, y, z, a, b, c)
    pallet_map = send("r2,cam,r2_send_cam_data", 1)
    tp_log(str(pallet_map))
    cntr = 0
    pallet_place = 0
    side_l = 0
    side_j = 0
    ref_c = 0
    if SIDE == "L":
        ref_c = 107
        side_l = Global_place_L
        side_j = Global_place_L_j
    elif SIDE == "R":
        ref_c = 106
        side_l = Global_place_R
        side_j = Global_place_R_j
    for i in pallet_map:
        if SIDE == "R" and cntr < len(pallet_map) // 2:
            p = int(i)
            if p == 0:
                pallet_place = cntr
                break
        elif SIDE == "L" and cntr >= len(pallet_map) // 2:
            p = int(i)
            if p == 0:
                pallet_place = cntr - 9
                break
        cntr += 1
    x = 160 * (pallet_place // 3)
    y = 140 * (pallet_place % 3)
    place_above = trans(side_l, [x, y, 100, 0, 0, 0])
    place = trans(side_l, [x, y, 0, 0, 0, 0])
    place_above = coord_transform(place_above, ref_c, DR_BASE)
    place = coord_transform(place, ref_c, DR_BASE)
    movej(Global_safe)
    set_velx(225, 225)
    set_accx(300, 300)
    movej(side_j)
    movel(place_above)
    movel(place, vel=25)
    task_compliance_ctrl(stiffness)
    set_desired_force(f_d, f_dir)
    wait(2)
    set_digital_output(6, 1)
    wait(0.5)
    movel(place_above)
    release_force()
    release_compliance_ctrl()


def pick():
    stiffness = [500, 500, 500, 100, 100, 100]
    Handover_above = trans(Global_handover, [0, -100, 0, 0, 0, 0], DR_BASE)
    force_desired = 30.0  # set desired force
    f_d = [0.0, force_desired, 0.0, 0.0, 0.0, 0.0]  # set force direction
    f_dir = [0, 1, 0, 0, 0, 0]  # set axis at which force would be applied (x, y, z, a, b, c)
    movej(Global_safe)
    movej(Global_handover_j)
    movel(Handover_above)
    set_digital_output(6, 1)
    wait(0.5)
    SIDE = send("r2,r1,side", 1)
    data = send("r2,r1,ready", 1)
    if data == "ready":
        movel(Global_handover, vel=35)
        task_compliance_ctrl(stiffness)
        set_desired_force(f_d, f_dir)
        wait(2)
        set_digital_output(6, 0)
        wait(0.5)
    data = send("r2,r1,secured", 1)
    if data == "part_released":
        send("r2,r1,done", 0)
        movel(Handover_above)
    release_force()
    release_compliance_ctrl()
    movel(Global_safe)
