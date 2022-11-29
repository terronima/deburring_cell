import socket
import time
import sys
import threading

# constants
DEBURR_L_USR_CORD_ID = 106
BR_L_PALLET_USR_CORD = 107
BR_R_PALLET_USR_CORD = 108
R_1_COORD_SYS = 101
R_2_COORD_SYS = 102
L_1_COORD_SYS = 103
L_2_COORD_SYS = 104
L_F1_USR_CORD = 105
AIRBLOW_OUTPUT = 7
GREEN = 10
RED = 11
YELLOW = 12
GREET = 0
RIGHT_MOTOR = 13
LEFT_MOTOR = 14
PART_PRESENT_SENSOR = 11
# Global variables
Global_standby = posj(-141.6, -0.31, 142.12, 2.05, 37.75, -141.84)

# Global_Pick_L_j = posj(-138.03, 48.20, 91.53, 0.59, 38.24, -137.18)

# Velocity and Acceleration
deburr_vel = [800, 80]
jmove_vel = 80
intermediate_jmove_vel = 80
lmove_vel = 550
convergence_vel = 100
convergence_j_vel = 80
convergence_acc = 200
safe_acc = 400
pick_acc = 300
intermediate_acc = 200
deburr_acc = [550, 400]
set_tool("right part")
SIDE = "L"
camera_map = ""

# ONLY_LEFT = 1, ONLY_RIGHT = 2, INTERMITTENT = 3, SIDE_BY_SIDE = 4
PICK_MODE = ""

#global pallet_place

# List of point for L Part faces
L_F1 = [Global_L_F1_centre_j, Global_L_F1_centre, Global_L_F1_P1, Global_L_F1_P2, Global_L_F1_P3, Global_L_F1_P4,
        Global_L_F1_P5, Global_L_F1_P6, Global_L_F1_P7, Global_L_F1_P8, Global_L_F1_Backoff, 1]

L_F2 = [Global_L_F2_centre_j, Global_L_F2_centre, Global_L_F2_P1, Global_L_F2_P2, Global_L_F2_P3, Global_L_F2_P4,
        Global_L_F2_Backoff, 2]

L_F2_2 = [Global_L_F2_2_centre_j, Global_L_F2_2_centre, Global_L_F2_2_P1, Global_L_F2_2_P2, Global_L_F2_2_P3,
          Global_L_F2_2_Backoff]

L_F3 = [Global_L_F3_centre_j, Global_L_F3_centre, Global_L_F3_P1, Global_L_F3_P2, Global_L_F3_P3, Global_L_F3_P4,
        Global_L_F3_P5, Global_L_F3_P6, Global_L_F3_Backoff]
L_F4 = [Global_L_F4_centre_j, Global_L_F4_centre, Global_L_F4_P1, Global_L_F4_P2, Global_L_F4_P3, Global_L_F4_P4,
        Global_L_F4_P5, Global_L_F4_P6, Global_L_F4_Backoff]

L_F5 = [Global_L_F5_centre_j, Global_L_F5_centre, Global_L_F5_P1, Global_L_F5_P2, Global_L_F5_P3, Global_L_F5_P4,
        Global_L_F5_P5, Global_L_F5_P6, Global_L_F5_Backoff]

L_F6 = [Global_L_F6_centre_j, Global_L_F6_centre, Global_L_F6_P1, Global_L_F6_P2, Global_L_F6_P3, Global_L_F6_P4,
        Global_L_F6_P5, Global_L_F6_P6, Global_L_F6_Backoff, 6]

L_F7 = [Global_L_F7_centre_j, Global_L_F7_P1, Global_L_F7_P2, Global_L_F7_P3, Global_L_F7_P4, Global_L_F7_P5,
        Global_L_F7_Backoff, 7]

L_F7_2 = [Global_L_F7_2_centre_j, Global_L_F7_2_centre, Global_L_F7_2_P4, Global_L_F7_2_P2, Global_L_F7_2_P1,
          Global_L_F7_2_Backoff, 72]

L_F8 = [Global_L_F8_centre_j, Global_L_F8_centre, Global_L_F8_P3, Global_L_F8_P2, Global_L_F8_P1, Global_L_F8_Backoff,
        8]

L_F8_2 = [Global_L_F8_2_centre_j, Global_L_F8_2_centre, Global_L_F8_2_P1, Global_L_F8_2_P2, Global_L_F8_2_P3,
          Global_L_F8_2_P4, Global_L_F8_2_Backoff, 82]

