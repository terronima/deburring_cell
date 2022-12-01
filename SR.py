import socket
import sys
import threading

# constants
SR_L_PALLET_COORD = 105
SR_R_PALLET_COORD = 102
R_COORD_SYS = 106
L_COORD_SYS = 103
AIRBLOW_OUTPUT = 6
DEBURR_MOTOR =  8
WATER_LEVEL_SENSOR = 7
AIR_BLADE = 2

# STATE
START = 1
STOP = 0
LOW = 0
HIGH = 1

# Velocity and Acceleration
deburr_vel = [800, 80]
jmove_vel = 80
intermediate_jmove_vel = 80
lmove_vel = 500
convergence_vel = 100
convergence_acc = 200
safe_acc = 400
deburr_acc = [550, 400]
set_tool("R_Part")
SIDE = ""
camera_map = ""

# List of point for L Part faces
L_F0 = [Global_L_F0_centre_j, Global_L_F0_centre, Global_L_F0_Backoff, 0]

L_F1 = [Global_L_F1_centre_j, 1, Global_L_F1_P1, Global_L_F1_P2, Global_L_F1_P3, Global_L_F1_P4, Global_L_F1_P5, Global_L_F1_P6, Global_L_F1_P7, Global_L_F1_P8, Global_L_F1_P9, Global_L_F1_P10, Global_L_F1_P11, Global_L_F1_P12, Global_L_F1_P13, Global_L_F1_Backoff, 1]

L_F2 = [Global_L_F2_centre_j, 1, Global_L_F2_P1, Global_L_F2_P2, Global_L_F2_P3, Global_L_F2_Backoff, 9]

L_F3 = [Global_L_F3_centre_j, 1, Global_L_F3_P1, Global_L_F3_P2, Global_L_F3_Backoff, 9]

L_F4 = [Global_L_F4_centre_j, 1, Global_L_F4_P1, Global_L_F4_P1, Global_L_F4_Backoff, 9]

L_F5 = [Global_L_F5_centre_j, 1, Global_L_F5_P1, Global_L_F5_P1, Global_L_F5_Backoff, 9]

L_F6 = [Global_L_F6_centre_j, 1, Global_L_F6_P1, Global_L_F6_P2, Global_L_F6_Backoff, 9]


# List of point for R Part faces
R_F0 = [Global_R_F0_centre_j, Global_R_F0_centre, Global_R_F0_Backoff, 0]

R_F1 = [Global_R_F1_centre_j, 1, Global_R_F1_P1, Global_R_F1_P2, Global_R_F1_P3, Global_R_F1_P4, Global_R_F1_P5, Global_R_F1_P6, Global_R_F1_P7, Global_R_F1_P8, Global_R_F1_P9, Global_R_F1_P10, Global_R_F1_P11, Global_R_F1_P12, Global_R_F1_P13, Global_R_F1_Backoff, 1]

R_F2 = [Global_R_F2_centre_j, 1, Global_R_F2_P1, Global_R_F2_P2, Global_R_F2_P4, Global_R_F2_Backoff, 9]
        
R_F3 = [Global_R_F3_centre_j, 1, Global_R_F3_P1, Global_R_F3_P2, Global_R_F3_P3, Global_R_F3_Backoff, 9]

R_F4 = [Global_R_F4_centre_j, 1, Global_R_F4_P1, Global_R_F4_P1, Global_R_F4_Backoff, 9]

R_F5 = [Global_R_F5_centre_j, 1, Global_R_F5_P1, Global_R_F5_P1, Global_R_F5_Backoff, 9]

R_F6 = [Global_R_F6_centre_j, 1, Global_R_F6_P1, Global_R_F6_P2, Global_R_F6_Backoff, 9]

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

def greet():
    global SIDE
    global client
    received = ""
    while True:
        try:
            received = client.recv(HEADER).decode(FORMAT)
        except:
            print("Failed")
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(ADDR)
        if received:
                data = "r2"
                send(data, 1)
                break

