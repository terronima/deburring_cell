import socket
import sys
import threading

# constants
DEBURR_L_USR_CORD_ID = 106
BR_L_PALLET_USR_CORD = 107
BR_R_PALLET_USR_CORD = 108
R_1_COORD_SYS = 101
R_BRUSH_COORD_SYS = 102
L_BRUSH_COORD_SYS = 103
L_2_COORD_SYS = 104
L_F1_USR_CORD = 105
AIRBLOW_OUTPUT = 7
GREEN = 10
RED = 11
YELLOW = 12
GREET = 0
RIGHT_MOTOR = 16
LEFT_MOTOR = 15
GRIPPER_CLOSE = 9
GRIPPER_OPEN = 10
PART_PRESENT_SENSOR = 11

# Global variables
Global_standby = posj(-141.6, -0.31, 142.12, 2.05, 37.75, -141.84)
HMI_Offset = ""

# Global_Pick_L_j = posj(-138.03, 48.20, 91.53, 0.59, 38.24, -137.18)

# Velocity and Acceleration
deburr_vel = [850, 80]
jmove_vel = 80
intermediate_jmove_vel = 80
lmove_vel = 550
convergence_vel = 100
convergence_j_vel = 80
convergence_acc = 200
safe_acc = 400
pick_acc = 200
intermediate_acc = 200
deburr_acc = [600, 500]
set_tool("right part")
SIDE = ""
camera_map = ""
PICK_MODE = ""
PICK_FLAG = 0

#global pallet_place

# List of point for L Part faces
L_F1 = [Global_L_F1_P1, Global_L_F1_P2, Global_L_F1_P3, Global_L_F1_P4, Global_L_F1_P5, Global_L_F1_P6, Global_L_F1_P7]

L_F2 = [Global_L_F2_P1, Global_L_F2_P2, Global_L_F2_P3, Global_L_F2_P4, Global_L_F2_P5, Global_L_F2_P6, Global_L_F2_P7, Global_L_F2_P8]

L_F3 = [Global_L_F3_P1, Global_L_F3_P2, Global_L_F3_P3, Global_L_F3_P4, Global_L_F3_P5, Global_L_F3_P6, Global_L_F3_P7, Global_L_F3_P8]

L_F5 = [Global_L_F5_P1, Global_L_F5_P2, Global_L_F5_P3, Global_L_F5_P4, Global_L_F5_P5, Global_L_F5_P6, Global_L_F5_P7, Global_L_F5_P8]

L_F7 = [Global_L_F7_P1, Global_L_F7_P2, Global_L_F7_P3]

L_F8 = [Global_L_F8_P1, Global_L_F8_P2, Global_L_F8_P3]

L_F6 = [Global_L_F6_P1, Global_L_F6_P2, Global_L_F6_P3, Global_L_F6_P4, Global_L_F6_P5, Global_L_F6_P6, Global_L_F6_P7, Global_L_F6_P8]

L_F4 = [Global_L_F4_P1, Global_L_F4_P2, Global_L_F4_P3, Global_L_F4_P4, Global_L_F4_P5, Global_L_F4_P6, Global_L_F4_P7, Global_L_F4_P8]

# List of point for R Part faces
R_F1 = [Global_R_F1_P1, Global_R_F1_P2, Global_R_F1_P3, Global_R_F1_P4, Global_R_F1_P5, Global_R_F1_P6, Global_R_F1_P7, Global_R_F1_P8]

R_F2 = [Global_R_F2_P1, Global_R_F2_P2, Global_R_F2_P3, Global_R_F2_P4, Global_R_F2_P5, Global_R_F2_P6, Global_R_F2_P7, Global_R_F2_P8]

R_F3 = [Global_R_F3_P1, Global_R_F3_P2, Global_R_F3_P3, Global_R_F3_P4, Global_R_F3_P5, Global_R_F3_P6, Global_R_F3_P7, Global_R_F3_P8]

R_F5 = [Global_R_F5_P1, Global_R_F5_P2, Global_R_F5_P3, Global_R_F5_P4, Global_R_F5_P5, Global_R_F5_P6, Global_R_F5_P7, Global_R_F5_P8, Global_R_F5_P9]

R_F7 = [Global_R_F7_P1, Global_R_F7_P2, Global_R_F7_P3, Global_R_F7_P4, Global_R_F7_P5, Global_R_F7_P6, Global_R_F7_P7, Global_R_F7_P8]

R_F6 = [Global_R_F6_P1, Global_R_F6_P2, Global_R_F6_P3, Global_R_F6_P4, Global_R_F6_P5, Global_R_F6_P6, Global_R_F6_P7, Global_R_F6_P8, Global_R_F6_P9]

R_F4 = [Global_R_F4_P1, Global_R_F4_P2, Global_R_F4_P3, Global_R_F4_P4, Global_R_F4_P5, Global_R_F4_P6, Global_R_F4_P7, Global_R_F4_P8, Global_R_F4_P9]

R_F8 = [Global_R_F8_P1, Global_R_F8_P2, Global_R_F8_P3, Global_R_F8_P4, Global_R_F8_P5]

PAUSE = 0
NEW_COORDINATE_SYS = []
NEW_COORDINATE_SYS_FLAG = 0
HOST = "192.168.1.9"  # The server's hostname or IP address
PORT = 12347  # The port used by the server
FORMAT = "utf-8"
HEADER = 64
ADDR = (HOST, PORT)
GREETING_SENT = False
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg, resp_req): #0 - send no lsten, 1 send and lsten, 2 - no send only lsten    
    if resp_req != 2:
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * ((HEADER) - len(send_length))
        client.send(send_length)
        client.send(message)
    while resp_req != 0:
        data = client.recv(64).decode(FORMAT) 
        data = data.strip("z") 
        if data != "z":
            data = data.strip("z")
            #tp_log(str(data))
            return (data)
        time.sleep(1)