# List of point for R Part faces
R_F1 = [Global_R_F1_centre_j, Global_R_F1_centre, Global_R_F1_P1, Global_R_F1_P2, Global_R_F1_P3, Global_R_F1_P4,
        Global_R_F1_P5, Global_R_F1_P6, Global_R_F1_P7, Global_R_F1_P8, Global_R_F1_Backoff, 1]

R_F2 = [Global_R_F2_centre_j, 1, Global_R_F2_P1, Global_R_F2_P2, Global_R_F2_P3, Global_R_F2_P4, Global_R_F2_P5,
        Global_R_F2_P6, Global_R_F2_Backoff, 2]

R_F2_2 = [Global_R_F2_2_centre_j, 1, Global_R_F2_2_Test, Global_R_F2_2_P1, Global_R_F2_2_P2, Global_R_F2_2_P3,
          Global_R_F2_2_P4, Global_R_F2_2_Backoff, 22]

R_F3 = [Global_R_F3_centre_j, 1, Global_R_F3_P1, Global_R_F3_P2, Global_R_F3_P3, Global_R_F3_P4, Global_R_F3_P5,
        Global_R_F3_P6, Global_R_F3_Backoff]

R_F4 = [Global_R_F4_centre_j, 1, Global_R_F4_P1, Global_R_F4_P2, Global_R_F4_P3, Global_R_F4_P4, Global_R_F4_P5,
        Global_R_F4_Backoff]

R_F5 = [Global_R_F5_centre_j, 1, Global_R_F5_P1, Global_R_F5_P2, Global_R_F5_P3, Global_R_F5_P4, Global_R_F5_P5,
        Global_R_F5_P6, Global_R_F5_P7, Global_R_F5_Backoff]

R_F6 = [Global_R_F6_centre_j, Global_R_F6_centre, Global_R_F6_P1, Global_R_F6_P2, Global_R_F6_P3, Global_R_F6_P4,
        Global_R_F6_P5, Global_R_F6_Backoff, 6]

R_F7 = [Global_R_F7_centre_j, 1, Global_R_F7_P1, Global_R_F7_P2, Global_R_F7_P3, Global_R_F7_P4, Global_R_F7_P5,
        Global_R_F7_P6, Global_R_F7_P7, Global_R_F7_Backoff]

R_F8 = [Global_R_F8_centre_j, 1, Global_R_F8_P1, Global_R_F8_P2, Global_R_F8_P3, Global_R_F8_P4, Global_R_F8_P5,
        Global_R_F8_P6, Global_R_F8_Backoff]
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
        if data:
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

# pick function to pick both L & R Parts
def pick(pos):
    # pallet_map = "100000001000000000"
    # receives string of position from camera
    tp_log("poaition: " +str(pos))
    tp_log("SIDE is " + str(SIDE))
    pallet_place = int(pos)    
    side_l = None
    side_j = None
    delta_x = None
    delta_y = None
    ref_c = None

    if (SIDE == "R" and pallet_place == 0):
        tp_log("Executing first condition")
        movej(Global_pick_R_0_above_j, vel=jmove_vel, acc=pick_acc)
        set_digital_output(AIRBLOW_OUTPUT, 1)
        if get_digital_input(9) == 1:
            movej(Global_pick_R_0_j, vel=convergence_j_vel, acc=convergence_acc)
        else:
            set_digital_output(AIRBLOW_OUTPUT, 1)
            movej(Global_pick_R_0_j, vel=convergence_j_vel, acc=convergence_acc)
        wait(2)
        set_digital_output(AIRBLOW_OUTPUT, 0)
        if get_digital_input(10) == 1:
            movej(Global_pick_R_0_above_j, vel=convergence_j_vel, acc=convergence_acc)
            movej(Global_BR_HOME, vel=jmove_vel, acc=pick_acc)
        else:
            set_digital_output(AIRBLOW_OUTPUT, 0)
            wait(0.5)
            movej(Global_pick_R_0_above_j, vel=convergence_j_vel, acc=convergence_acc)
            movej(Global_BR_HOME, vel=jmove_vel, acc=pick_acc)
    
    elif (SIDE == "R" and pallet_place == 1):
        tp_log("Executing second condition")
        movej(Global_pick_R_1_above_j, vel=jmove_vel, acc=pick_acc)
        set_digital_output(AIRBLOW_OUTPUT, 1)
        if get_digital_input(9) == 1:
            movej(Global_pick_R_1_j, vel=convergence_j_vel, acc=convergence_acc)
        else:
            set_digital_output(AIRBLOW_OUTPUT, 1)
            movej(Global_pick_R_1_j, vel=convergence_j_vel, acc=convergence_acc)
        wait(2)
        set_digital_output(AIRBLOW_OUTPUT, 0)
        if get_digital_input(10) == 1:
            movej(Global_pick_R_1_above_j, vel=convergence_j_vel, acc=convergence_acc)
            movej(Global_BR_HOME, vel=jmove_vel, acc=pick_acc)
        else:
            set_digital_output(AIRBLOW_OUTPUT, 0)
            wait(0.5)
            movej(Global_pick_R_1_above_j, vel=convergence_j_vel, acc=convergence_acc)
            movej(Global_BR_HOME, vel=jmove_vel, acc=pick_acc)
    
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
        movej(side_j, vel=jmove_vel, acc=pick_acc)
        movel(pick_pos_above, vel=lmove_vel, acc=pick_acc)
        set_digital_output(AIRBLOW_OUTPUT, 1)
        if get_digital_input(9) == 1:
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
        wait(2)
        release_force()
        release_compliance_ctrl()
        set_digital_output(AIRBLOW_OUTPUT, 0)
        if get_digital_input(10) == 1:
            movel(pick_pos_above, vel=convergence_vel, acc=pick_acc)
            movej(Global_BR_HOME, vel=jmove_vel, acc=pick_acc)
        else:
            set_digital_output(AIRBLOW_OUTPUT, 0)
            movel(pick_pos_above, vel=convergence_vel, acc=pick_acc)
            movej(Global_BR_HOME, vel=jmove_vel, acc=pick_acc)
        set_ref_coord(DR_BASE)


