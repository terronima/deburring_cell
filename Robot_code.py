import socket
import sys
import threading

# constants
DEBURR_L_USR_CORD_ID = 106
BR_L_PALLET_USR_CORD = 107
BR_R_PALLET_USR_CORD = 108
L_F1_USR_CORD = 105
AIRBLOW_OUTPUT = 7
GREEN = 10
RED = 11
YELLOW = 12
GREET = 0
RIGHT_MOTOR = 13
LEFT_MOTOR = 14
# Global variables
Global_standby = posj(-141.6, -0.31, 142.12, 2.05, 37.75, -141.84)

# Global_Pick_L_j = posj(-138.03, 48.20, 91.53, 0.59, 38.24, -137.18)

# Velocity and Acceleration
deburr_vel = 200
jmove_vel = 80
intermediate_jmove_vel = 80
lmove_vel = 500
convergence_vel = 300
safe_acc = 400
deburr_acc = 250
set_tool("right part")
SIDE = ""
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

R_F2 = [Global_R_F2_centre_j, Global_R_F2_P1, Global_R_F2_P2, Global_R_F2_P3, Global_R_F2_P4, Global_R_F2_P5,
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

def send(msg):
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
            send(data)
            break    

# pick function to pick both L & R Parts
def pick(pos):
    # pallet_map = "100000001000000000"
    # receives string of position from camera
    tp_log(str(pos))
    pallet_place = int(pos)    
    side_l = None
    side_j = None
    delta_x = None
    delta_y = None
    ref_c = None
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
        delta_y = -140 * (pallet_place % 3)
    tp_log("SIDE is " + str(SIDE))
    tp_log("delta_x  = " + str(delta_x))
    tp_log("delta_y   = " + str(delta_y ))
    delta_val_above = trans(side_l, [delta_x, delta_y, 100, 0, 0, 0])
    delta_val = trans(side_l, [delta_x, delta_y, 0, 0, 0, 0])
    pick_pos_above = coord_transform(delta_val_above, ref_c, DR_BASE)
    pick_pos = coord_transform(delta_val, ref_c, DR_BASE)
    movej(side_j, vel=jmove_vel, acc=safe_acc)
    movel(pick_pos_above, vel=lmove_vel, acc=safe_acc)
    set_digital_output(AIRBLOW_OUTPUT, 1)
    if get_digital_input(9) == 1:
        movel(pick_pos, vel=convergence_vel, acc=safe_acc)
    else:
        set_digital_output(AIRBLOW_OUTPUT, 1)
        movel(pick_pos, vel=convergence_vel, acc=safe_acc)
    k_d = [500.0, 500.0, 500.0, 200.0, 200.0, 200.0]
    task_compliance_ctrl(k_d)
    force_desired = 10.0
    f_d = [0.0, 0.0, -force_desired, 0.0, 0.0, 0.0]
    f_dir = [0, 0, 1, 0, 0, 0]
    set_desired_force(f_d, f_dir)
    force_check = 10.0
    while (1):
        force_condition = check_force_condition(DR_AXIS_Z, max=force_check)
        if force_condition == 1:
            break
    wait(1)
    release_force()
    release_compliance_ctrl()
    set_digital_output(AIRBLOW_OUTPUT, 0)
    if get_digital_input(10) == 1:
        movel(pick_pos_above, vel=convergence_vel, acc=safe_acc)
        movej(Global_BR_HOME, vel=jmove_vel, acc=safe_acc)
    else:
        set_digital_output(AIRBLOW_OUTPUT, 0)
        movel(pick_pos_above, vel=convergence_vel, acc=safe_acc)
        movej(Global_BR_HOME, vel=jmove_vel, acc=safe_acc)
    set_ref_coord(DR_BASE)


# Deburr L function
def deburr_L(*Faces, ref_c):
    global NEW_COORDINATE_SYS_FLAG
    global NEW_COORDINATE_SYS
    set_digital_output(RIGHT_MOTOR, 0)
    set_digital_output(LEFT_MOTOR, 1)
    for m in Faces:
        Face_points = []
        L_Face = []
        L_Face = m
        L_F_j_position = L_Face[0]
        L_F_centre_position = L_Face[1]
        movej(L_F_j_position, vel=jmove_vel, acc=safe_acc)
        if not NEW_COORDINATE_SYS_FLAG:
            # movej(Global_L_safe)
            movel(L_F_centre_position, vel=lmove_vel, acc=safe_acc)
            set_ref_coord(L_F1_USR_CORD)
            k_d1 = [1500.0, 1500.0, 1500.0, 1000.0, 1000.0, 1000.0]
            task_compliance_ctrl(k_d1)
            force_desired = 1
            f_d = [0.0, 0.0, -force_desired, 0.0, 0.0, 0.0]
            f_dir = [0, 0, 1, 0, 0, 0]
            set_desired_force(f_d, f_dir)
            while (1):
                force_condition = check_force_condition(DR_AXIS_Z, max=force_desired)
                if force_condition == 1:
                    break
            release_compliance_ctrl()
            new_centre_position = get_current_posx()
            new_centre_position = new_centre_position[0]
            new_centre_position = trans(new_centre_position, [0, 0, -5, 0, 0, 0], L_F1_USR_CORD)
            NEW_COORDINATE_SYS = set_user_cart_coord(new_centre_position, ref=DR_BASE)
            NEW_COORDINATE_SYS_FLAG = 1
            tp_log(str(NEW_COORDINATE_SYS))
        set_ref_coord(NEW_COORDINATE_SYS)
        if L_Face[len(L_Face) - 1] == 1:
            movej(Global_L_F1_Intermediate, vel=intermediate_jmove_vel, acc=safe_acc)
            L_Face.pop()
        elif L_Face[len(L_Face) - 1] == 2:
            movej(Global_L_F2_Intermediate, vel=intermediate_jmove_vel, acc=safe_acc)
            L_Face.pop()
        elif L_Face[len(L_Face) - 1] == 6:
            movej(Global_L_F6_Intermediate, vel=intermediate_jmove_vel, acc=safe_acc)
            movej(Global_L_F6_2_Intermediate, vel=intermediate_jmove_vel, acc=safe_acc)
            L_Face.pop()
        elif L_Face[len(L_Face) - 1] == 7:
            movej(Global_L_F7_Intermediate, vel=intermediate_jmove_vel, acc=safe_acc)
            L_Face.pop()
        elif L_Face[len(L_Face) - 1] == 82:
            movej(Global_L_F8_2_Intermediate, vel=intermediate_jmove_vel, acc=safe_acc)
            L_Face.pop()
        elif L_Face[len(L_Face) - 1] == 72:
            movej(Global_L_F7_2_Intermediate, vel=intermediate_jmove_vel, acc=safe_acc)
            L_Face.pop()
        elif L_Face[len(L_Face) - 1] == 8:
            movej(Global_L_F8_Intermediate, vel=intermediate_jmove_vel, acc=safe_acc)
            L_Face.pop()
        for i in range(2, len(L_Face) - 2):
            L_Face_point = coord_transform(L_Face[i], DR_BASE, NEW_COORDINATE_SYS)
            Face_points.append(L_Face_point)
        movesx(Face_points, vel=deburr_vel, acc=deburr_acc)
        backoff_pos = coord_transform(L_Face[len(L_Face) - 1], DR_BASE, NEW_COORDINATE_SYS)
        movel(backoff_pos, vel=lmove_vel, acc=safe_acc, ref=NEW_COORDINATE_SYS)
        wait(0.5)
        release_force
    set_ref_coord(DR_BASE)
    NEW_COORDINATE_SYS_FLAG = 0


# Deburr R function
def deburr_R(*Faces, ref_c):
    global NEW_COORDINATE_SYS_FLAG
    global NEW_COORDINATE_SYS
    set_digital_output(RIGHT_MOTOR, 1)
    set_digital_output(LEFT_MOTOR, 0)
    for m in Faces:
        Face_points = []
        R_Face = []
        R_Face = m
        R_F_j_position = R_Face[0]
        R_F_centre_position = R_Face[1]
        movej(R_F_j_position, vel=jmove_vel, acc=safe_acc)
        if not NEW_COORDINATE_SYS_FLAG:
            # movej(Global_L_safe)
            movel(R_F_centre_position, vel=lmove_vel, acc=safe_acc)
            set_ref_coord(L_F1_USR_CORD)
            k_d1 = [1500.0, 1500.0, 1500.0, 1000.0, 1000.0, 1000.0]
            task_compliance_ctrl(k_d1)
            force_desired = 1
            f_d = [0.0, 0.0, -force_desired, 0.0, 0.0, 0.0]
            f_dir = [0, 0, 1, 0, 0, 0]
            set_desired_force(f_d, f_dir)
            while (1):
                force_condition = check_force_condition(DR_AXIS_Z, max=force_desired)
                if force_condition == 1:
                    break
            release_compliance_ctrl()
            new_centre_position = get_current_posx()
            new_centre_position = new_centre_position[0]
            new_centre_position = trans(new_centre_position, [0, 0, -5, 0, 0, 0], L_F1_USR_CORD)
            NEW_COORDINATE_SYS = set_user_cart_coord(new_centre_position, ref=DR_BASE)
            NEW_COORDINATE_SYS_FLAG = 1
            tp_log(str(NEW_COORDINATE_SYS))
        set_ref_coord(NEW_COORDINATE_SYS)
        if R_Face[len(R_Face) - 1] == 1:
            movej(Global_R_F1_Intermediate, vel=intermediate_jmove_vel, acc=safe_acc)
            R_Face.pop()
        elif R_Face[len(R_Face) - 1] == 2:
            movej(Global_R_F2_Intermediate, vel=intermediate_jmove_vel, acc=safe_acc)
            R_Face.pop()
        elif R_Face[len(R_Face) - 1] == 6:
            movej(Global_R_F6_Intermediate, vel=intermediate_jmove_vel, acc=safe_acc)
            R_Face.pop()
        elif R_Face[len(R_Face) - 1] == 22:
            movej(Global_R_F2_2_Intermediate, vel=intermediate_jmove_vel, acc=safe_acc)
            R_Face.pop()
        for i in range(2, len(R_Face) - 2):
            R_Face_point = coord_transform(R_Face[i], DR_BASE, NEW_COORDINATE_SYS)
            Face_points.append(R_Face_point)
        movesx(Face_points, vel=deburr_vel, acc=deburr_acc)
        backoff_pos = coord_transform(R_Face[len(R_Face) - 1], DR_BASE, NEW_COORDINATE_SYS)
        movel(backoff_pos, vel=lmove_vel, acc=safe_acc, ref=NEW_COORDINATE_SYS)
        wait(0.5)
        release_force
    set_ref_coord(DR_BASE)
    NEW_COORDINATE_SYS_FLAG = 0


def handover():
    movej(Global_BR_HOME, vel=jmove_vel, acc=safe_acc)
    movej(Global_handover_L_j, vel=jmove_vel, acc=safe_acc)
    data = send("r1,r2,ready")
    if data == "ready":
        wait(0.5)
        set_digital_output(6, 1)
    data = send("r1,r2,part_released")
    if data == "secured":
        send("r1,r2,done")
        set_digital_output(6, 0)
        wait(1)
    movej(Global_BR_HOME, vel=jmove_vel, acc=safe_acc)

def left_only_MODE(pallet_map):
    global SIDE
    SIDE = "L"
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
            pallet_place = cntr - 9
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
        if cntr >= 8:
            for i in range(int(len(pallet_map[9::])), int(len(pallet_map))):
                if pallet_map[i] == 1:
                    SIDE = "L"
                    pallet_place = cntr - 9
                    return pallet_place
                cntr += 1
                
                
    -----------------MAIN-------------------

pallet_place = None
camera_map = 0
pallet_map = []
GREET = 0
cntr = 0
# greet the server and establish connection
tp_log("Now greeting...")
if GREET == 0:
    tp_log("Greet complete!")
    greet()
    GREET = 1

while True:
    tp_log("Entering big loop...")
    #PAUSE = int(send("r1,HMI,is_r1_paused"))
    PAUSE = 0
    if PAUSE:
        time.sleep(1)
    else:
        # request camera map
        camera_map = send("r1,cam,r1_send_cam_data")
        tp_log("Original_camera_map before" + str(camera_map))
        camera_map = camera_map.strip("z")
        tp_log("Original_camera_map " + str(camera_map))

        # modify Right pallet data in camera map   
        pallet_map = []
        tp_log("cleared pallet map: " + str(pallet_map))
        R_pallet_map = camera_map[0:9]
        New_R_pallet_map = ""
        j = 2
        for i in range(0, int(len(R_pallet_map))):
            New_R_pallet_map += str(R_pallet_map[j])
            j -= 1
            if j == -1:
                j = 5
            elif j == 2:
                j = 8
        pallet_map_str = New_R_pallet_map + camera_map[9::]
        for i in pallet_map_str:
            pallet_map.append(int(i))
        tp_log("updated_pallet_map " + str(pallet_map))
        PICK_MODE = send("r1,HMI,PICK_MODE")   
        PICK_MODE = PICK_MODE.strip("z") 
        tp_log("Pick mode:" + PICK_MODE) 
        while True:       
            pick_pos = None
            if PICK_MODE == "left_only":
                pick_pos = left_only_MODE(pallet_map)

            elif PICK_MODE == "right_only":
                pick_pos = right_only_MODE(pallet_map)

            elif PICK_MODE == "intermittent":
                pick_pos = intermittent_MODE(pallet_map)

            elif PICK_MODE == "side_by_side":
                pick_pos = side_by_side_MODE(pallet_map)
            tp_log("Pallet pick pos " + str(pick_pos))

            pick(pick_pos)

            #if SIDE == "L":
                # deburr_L(L_F1, L_F2, L_F3, L_F5, L_F7, L_F8_2, ref_c = DR_BASE)
                # deburr_L(L_F6, L_F4, L_F7_2, L_F8, ref_c = DR_BASE)
            #elif SIDE == "R":
                # deburr_R(R_F1, R_F2, R_F3, R_F5, R_F7, ref_c = DR_BASE)
                # deburr_R(R_F6, R_F4, R_F8, ref_c = DR_BASE)

            #handover()
            if SIDE == "R":
                cntr = pick_pos
            elif SIDE == "L":
                cntr = pick_pos + 10
            pallet_map[cntr] = 0
            tp_log("cntr is: " + str(cntr))    
            tp_log(str(pallet_map))
            if sum(pallet_map) == 0:
                tp_log("camera map is empty")
                set_digital_output(RIGHT_MOTOR, 0)
                set_digital_output(LEFT_MOTOR, 0)
                break
    tp_log("small loop breaked")