# Deburr L function
def deburr_L(*Faces, ref_c):
    global NEW_COORDINATE_SYS_FLAG
    global NEW_COORDINATE_SYS
    new_centre_position = None
    delta = None
    delta_x = None
    delta_y = None
    delta_z = None
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
            force_desired = 5
            f_d = [0.0, 0.0, force_desired, 0.0, 0.0, 0.0]
            f_dir = [0, 0, 1, 0, 0, 0]
            set_desired_force(f_d, f_dir)
            while True:
                tp_log("Inside while...")
                force_condition = check_force_condition(DR_AXIS_Z, max=force_desired, ref=DR_TOOL)
                if force_condition != 1:
                    break
            release_compliance_ctrl()
            new_centre_position = get_current_posx()
            new_centre_position = new_centre_position[0]
            tp_log("ref coord position: " + str(new_centre_position))
            NEW_COORDINATE_SYS_FLAG = 1    
            delta = subtract_pose(new_centre_position, L_F_centre_position)
            tp_log("delta: " + str(delta))
        delta_x = delta[0]-1
        delta_y = delta[1]
        delta_z = delta[2]-7
        set_ref_coord(ref_c)
        
        if L_Face[len(L_Face) - 1] == 0:
            L_Face.pop()

        elif L_Face[len(L_Face) - 1] == 1:
            L_Face_point = trans(L_Face[2],[0, 0, delta_z, 0, 0, 0], ref_c, ref_c)
            movel(L_Face_point, vel=deburr_vel, acc=deburr_acc, ref=ref_c)
            for i in range(3, len(L_Face) - 2):
                L_Face_point = trans(L_Face[i],[0, 0, delta_z, 0, 0, 0], ref_c, ref_c)
                Face_points.append(L_Face_point)
            L_Face.pop()
            movesx(Face_points, vel=deburr_vel, acc=deburr_acc, ref=ref_c)
        else:
            for i in range(2, len(L_Face) - 2):
                L_Face_point = trans(L_Face[i],[0, 0, delta_z, 0, 0, 0], ref_c, ref_c)
                movel(L_Face_point, vel=deburr_vel, acc=deburr_acc, ref=ref_c)
            L_Face.pop()
        backoff_pos = trans(L_Face[len(L_Face) - 1], [0, 0, delta_z, 0, 0, 0], ref_c, ref_c)
        movel(backoff_pos, vel=lmove_vel, acc=safe_acc, ref=ref_c)
        #mwait(0)
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
            force_desired = 5
            f_d = [0.0, 0.0, force_desired, 0.0, 0.0, 0.0]
            f_dir = [0, 0, 1, 0, 0, 0]
            set_desired_force(f_d, f_dir)
            while True:
                tp_log("Inside while...")
                force_condition = check_force_condition(DR_AXIS_Z, max=force_desired, ref=DR_TOOL)
                if force_condition != 1:
                    break
            release_compliance_ctrl()
            new_centre_position = get_current_posx()
            new_centre_position = new_centre_position[0]
            tp_log("ref coord position: " + str(new_centre_position))
            NEW_COORDINATE_SYS_FLAG = 1    
            delta = subtract_pose(new_centre_position, R_F_centre_position)
            tp_log("delta: " + str(delta))
        delta_x = delta[0]-1
        delta_y = delta[1]
        delta_z = delta[2]-7
        set_ref_coord(ref_c)
        if R_Face[len(R_Face) - 1] == 0:
            R_Face.pop()

        elif R_Face[len(R_Face) - 1] == 1:
            R_Face_point = trans(R_Face[2],[0, 0, delta_z, 0, 0, 0], ref_c, ref_c)
            movel(R_Face_point, vel=deburr_vel, acc=deburr_acc, ref=ref_c)
            for i in range(3, len(R_Face) - 2):
                R_Face_point = trans(R_Face[i],[0, 0, delta_z, 0, 0, 0], ref_c, ref_c)
                Face_points.append(R_Face_point)
            R_Face.pop()
            movesx(Face_points, vel=deburr_vel, acc=deburr_acc, ref=ref_c)
        else:
            for i in range(2, len(R_Face) - 2):
                R_Face_point = trans(R_Face[i],[0, 0, delta_z, 0, 0, 0], ref_c, ref_c)
                movel(R_Face_point, vel=deburr_vel, acc=deburr_acc, ref=ref_c)
            R_Face.pop()
        backoff_pos = trans(R_Face[len(R_Face) - 1], [0, 0, delta_z, 0, 0, 0], ref_c, ref_c)
        movel(backoff_pos, vel=lmove_vel, acc=safe_acc, ref=ref_c)
        #mwait(0)
        wait(0.5)
        release_force
    NEW_COORDINATE_SYS_FLAG = 0
    set_ref_coord(DR_BASE)

def dip_part():
    if (get_digital_input(WATER_LEVEL_SENSOR) == LOW):
        send("r2,HMI,r2_faulted", 0)
    else:
        Global_above_basin_l = trans(Global_basin_l, [0, 0, 300, 0, 0, 0], ref=DR_BASE)
        set_velx(deburr_vel)
        set_accx(safe_acc)
        movej(Global_above_basin_j)
        movel(Global_above_basin_l)
        movel(Global_basin_l)
        wait(1)
        set_digital_output(AIR_BLADE, 1)
        movel(Global_above_basin_l)
        set_digital_output(AIR_BLADE, 0)
        movej(Global_above_basin_j)
        movej(Global_standby)