# Deburr L function
def deburr_L(*Faces, ref_c):
    global NEW_COORDINATE_SYS_FLAG
    global NEW_COORDINATE_SYS
    new_centre_position = None
    delta = None
    delta_x = None
    delta_y = None
    delta_z = None
    #set_digital_output(RIGHT_MOTOR, 1)
    #set_digital_output(LEFT_MOTOR, 0)
    for m in Faces:
        Face_points = []
        L_Face = []
        L_Face = m
        L_F_j_position = L_Face[0]
        L_F_centre_position = L_Face[1]
        amovej(L_F_j_position, vel=jmove_vel, acc=safe_acc)
        mwait(0)
        if not NEW_COORDINATE_SYS_FLAG:  
            set_ref_coord(ref_c)          
            movel(L_F_centre_position, vel=lmove_vel, acc=safe_acc)
            k_d1 = [1500.0, 1500.0, 1500.0, 1000.0, 1000.0, 1000.0]
            task_compliance_ctrl(k_d1)
            force_desired = 1
            f_d = [0.0, 0.0, -force_desired, 0.0, 0.0, 0.0]
            f_dir = [0, 0, 1, 0, 0, 0]
            set_desired_force(f_d, f_dir)
            while (1):
                #wait(3)
                force_condition = check_force_condition(DR_AXIS_Z, max=force_desired)
                if force_condition == 1:
                    break
            release_compliance_ctrl()
            new_centre_position = get_current_posx()
            new_centre_position = new_centre_position[0]
            tp_log("ref coord position: " + str(new_centre_position))
            NEW_COORDINATE_SYS_FLAG = 1    
            delta = subtract_pose(new_centre_position, L_F_centre_position)
            tp_log("delta: " + str(delta))
        delta_x = delta[0]
        delta_y = delta[1]
        delta_z = delta[2]-5
        if L_Face[len(L_Face) - 1] == 1:
            movej(Global_L_F1_Intermediate, vel=intermediate_jmove_vel, acc=intermediate_acc)
            L_Face.pop()
        elif L_Face[len(L_Face) - 1] == 2:
            movej(Global_L_F2_Intermediate, vel=intermediate_jmove_vel, acc=intermediate_acc)
            L_Face.pop()
        elif L_Face[len(L_Face) - 1] == 6:
            movej(Global_L_F6_Intermediate, vel=intermediate_jmove_vel, acc=intermediate_acc)
            movej(Global_L_F6_2_Intermediate, vel=intermediate_jmove_vel, acc=intermediate_acc)
            L_Face.pop()
        elif L_Face[len(L_Face) - 1] == 7:
            movej(Global_L_F7_Intermediate, vel=intermediate_jmove_vel, acc=intermediate_acc)
            L_Face.pop()
        elif L_Face[len(L_Face) - 1] == 82:
            movej(Global_L_F8_2_Intermediate, vel=intermediate_jmove_vel, acc=intermediate_acc)
            L_Face.pop()
        elif L_Face[len(L_Face) - 1] == 72:
            movej(Global_L_F7_2_Intermediate, vel=intermediate_jmove_vel, acc=intermediate_acc)
            L_Face.pop()
        elif L_Face[len(L_Face) - 1] == 8:
            movej(Global_L_F8_Intermediate, vel=intermediate_jmove_vel, acc=intermediate_acc)
            L_Face.pop()
        for i in range(2, len(L_Face) - 2):
            L_Face_point = trans(L_Face[i],[delta_x, delta_y, delta_z, 0, 0, 0], ref_c, ref_c)
            Face_points.append(L_Face_point)
        backoff_pos = trans(L_Face[len(L_Face) - 1], [delta_x, delta_y, delta_z, 0, 0, 0], ref_c, ref_c)
        set_ref_coord(ref_c)
        movesx(Face_points, vel=deburr_vel, acc=deburr_acc, ref=ref_c)
        amovel(backoff_pos, vel=lmove_vel, acc=safe_acc, ref=ref_c)
        mwait(0)
        wait(0.5)
        release_force  
    NEW_COORDINATE_SYS_FLAG = 0
    set_ref_coord(DR_BASE)