def send_camera_map(msg):
    data = ""
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * ((HEADER) - len(send_length))
    client.send(send_length)
    client.send(message)
    while True:
        data = client.recv(64).decode(FORMAT)
        data.strip("z")
        if data != "z":
            #tp_log(str(data))
            return (data)

def greet():
    global SIDE
    global PAUSE
    global PICK_MODE
    global client
    received = ""
    while True:
        try:
            received = client.recv(HEADER).decode(FORMAT)
        except:
            print("Failed")
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(ADDR)
            greet()
        if received == "name":
            data = "r1"
            send(data, 0)
            break    

def fn_th_HMI_Offset():
    global HMI_offset
    HMI_offset = float(send("r1,HMI,br_offset", 1))
    time.sleep(1)
    

# pick function to pick both L & R Parts
def pick(pos):
    tp_log("poaition: " +str(pos))
    tp_log("SIDE is " + str(SIDE))
    pallet_place = int(pos)    
    side_l = None
    side_j = None
    delta_x = None
    delta_y = None
    ref_c = None

    if (SIDE == "R" and pallet_place == 0):
        amovej(Global_pick_R_0_above_j, vel=jmove_vel, acc=pick_acc)
        mwait(0.5)
        set_digital_output(AIRBLOW_OUTPUT, 1)
        if get_digital_input(GRIPPER_CLOSE) == 1:
            movej(Global_pick_R_0_j, vel=convergence_j_vel, acc=convergence_acc)
        else:
            set_digital_output(AIRBLOW_OUTPUT, 1)
            movej(Global_pick_R_0_j, vel=convergence_j_vel, acc=convergence_acc)
        wait(2)
        if get_digital_input(PART_PRESENT_SENSOR):
            set_digital_output(AIRBLOW_OUTPUT, 0)
            if get_digital_input(GRIPPER_OPEN) == 1:
                movej(Global_pick_R_0_above_j, vel=convergence_j_vel, acc=convergence_acc)
                movej(Global_BR_HOME, vel=jmove_vel, acc=pick_acc)
            else:
                set_digital_output(AIRBLOW_OUTPUT, 0)
                wait(0.5)
                movej(Global_pick_R_0_above_j, vel=convergence_j_vel, acc=convergence_acc)
                movej(Global_BR_HOME, vel=jmove_vel, acc=pick_acc)
            PICK_FLAG = 1
        else:
            movej(Global_pick_R_0_above_j, vel=convergence_j_vel, acc=convergence_acc)
            movej(Global_BR_HOME, vel=jmove_vel, acc=pick_acc)
            PICK_FLAG = 0

    
    elif (SIDE == "R" and pallet_place == 1):
        amovej(Global_pick_R_1_above_j, vel=jmove_vel, acc=pick_acc)
        mwait(0.5)
        set_digital_output(AIRBLOW_OUTPUT, 1)
        if get_digital_input(GRIPPER_CLOSE) == 1:
            movej(Global_pick_R_1_j, vel=convergence_j_vel, acc=convergence_acc)
        else:
            set_digital_output(AIRBLOW_OUTPUT, 1)
            movej(Global_pick_R_1_j, vel=convergence_j_vel, acc=convergence_acc)
        wait(2)
        if get_digital_input(PART_PRESENT_SENSOR):
            set_digital_output(AIRBLOW_OUTPUT, 0)
            if get_digital_input(GRIPPER_OPEN) == 1:
                movej(Global_pick_R_1_above_j, vel=convergence_j_vel, acc=convergence_acc)
                movej(Global_BR_HOME, vel=jmove_vel, acc=pick_acc)
            else:
                set_digital_output(AIRBLOW_OUTPUT, 0)
                wait(0.5)
                movej(Global_pick_R_1_above_j, vel=convergence_j_vel, acc=convergence_acc)
                movej(Global_BR_HOME, vel=jmove_vel, acc=pick_acc)
            PICK_FLAG = 1
        else:
            movej(Global_pick_R_1_above_j, vel=convergence_j_vel, acc=convergence_acc)
            movej(Global_BR_HOME, vel=jmove_vel, acc=pick_acc)
            PICK_FLAG = 0

    
    else:
        # assign required parameters for pick process
        if SIDE == "L":  # if L then sets the picking position of L pallet
            ref_c = BR_L_PALLET_USR_CORD
            side_l = Global_pick_L_l
            side_j = Global_pick_L_j
            delta_x = 160 * (pallet_place // 3)
            delta_y = 140 * (pallet_place % 3)
        elif SIDE == "R":  # if R then sets the picking position of R pallet
            ref_c = BR_R_PALLET_USR_CORD
            side_l = Global_pick_R_l
            side_j = Global_pick_R_j
            delta_x = 160 * (pallet_place // 3)
            delta_y = 140 * (pallet_place % 3)
        #tp_log("SIDE is " + str(SIDE))
        tp_log("delta_x  = " + str(delta_x))
        tp_log("delta_y   = " + str(delta_y ))
        delta_val_above = trans(side_l, [delta_x, delta_y, 100, 0, 0, 0])
        delta_val = trans(side_l, [delta_x, delta_y, 0, 0, 0, 0])
        pick_pos_above = coord_transform(delta_val_above, ref_c, DR_BASE)
        pick_pos = coord_transform(delta_val, ref_c, DR_BASE)
        amovej(side_j, vel=jmove_vel, acc=pick_acc)
        mwait(0.5)
        set_digital_output(AIRBLOW_OUTPUT, 1)
        movel(pick_pos_above, vel=lmove_vel, acc=pick_acc)
        if get_digital_input(GRIPPER_CLOSE) == 1:
            movel(pick_pos, vel=convergence_vel, acc=convergence_acc)
        else:
            set_digital_output(AIRBLOW_OUTPUT, 1)
            movel(pick_pos, vel=convergence_vel, acc=convergence_acc)
        k_d = [500.0, 500.0, 500.0, 200.0, 200.0, 200.0]
        task_compliance_ctrl(k_d)
        force_desired = 10.0
        f_d = [0.0, 0.0, -force_desired, 0.0, 0.0, 0.0]
        f_dir = [0, 0, 1, 0, 0, 0]
        set_desired_force(f_d, f_dir)
        force_check = 10.0
        while True:
            #wait(3)
            force_condition = check_force_condition(DR_AXIS_Z, max=force_check)
            if get_digital_input(11) == 0:
                break
        wait(3)
        release_force()
        release_compliance_ctrl()
        if get_digital_input(PART_PRESENT_SENSOR):
            PICK_FLAG = 1
            tp_log("pick flag" +str(PICK_FLAG))
            set_digital_output(AIRBLOW_OUTPUT, 0)
            if get_digital_input(GRIPPER_OPEN) == 1:
                movel(pick_pos_above, vel=convergence_vel, acc=pick_acc)
            else:
                set_digital_output(AIRBLOW_OUTPUT, 0)
                movel(pick_pos_above, vel=convergence_vel, acc=pick_acc)
        else:
            movel(pick_pos_above, vel=convergence_vel, acc=pick_acc)
            PICK_FLAG = 0
            tp_log("pick flag" +str(PICK_FLAG))
        movej(Global_BR_HOME, vel=jmove_vel, acc=pick_acc)
        set_ref_coord(DR_BASE)

    return PICK_FLAG

def L_F1_deburr(L_F1, ref_c, delta_x, delta_y, delta_z):
    delta_z -= 10
    delta_z += HMI_offset
    L_F1_points = []
    movej(Global_L_F1_centre_j, vel=jmove_vel, acc=safe_acc)
    for i in range(0, len(L_F1)):
            L_Face_point = trans(L_F1[i],[delta_x, delta_y, delta_z, 0, 0, 0], ref_c, ref_c)
            L_F1_points.append(L_Face_point)
    movel(L_F1_points[0], vel=lmove_vel, acc=safe_acc)
    movesx([L_F1_points[1], L_F1_points[2], L_F1_points[3], L_F1_points[4], L_F1_points[5], L_F1_points[6]], vel=deburr_vel, acc=deburr_acc)
    amovel(Global_L_F1_Backoff, vel=lmove_vel, acc=safe_acc)
    mwait(0)

def L_F2_deburr(L_F2, ref_c, delta_x, delta_y, delta_z):
    delta_z -= 10
    delta_z += HMI_offset
    L_F2_points = []
    movej(Global_L_F2_centre_j, vel=jmove_vel, acc=safe_acc)
    for i in range(0, len(L_F2)):
            L_Face_point = trans(L_F2[i],[delta_x, delta_y, delta_z, 0, 0, 0], ref_c, ref_c)
            L_F2_points.append(L_Face_point)
    movel(L_F2_points[0], vel=lmove_vel, acc=safe_acc)
    movesx([L_F2_points[1], L_F2_points[2], L_F2_points[3], L_F2_points[4], L_F2_points[5], L_F2_points[6], L_F2_points[7]], vel=deburr_vel, acc=deburr_acc)
    amovel(Global_L_F2_Backoff, vel=lmove_vel, acc=safe_acc)
    mwait(0)

def L_F3_deburr(L_F3, ref_c, delta_x, delta_y, delta_z):
    delta_z -= 11
    delta_z += HMI_offset
    L_F3_points = []
    movej(Global_L_F3_centre_j, vel=jmove_vel, acc=safe_acc)
    for i in range(0, len(L_F3)):
            L_Face_point = trans(L_F3[i],[delta_x, delta_y, delta_z, 0, 0, 0], ref_c, ref_c)
            L_F3_points.append(L_Face_point)
    movel(L_F3_points[0], vel=lmove_vel, acc=safe_acc)
    movel(L_F3_points[1], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(L_F3_points[2], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(L_F3_points[3], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(L_F3_points[4], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(L_F3_points[5], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(L_F3_points[6], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(L_F3_points[7], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    amovel(Global_L_F3_Backoff, vel=lmove_vel, acc=safe_acc)
    mwait(0)

def L_F5_deburr(L_F5, ref_c, delta_x, delta_y, delta_z):
    delta_z -= 11
    delta_z += HMI_offset
    L_F5_points = []
    movej(Global_L_F5_centre_j, vel=jmove_vel, acc=safe_acc)
    for i in range(0, len(L_F5)):
            L_Face_point = trans(L_F5[i],[delta_x, delta_y, delta_z, 0, 0, 0], ref_c, ref_c)
            L_F5_points.append(L_Face_point)
    movel(L_F5_points[0], vel=lmove_vel, acc=safe_acc)
    movel(L_F5_points[1], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(L_F5_points[2], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(L_F5_points[3], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(L_F5_points[4], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(L_F5_points[5], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(L_F5_points[6], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(L_F5_points[7], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    amovel(Global_L_F5_Backoff, vel=lmove_vel, acc=safe_acc)
    mwait(0)

def L_F7_deburr(L_F7, ref_c, delta_x, delta_y, delta_z):
    delta_z -= 12
    delta_z += HMI_offset
    L_F7_points = []
    movej(Global_L_F7_centre_j, vel=jmove_vel, acc=safe_acc)
    for i in range(0, len(L_F7)):
            L_Face_point = trans(L_F7[i],[delta_x, delta_y, delta_z, 0, 0, 0], ref_c, ref_c)
            L_F7_points.append(L_Face_point)
    movel(L_F7_points[0], vel=lmove_vel, acc=safe_acc)
    movec(L_F7_points[1], L_F7_points[2], vel=deburr_vel, acc=deburr_acc)
    amovel(Global_L_F7_Backoff, vel=lmove_vel, acc=safe_acc)
    mwait(0)

def L_F8_deburr(L_F8, ref_c, delta_x, delta_y, delta_z):
    delta_z -= 11
    delta_z += HMI_offset
    L_F8_points = []
    movej(Global_L_F8_centre_j, vel=jmove_vel, acc=safe_acc)
    for i in range(0, len(L_F8)):
            L_Face_point = trans(L_F8[i],[delta_x, delta_y, delta_z, 0, 0, 0], ref_c, ref_c)
            L_F8_points.append(L_Face_point)
    movel(L_F8_points[0], vel=lmove_vel, acc=safe_acc)
    movec(L_F8_points[1], L_F8_points[2], vel=deburr_vel, acc=deburr_acc)
    amovel(Global_L_F8_Backoff, vel=lmove_vel, acc=safe_acc)
    mwait(0)

def L_F6_deburr(L_F6, ref_c, delta_x, delta_y, delta_z):
    delta_z -= 11
    delta_z += HMI_offset
    L_F6_points = []
    movej(Global_L_F6_centre_j, vel=jmove_vel, acc=safe_acc)
    for i in range(0, len(L_F6)):
            L_Face_point = trans(L_F6[i],[delta_x, delta_y, delta_z, 0, 0, 0], ref_c, ref_c)
            L_F6_points.append(L_Face_point)
    movel(L_F6_points[0], vel=lmove_vel, acc=safe_acc)
    movel(L_F6_points[1], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(L_F6_points[2], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(L_F6_points[3], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(L_F6_points[4], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(L_F6_points[5], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(L_F6_points[6], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(L_F6_points[7], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    amovel(Global_L_F6_Backoff, vel=lmove_vel, acc=safe_acc)
    mwait(0)

def L_F4_deburr(L_F4, ref_c, delta_x, delta_y, delta_z):
    delta_z -= 11
    delta_z += HMI_offset
    L_F4_points = []
    movej(Global_L_F4_centre_j, vel=jmove_vel, acc=safe_acc)
    for i in range(0, len(L_F4)):
            L_Face_point = trans(L_F4[i],[delta_x, delta_y, delta_z, 0, 0, 0], ref_c, ref_c)
            L_F4_points.append(L_Face_point)
    movel(L_F4_points[0], vel=lmove_vel, acc=safe_acc)
    movel(L_F4_points[1], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(L_F4_points[2], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(L_F4_points[3], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(L_F4_points[4], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(L_F4_points[5], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(L_F4_points[6], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(L_F4_points[7], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    amovel(Global_L_F4_Backoff, vel=lmove_vel, acc=safe_acc)
    mwait(0)

# Deburr L_B1 function
def deburr_L_B1(ref_c):
    delta_x = None
    delta_y = None
    delta_z = None
    set_digital_output(RIGHT_MOTOR, 1)
    set_digital_output(LEFT_MOTOR, 0)
    amovej(Global_L_B1_Reference_j, vel=jmove_vel, acc=safe_acc)
    mwait(0)
    set_ref_coord(ref_c)          
    movel(Global_L_B1_Reference, vel=lmove_vel, acc=safe_acc)
    wait(1)
    k_d1 = [1500.0, 1500.0, 1500.0, 1000.0, 1000.0, 1000.0]
    task_compliance_ctrl(k_d1)
    force_desired = 20
    f_d = [0.0, 0.0, force_desired, 0.0, 0.0, 0.0]
    f_dir = [0, 0, 1, 0, 0, 0]
    set_desired_force(f_d, f_dir)
    force_condition = check_force_condition(DR_AXIS_Z, max=force_desired)
    while (force_condition):
        #wait(3)
        force_condition = check_force_condition(DR_AXIS_Z, max=force_desired)
        if force_condition == 0:
            break
    release_compliance_ctrl()
    new_centre_position = get_current_posx()
    new_centre_position = new_centre_position[0]
    tp_log("ref coord position: " + str(new_centre_position))
    NEW_COORDINATE_SYS_FLAG = 1    
    movej(Global_L_B1_Reference_j, vel=jmove_vel, acc=safe_acc)
    delta = subtract_pose(new_centre_position, Global_L_B1_Reference)
    tp_log("delta: " + str(delta))
    delta_x = delta[0]
    delta_y = delta[1]
    delta_z = delta[2]
    tp_log("delta_x: " + str(delta_x))
    tp_log("delta_y: " + str(delta_y))
    tp_log("delta_z: " + str(delta_z))
    set_ref_coord(ref_c)
    L_F1_deburr(L_F1, ref_c, delta_x, delta_y, delta_z)
    L_F3_deburr(L_F3, ref_c, delta_x, delta_y, delta_z)
    L_F6_deburr(L_F6, ref_c, delta_x, delta_y, delta_z)

    set_ref_coord(R_1_COORD_SYS)
    L_F7_deburr(L_F7, R_1_COORD_SYS, delta_x, delta_y, delta_z)
    wait(0.5)
    set_digital_output(RIGHT_MOTOR, 0)
    set_digital_output(LEFT_MOTOR, 0)
    release_force( 0.1 )

# Deburr L_B2 function
def deburr_L_B2(ref_c):
    delta_x = None
    delta_y = None
    delta_z = None
    set_digital_output(RIGHT_MOTOR, 0)
    set_digital_output(LEFT_MOTOR, 1)
    amovej(Global_L_B2_Reference_j, vel=jmove_vel, acc=safe_acc)
    mwait(0)
    set_ref_coord(ref_c)          
    movel(Global_L_B2_Reference, vel=lmove_vel, acc=safe_acc)
    k_d1 = [1500.0, 1500.0, 1500.0, 1000.0, 1000.0, 1000.0]
    task_compliance_ctrl(k_d1)
    force_desired = 20
    f_d = [0.0, 0.0, force_desired, 0.0, 0.0, 0.0]
    f_dir = [0, 0, 1, 0, 0, 0]
    set_desired_force(f_d, f_dir)
    force_condition = check_force_condition(DR_AXIS_Z, max=force_desired)
    while (force_condition):
        #wait(3)
        force_condition = check_force_condition(DR_AXIS_Z, max=force_desired)
        if force_condition == 0:
            break
    release_compliance_ctrl()
    new_centre_position = get_current_posx()
    new_centre_position = new_centre_position[0]
    tp_log("ref coord position: " + str(new_centre_position))
    NEW_COORDINATE_SYS_FLAG = 1    
    movej(Global_L_B2_Reference_j, vel=jmove_vel, acc=safe_acc)
    delta = subtract_pose(new_centre_position, Global_L_B2_Reference)
    tp_log("delta: " + str(delta))
    delta_x = delta[0]
    delta_y = delta[1]
    delta_z = delta[2]
    set_ref_coord(ref_c)
    L_F5_deburr(L_F5, ref_c, delta_x, delta_y, delta_z)
    L_F4_deburr(L_F4, ref_c, delta_x, delta_y, delta_z)
    L_F2_deburr(L_F2, ref_c, delta_x, delta_y, delta_z)

    set_ref_coord(L_2_COORD_SYS)
    L_F8_deburr(L_F8, L_2_COORD_SYS, delta_x, delta_y, delta_z)
    wait(0.5)
    set_digital_output(RIGHT_MOTOR, 0)
    set_digital_output(LEFT_MOTOR, 0)
    release_force( 0.1 )

def R_F1_deburr(R_F1, ref_c, delta_x, delta_y, delta_z):
    R_F1_points = []
    delta_z -= 10
    delta_z += HMI_offset
    tp_log("delta_x: " + str(delta_x))
    tp_log("delta_y: " + str(delta_y))
    tp_log("delta_z: " + str(delta_z))
    movej(Global_R_F1_centre_j, vel=jmove_vel, acc=safe_acc)
    for i in range(0, len(R_F1)):
            R_Face_point = trans(R_F1[i],[delta_x, delta_y, delta_z, 0, 0, 0], ref_c, ref_c)
            R_F1_points.append(R_Face_point)
    movel(R_F1_points[0], vel=lmove_vel, acc=safe_acc)
    movesx([R_F1_points[1], R_F1_points[2], R_F1_points[3], R_F1_points[4], R_F1_points[5], R_F1_points[6], R_F1_points[7]], vel=deburr_vel, acc=deburr_acc)
    #movel(R_F1_points[0], vel=lmove_vel, acc=safe_acc)
    #movel(R_F1_points[1], vel=lmove_vel, acc=safe_acc, r=	50, ra=DR_MV_RA_DUPLICATE)
    #movel(R_F1_points[2], vel=lmove_vel, acc=safe_acc, r=	50, ra=DR_MV_RA_DUPLICATE)
    #movec(R_F1_points[1], R_F1_points[2], vel=deburr_vel, acc=deburr_acc, ori = DR_MV_ORI_RADIAL)
    #movel(R_F1_points[3], vel=lmove_vel, acc=safe_acc)
    #movej(Global_R_F1_REORIENT_J, vel=jmove_vel, acc=safe_acc)
    #movel(R_F1_points[2], vel=lmove_vel, acc=safe_acc, r=	50, ra=DR_MV_RA_DUPLICATE)
    #movel(R_F1_points[4], vel=lmove_vel, acc=safe_acc, r=50, ra=DR_MV_RA_DUPLICATE)
    #movel(R_F1_points[5], vel=lmove_vel, acc=safe_acc, r=	50, ra=DR_MV_RA_DUPLICATE)
    #movel(R_F1_points[6], vel=lmove_vel, acc=safe_acc, r=50, ra=DR_MV_RA_DUPLICATE)
    #movel(R_F1_points[7], vel=lmove_vel, acc=safe_acc, r=	50, ra=DR_MV_RA_DUPLICATE)
    #movec(R_F1_points[4], R_F1_points[5], vel=deburr_vel, acc=deburr_acc, ori = DR_MV_ORI_TEACH)
    amovel(Global_R_F1_Backoff, vel=lmove_vel, acc=safe_acc)
    mwait(0)

def R_F2_deburr(R_F2, ref_c, delta_x, delta_y, delta_z):
    R_F2_points = []
    delta_z -= 10
    delta_z += HMI_offset
    movej(Global_R_F2_centre_j, vel=jmove_vel, acc=safe_acc)
    for i in range(0, len(R_F2)):
            R_Face_point = trans(R_F2[i],[delta_x, delta_y, delta_z, 0, 0, 0], ref_c, ref_c)
            R_F2_points.append(R_Face_point)
    movel(R_F2_points[0], vel=lmove_vel, acc=safe_acc)
    movesx([R_F2_points[1], R_F2_points[2], R_F2_points[3], R_F2_points[4], R_F2_points[5], R_F2_points[6], R_F2_points[7]], vel=deburr_vel, acc=deburr_acc)
    #movel(R_F2_points[1], vel=lmove_vel, acc=safe_acc)
    #movel(R_F2_points[2], vel=lmove_vel, acc=safe_acc, r=35, ra=DR_MV_RA_DUPLICATE)
    #movel(R_F2_points[3], vel=lmove_vel, acc=safe_acc, r=35, ra=DR_MV_RA_DUPLICATE)
    #movel(R_F2_points[4], vel=lmove_vel, acc=safe_acc)
    #movec(R_F2_points[1], R_F2_points[2], vel=deburr_vel, acc=deburr_acc, ori = DR_MV_ORI_TEACH)
    amovel(Global_R_F2_Backoff, vel=lmove_vel, acc=safe_acc)
    mwait(0)

def R_F3_deburr(R_F3, ref_c, delta_x, delta_y, delta_z):
    R_F3_points = []
    delta_z -= 11
    delta_z += HMI_offset
    movej(Global_R_F3_centre_j, vel=jmove_vel, acc=safe_acc)
    for i in range(0, len(R_F3)):
            R_Face_point = trans(R_F3[i],[delta_x+0.5, 0, delta_z-0.5, 0, 0, 0], ref_c, ref_c)
            R_F3_points.append(R_Face_point)
    movel(R_F3_points[0], vel=lmove_vel, acc=safe_acc)
    movel(R_F3_points[1], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(R_F3_points[2], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(R_F3_points[3], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(R_F3_points[4], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(R_F3_points[5], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(R_F3_points[6], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(R_F3_points[7], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    #movec(R_F3_points[2], R_F3_points[3], vel=deburr_vel, acc=deburr_acc, ori = DR_MV_ORI_RADIAL)
    amovel(Global_R_F3_Backoff, vel=lmove_vel, acc=safe_acc)
    mwait(0)

def R_F5_deburr(R_F5, ref_c, delta_x, delta_y, delta_z):
    R_F5_points = []
    delta_z -= 11
    delta_z += HMI_offset
    movej(Global_R_F5_centre_j, vel=jmove_vel, acc=safe_acc)
    for i in range(0, len(R_F5)):
            R_Face_point = trans(R_F5[i],[delta_x+1, 0, delta_z-1, 0, 0, 0], ref_c, ref_c)
            R_F5_points.append(R_Face_point)
    movel(R_F5_points[0], vel=lmove_vel, acc=safe_acc)
    movel(R_F5_points[1], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(R_F5_points[2], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(R_F5_points[3], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(R_F5_points[4], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(R_F5_points[5], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(R_F5_points[6], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(R_F5_points[7], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(R_F5_points[8], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    #movec(R_F5_points[2], R_F5_points[3], vel=deburr_vel, acc=deburr_acc, ori = DR_MV_ORI_RADIAL)
    amovel(Global_R_F5_Backoff, vel=lmove_vel, acc=safe_acc)
    mwait(0)

def R_F7_deburr(R_F7, ref_c, delta_x, delta_y, delta_z):
    R_F7_points = []
    delta_z -= 11
    delta_z += HMI_offset
    movej(Global_R_F7_centre_j, vel=jmove_vel, acc=safe_acc)
    for i in range(0, len(R_F7)):
            R_Face_point = trans(R_F7[i],[delta_x, delta_y, delta_z, 0, 0, 0], ref_c, ref_c)
            R_F7_points.append(R_Face_point)
    movel(R_F7_points[0], vel=lmove_vel, acc=safe_acc)
    movesx([R_F7_points[1], R_F7_points[2], R_F7_points[3], R_F7_points[4], R_F7_points[5]], vel=deburr_vel, acc=deburr_acc)
    amovel(Global_R_F7_Backoff, vel=lmove_vel, acc=safe_acc)
    mwait(0)

def R_F6_deburr(R_F6, ref_c, delta_x, delta_y, delta_z):
    R_F6_points = []
    delta_z -= 11.5
    delta_z += HMI_offset
    movej(Global_R_F6_centre_j, vel=jmove_vel, acc=safe_acc)
    for i in range(0, len(R_F6)):
            R_Face_point = trans(R_F6[i],[delta_x, delta_y, delta_z, 0, 0, 0], ref_c, ref_c)
            R_F6_points.append(R_Face_point)
    movel(R_F6_points[0], vel=lmove_vel, acc=safe_acc)
    #movesx([R_F6_points[1], R_F6_points[2], R_F6_points[3], R_F6_points[4], R_F6_points[5], R_F6_points[6], R_F6_points[7], R_F6_points[8]], vel=deburr_vel, acc=deburr_acc)
    movel(R_F6_points[1], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(R_F6_points[2], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(R_F6_points[3], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(R_F6_points[4], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(R_F6_points[5], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(R_F6_points[6], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(R_F6_points[7], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(R_F6_points[8], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    #movec(R_F6_points[2], R_F6_points[3], vel=deburr_vel, acc=deburr_acc, ori = DR_MV_ORI_TEACH)
    amovel(Global_R_F6_Backoff, vel=lmove_vel, acc=safe_acc)
    mwait(0)

def R_F4_deburr(R_F4, ref_c, delta_x, delta_y, delta_z):
    R_F4_points = []
    delta_z -= 11
    delta_z += HMI_offset
    movej(Global_R_F4_centre_j, vel=jmove_vel, acc=safe_acc)
    for i in range(0, len(R_F4)):
            R_Face_point = trans(R_F4[i],[delta_x, delta_y, delta_z, 0, 0, 0], ref_c, ref_c)
            R_F4_points.append(R_Face_point)
    movel(R_F4_points[0], vel=lmove_vel, acc=safe_acc)
    movel(R_F4_points[1], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(R_F4_points[2], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(R_F4_points[3], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(R_F4_points[4], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(R_F4_points[5], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(R_F4_points[6], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(R_F4_points[7], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    movel(R_F4_points[8], vel=lmove_vel, acc=safe_acc,  r=20, ra=DR_MV_RA_DUPLICATE)
    #movec(R_F4_points[2], R_F4_points[3], vel=deburr_vel, acc=deburr_acc, ori = DR_MV_ORI_TEACH)
    amovel(Global_R_F4_Backoff, vel=lmove_vel, acc=safe_acc)
    mwait(0)

def R_F8_deburr(R_F8, ref_c, delta_x, delta_y, delta_z):
    R_F8_points = []
    delta_z -= 12
    delta_z += HMI_offset
    movej(Global_R_F8_centre_j, vel=jmove_vel, acc=safe_acc)
    for i in range(0, len(R_F8)):
            R_Face_point = trans(R_F8[i],[delta_x, delta_y, delta_z, 0, 0, 0], ref_c, ref_c)
            R_F8_points.append(R_Face_point)
    movel(R_F8_points[0], vel=lmove_vel, acc=safe_acc)
    movec(R_F8_points[1], R_F8_points[2], vel=deburr_vel, acc=deburr_acc)
    movec(R_F8_points[3], R_F8_points[4], vel=deburr_vel, acc=deburr_acc)
    amovel(Global_R_F8_Backoff, vel=lmove_vel, acc=safe_acc)
    mwait(0)

# Deburr R_B1 function
def deburr_R_B1(ref_c):
    new_centre_position = None
    delta = None
    delta_x = None
    delta_y = None
    delta_z = None
    set_digital_output(RIGHT_MOTOR, 1)
    set_digital_output(LEFT_MOTOR, 0)
    amovej(Global_R_B1_Reference_j, vel=jmove_vel, acc=safe_acc)
    mwait(0)
    set_ref_coord(ref_c)          
    movel(Global_R_B1_Reference, vel=lmove_vel, acc=safe_acc)
    k_d1 = [1500.0, 1500.0, 1500.0, 1000.0, 1000.0, 1000.0]
    task_compliance_ctrl(k_d1)
    force_desired = 20
    f_d = [0.0, 0.0, force_desired, 0.0, 0.0, 0.0]
    f_dir = [0, 0, 1, 0, 0, 0]
    set_desired_force(f_d, f_dir)
    force_condition = check_force_condition(DR_AXIS_Z, max=force_desired)
    while (force_condition):
        #wait(3)
        force_condition = check_force_condition(DR_AXIS_Z, max=force_desired)
        if force_condition == 0:
            break
    release_compliance_ctrl()
    new_centre_position = get_current_posx()
    new_centre_position = new_centre_position[0]
    tp_log("ref coord position: " + str(new_centre_position))
    NEW_COORDINATE_SYS_FLAG = 1    
    movej(Global_R_B1_Reference_j, vel=jmove_vel, acc=safe_acc)
    delta = subtract_pose(new_centre_position, Global_R_B1_Reference)
    tp_log("delta: " + str(delta))
    delta_x = delta[0]
    delta_y = delta[1]
    delta_z = delta[2]
    tp_log("delta_x: " + str(delta_x))
    tp_log("delta_y: " + str(delta_y))
    tp_log("delta_z: " + str(delta_z))
    set_ref_coord(ref_c)
    R_F1_deburr(R_F1, ref_c, delta_x, delta_y, delta_z)
    R_F2_deburr(R_F2, ref_c, delta_x, delta_y, delta_z)
    R_F3_deburr(R_F3, ref_c, delta_x, delta_y, delta_z)
    R_F5_deburr(R_F5, ref_c, delta_x, delta_y, delta_z)

    set_ref_coord(R_1_COORD_SYS)
    R_F7_deburr(R_F7, R_1_COORD_SYS, delta_x, delta_y, delta_z)
    wait(0.5)
    set_digital_output(RIGHT_MOTOR, 0)
    set_digital_output(LEFT_MOTOR, 0)
    release_force( 0.1 )
# Deburr R_B2 function
def deburr_R_B2(ref_c):
    new_centre_position = None
    delta = None
    delta_x = None
    delta_y = None
    delta_z = None
    set_digital_output(RIGHT_MOTOR, 0)
    set_digital_output(LEFT_MOTOR, 1)
    amovej(Global_R_B2_Reference_j, vel=jmove_vel, acc=safe_acc)
    mwait(0)
    set_ref_coord(ref_c)          
    movel(Global_R_B2_Reference, vel=lmove_vel, acc=safe_acc)
    k_d1 = [1500.0, 1500.0, 1500.0, 1000.0, 1000.0, 1000.0]
    task_compliance_ctrl(k_d1)
    force_desired = 20
    f_d = [0.0, 0.0, force_desired, 0.0, 0.0, 0.0]
    f_dir = [0, 0, 1, 0, 0, 0]
    set_desired_force(f_d, f_dir)
    force_condition = check_force_condition(DR_AXIS_Z, max=force_desired)
    while (force_condition):
        #wait(3)
        force_condition = check_force_condition(DR_AXIS_Z, max=force_desired)
        if force_condition == 0:
            break
    release_compliance_ctrl()
    new_centre_position = get_current_posx()
    new_centre_position = new_centre_position[0]
    tp_log("ref coord position: " + str(new_centre_position))
    NEW_COORDINATE_SYS_FLAG = 1    
    movej(Global_R_B2_Reference_j, vel=jmove_vel, acc=safe_acc)
    delta = subtract_pose(new_centre_position, Global_R_B2_Reference)
    tp_log("delta: " + str(delta))
    delta_x = delta[0]
    delta_y = delta[1]
    delta_z = delta[2]
    set_ref_coord(ref_c)
    R_F6_deburr(R_F6, ref_c, delta_x, delta_y, delta_z)
    R_F4_deburr(R_F4, ref_c, delta_x, delta_y, delta_z)

    set_ref_coord(L_2_COORD_SYS)
    R_F8_deburr(R_F8, L_2_COORD_SYS, delta_x, delta_y, delta_z)
    wait(0.5)
    set_digital_output(RIGHT_MOTOR, 0)
    set_digital_output(LEFT_MOTOR, 0)
    release_force( 0.1 )

def handover():
    set_ref_coord(DR_BASE)
    movej(Global_BR_HOME, vel=jmove_vel, acc=safe_acc)
    movej(Global_handover_j, vel=jmove_vel, acc=safe_acc)
    while True:
        send("r1,r2,wake", 0)
        in_data = send("", 2)
        #tp_popup("in_data: "+in_data, DR_PM_MESSAGE)
        if in_data == "side":
            send(str("r1,r2," +SIDE), 0)
            break
    while True:
        ready_state = send("", 2)
        #tp_popup("ready_state: "+ready_state, DR_PM_MESSAGE)
        if ready_state == "ready":
            send("r1,r2,okay", 0)
            break
    while True:
        secured = send("", 2)
        #tp_popup("secured: "+secured, DR_PM_MESSAGE)
        if secured == "secured":
            set_digital_output(7, 1)
            break
    send("r1,r2,part_released",0)
    while True:
        done = send("", 2)
        #tp_popup("done: "+done, DR_PM_MESSAGE)
        if done == "done":
            if SIDE == "R":
                send("r1,HMI,qbr", 0)
            elif SIDE == "L":
                send("r1,HMI,qbl", 0)
            break
    movel(Global_handover_l, vel=100, acc=100)
    movej(Global_BR_HOME, vel=jmove_vel, acc=safe_acc)

def Estop_recovery():
    set_digital_output(RIGHT_MOTOR, 0)
    set_digital_output(LEFT_MOTOR, 0)
    set_ref_coord(DR_BASE)
    current_position = get_current_posx()
    current_position = current_position[0]
    safe_position = trans(current_position, [0,-50, 200, 0, 0, 0], DR_BASE, DR_BASE)
    movel(safe_position, vel=intermediate_acc, acc=safe_acc)
    wait(0.5)
    movej(Global_estop_recovery_point, vel=50, acc=30)
    set_digital_output(AIRBLOW_OUTPUT ,1)
    #wait_nudge()
    wait(5)
    move_home(DR_HOME_TARGET_USER)


def left_only_MODE(pallet_map):
    global SIDE
    SIDE = "L"
    cntr = 9
    for i in range(int(len(pallet_map[9::])), int(len(pallet_map))):
        if pallet_map[i] == 1:
            pallet_place = cntr - 9
            return pallet_place
        cntr += 1
            

def right_only_MODE(pallet_map):
    global SIDE
    SIDE = "R"
    cntr = 0
    for i in range(0, int(len(pallet_map[0:9]))):
        if pallet_map[i] == 1:
            pallet_place = cntr
            return pallet_place
        cntr += 1

def intermittent_MODE(pallet_map):
    global SIDE
    cntr = 0
    for i in range(0, int(len(pallet_map[0:9]))):
        pick_el_1 = i
        if pallet_map[pick_el_1] == 1:
            SIDE = "R"
            pallet_place = cntr
            return pallet_place
            # string_of_picks += str(i) + ','
        pick_el_2 = i + int(len(pallet_map) / 2)
        if pallet_map[pick_el_2] == 1:
            SIDE = "L"
            pallet_place = cntr
            return pallet_place
        cntr += 1
            # string_of_picks += str(pick_el_2) + ','

def side_by_side_MODE(pallet_map):
    global SIDE
    cntr = 0
    for i in range(0, int(len(pallet_map[0:9]))):
        if pallet_map[i] == 1:
            SIDE = "R"
            pallet_place = cntr
            return pallet_place
        cntr += 1
        if cntr >= 9:
            for i in range(int(len(pallet_map[9::])), int(len(pallet_map))):
                if pallet_map[i] == 1:
                    SIDE = "L"
                    pallet_place = cntr - 9
                    return pallet_place
                cntr += 1