def place():
    global SIDE
    pallet_map = None
    place_speed = 25
    stiffness = [500, 500, 500, 1000, 1000, 1000]
    force_desired = 50.0  # set desired force
    f_d = [0.0, 0.0, -force_desired, 0.0, 0.0, 0.0]  # set force direction
    f_dir = [0, 0, 1, 0, 0, 0]  # set axis at which force would be applied (x, y, z, a, b, c)
    while True:
        pallet_map = send("r2,cam,r2_send_cam_data", 1)
        if (len(pallet_map)) == 18:
            break
        time.sleep(0.5)
    set_velx(225, 225)
    set_accx(300, 300)
    tp_log(str(pallet_map))
    cntr = 0
    pallet_place = None
    side_l = 0
    side_j = 0
    ref_c = 0
    if SIDE == "L":
        ref_c = SR_L_PALLET_COORD
        side_l = Global_place_L_l
        side_j = Global_place_L_j
    elif SIDE == "R":
        ref_c = SR_R_PALLET_COORD
        side_l = Global_place_R_l
        side_j = Global_place_R_j
    for i in pallet_map:
        if SIDE == "R" and cntr < len(pallet_map) // 2:
            p = int(i)
            tp_log("p is: " + str(p) + ", cntr is" + str(cntr))
            if p == 0:
                pallet_place = cntr 
                break
        elif SIDE == "L" and cntr >= len(pallet_map) // 2:
            p = int(i)
            if p == 0:
                pallet_place = cntr - 9
                break
        cntr += 1
    tp_log("pallet_place: " + str(pallet_place))
    y = 160 * (pallet_place // 3)
    x = -140 * (pallet_place % 3)
    place_above = trans(side_l, [x, y, 100, 0, 0, 0])
    place = trans(side_l, [x, y, 0, 0, 0, 0])
    place_above = coord_transform(place_above, ref_c, DR_BASE)
    place = coord_transform(place, ref_c, DR_BASE)
    movej(Global_SR_HOME_j)
    movej(side_j)
    movel(place_above)
    movel(place, vel=place_speed)
    task_compliance_ctrl(stiffness)
    set_desired_force(f_d, f_dir)
    wait(2)
    set_digital_output(6, 1)
    wait(1)
    release_force()
    release_compliance_ctrl()
    movel(place_above)
    tp_log(str(place_above))

def Estop_recovery():
    set_ref_coord(DR_BASE)
    current_position = get_current_posx()
    current_position = current_position[0]
    safe_position = trans(current_position, [0,-50, 300, 0, 0, 0], DR_BASE, DR_BASE)
    movel(safe_position, vel=intermediate_acc, acc=safe_acc)
    wait(0.5)
    movej(Global_estop_recovery_point, vel=50, acc=30)
    set_digital_output(AIRBLOW_OUTPUT ,1)
    #wait_nudge()
    wait(5)
    move_home(DR_HOME_TARGET_USER)
    

# get part from big robot, acknowledge transfer and side.
def receive_part():
    global SIDE
    side = ""
    in_data = ""
    handover_speed = 35
    stiffness = [500, 500, 500, 100, 100, 100]
    Handover_above = trans(Global_handover_l, [-100, 0, 0, 0, 0, 0], DR_BASE)
    force_desired = 10.0  # set desired force
    f_d = [-force_desired, 0.0, 0.0, 0.0, 0.0, 0.0]  # set force direction
    f_dir = [1, 0, 0, 0, 0, 0]  # set axis at which force would be applied (x, y, z, a, b, c)
    movej(Global_SR_HOME_j)
    movej(Global_handover_j)
    #movel(Handover_above)
    set_digital_output(6, 1)
    wait(0.5)
    while True:
        in_data = send("", 2)
        if in_data == "wake": 
            #tp_popup("in_data: "+in_data, DR_PM_MESSAGE) 
            send("r2,r1,side", 0)
            break
    while True:
        side = send("", 2)
        tp_log("received side from BR: " + str(side))
        #tp_popup("SIDE: "+SIDE, DR_PM_MESSAGE)
        if side == "L" or side == "R":            
            send("r2,r1,ready", 0)
            break
    while True:
        ready_confirm = send("", 2)
        #tp_popup("ready_confirm: "+ready_confirm, DR_PM_MESSAGE)
        if ready_confirm == "okay":
            #tp_popup("moving closer", DR_PM_MESSAGE)
            break
    set_ref_coord(DR_BASE)
    movel(Global_handover_l, vel=handover_speed)
    task_compliance_ctrl(stiffness)
    set_desired_force(f_d, f_dir)
    #while (1):
    #    force_condition = check_force_condition(DR_AXIS_X, max=force_desired)
    #    if force_condition == 1:
    #        break
    wait(3)
    set_digital_output(6, 0)
    wait(0.5)
    send("r2,r1,secured", 0)
    # break
    while True:
        part_status = send("", 2)
        #tp_popup("part_status: "+part_status, DR_PM_MESSAGE)
        if part_status == "part_released":         
            send("r2,r1,done", 0)
            break
    release_force()
    release_compliance_ctrl()
    movej(Global_handover_j)
    wait(1)
    movej(Global_SR_HOME_j)
    SIDE = side
    tp_log("global SIDE:" + str(SIDE))