# Deburr R function
def deburr_R(*Faces, ref_c):
    global NEW_COORDINATE_SYS_FLAG
    global NEW_COORDINATE_SYS
    new_centre_position = None
    delta = None
    delta_x = None
    delta_y = None
    delta_z = None
    #set_digital_output(RIGHT_MOTOR, 1)
    #set_digital_output(LEFT_MOTOR, 0)
    for m in Faces:
        Face_points = []
        R_Face = []
        R_Face = m
        R_F_j_position = R_Face[0]
        R_F_centre_position = R_Face[1]
        amovej(R_F_j_position, vel=jmove_vel, acc=safe_acc)
        mwait(0)        
        if not NEW_COORDINATE_SYS_FLAG:  
            set_ref_coord(ref_c)          
            movel(R_F_centre_position, vel=lmove_vel, acc=safe_acc)
            k_d1 = [1500.0, 1500.0, 1500.0, 1000.0, 1000.0, 1000.0]
            task_compliance_ctrl(k_d1)
            force_desired = 1
            f_d = [0.0, 0.0, -force_desired, 0.0, 0.0, 0.0]
            f_dir = [0, 0, 1, 0, 0, 0]
            set_desired_force(f_d, f_dir)
            while (1):
                #wait(3)
                force_condition = check_force_condition(DR_AXIS_Z, max=force_desired)
                if force_condition == 1:
                    break
            release_compliance_ctrl()
            new_centre_position = get_current_posx()
            new_centre_position = new_centre_position[0]
            tp_log("ref coord position: " + str(new_centre_position))
            NEW_COORDINATE_SYS_FLAG = 1    
            delta = subtract_pose(new_centre_position, R_F_centre_position)
            tp_log("delta: " + str(delta))
        delta_x = delta[0]
        delta_y = delta[1]
        delta_z = delta[2]-3
        if R_Face[len(R_Face) - 1] == 1:
            movej(Global_R_F1_Intermediate, vel=intermediate_jmove_vel, acc=intermediate_acc)
            R_Face.pop()
        elif R_Face[len(R_Face) - 1] == 2:
            movej(Global_R_F2_Intermediate, vel=intermediate_jmove_vel, acc=intermediate_acc)
            R_Face.pop()
        elif R_Face[len(R_Face) - 1] == 6:
            movej(Global_R_F6_Intermediate, vel=intermediate_jmove_vel, acc=intermediate_acc)
            R_Face.pop()
        elif R_Face[len(R_Face) - 1] == 22:
            movej(Global_R_F2_2_Intermediate, vel=intermediate_jmove_vel, acc=intermediate_acc)
            R_Face.pop()
        for i in range(2, len(R_Face) - 2):
            R_Face_point = trans(R_Face[i],[delta_x, delta_y, delta_z, 0, 0, 0], ref_c, ref_c)
            Face_points.append(R_Face_point)
        tp_log ("Face Points:" +str(Face_points))
        backoff_pos = trans(R_Face[len(R_Face) - 1], [delta_x, delta_y, delta_z, 0, 0, 0], ref_c, ref_c)
        tp_log("Backoff pos: " +str(backoff_pos))
        set_ref_coord(ref_c)
        movesx(Face_points, vel=deburr_vel, acc=deburr_acc, ref=ref_c)
        amovel(backoff_pos, vel=lmove_vel, acc=safe_acc, ref=ref_c)
        mwait(0)
        wait(0.5)
        release_force  
    NEW_COORDINATE_SYS_FLAG = 0
    set_ref_coord(DR_BASE)


def handover():
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
            #set_digital_output(7, 0)
            break
    movel(Global_handover_l, vel=lmove_vel, acc=safe_acc)
    movej(Global_BR_HOME, vel=jmove_vel, acc=safe_acc)

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