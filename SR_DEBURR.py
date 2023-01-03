import socket
import sys
import threading

# constants
SR_L_PALLET_COORD = 105
SR_R_PALLET_COORD = 102
R_COORD_SYS = 106
L_COORD_SYS = 103
AIRBLOW_OUTPUT = 6
DEBURR_MOTOR = 8
WATER_LEVEL_SENSOR = 7
AIR_BLADE = 2
PART_PRESENT_SENSOR = 6

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
intermediate_vel = 50
intermediate_acc = 50
convergence_vel = 100
convergence_acc = 200
safe_acc = 400
deburr_acc = [550, 400]
basin_vel = 50
basin_acc = 50
set_tool("R_Part")
SIDE = ""
camera_map = ""

HMI_offset = 0.0

# List of point for L Part faces
L_F0 = [Global_L_F0_centre_j, Global_L_F0_centre, Global_L_F0_Backoff, 0]

L_F1 = [Global_L_F1_P1, Global_L_F1_P2, Global_L_F1_P3, Global_L_F1_P4, Global_L_F1_P5, Global_L_F1_P6, Global_L_F1_P7,
        Global_L_F1_P8, Global_L_F1_P9, Global_L_F1_P10, Global_L_F1_P11, Global_L_F1_P12, Global_L_F1_P13]

L_F2 = [Global_L_F2_P1, Global_L_F2_P2]

L_F3 = [Global_L_F3_P1, Global_L_F3_P2]

L_F4 = [Global_L_F4_P1, Global_L_F4_P1]

L_F5 = [Global_L_F5_P1, Global_L_F5_P1]

L_F6 = [Global_L_F6_P1, Global_L_F6_P2]

# List of point for R Part faces
R_F0 = [Global_R_F0_centre_j, Global_R_F0_centre, Global_R_F0_Backoff, 0]

R_F1 = [Global_R_F1_P1, Global_R_F1_P2, Global_R_F1_P3, Global_R_F1_P4, Global_R_F1_P5, Global_R_F1_P6, Global_R_F1_P7,
        Global_R_F1_P8, Global_R_F1_P9, Global_R_F1_P10, Global_R_F1_P11, Global_R_F1_P12, Global_R_F1_P13]

R_F2 = [Global_R_F2_P1, Global_R_F2_P2]

R_F3 = [Global_R_F3_P1, Global_R_F3_P2]

R_F4 = [Global_R_F4_P1, Global_R_F4_P1]

R_F5 = [Global_R_F5_P1, Global_R_F5_P1]

R_F6 = [Global_R_F6_P1, Global_R_F6_P2]

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


def send(msg, resp_req):  # 0 - send no lsten, 1 send and lsten, 2 - no send only lsten
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
            # tp_log(str(data))
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


def get_HMI_Offset():
    global HMI_offset
    temp = 0.0
    temp_str = send("r1,HMI,br_offset", 1)
    temp_str = temp_str.strip("z")
    tp_log(temp_str)
    if 3 >= len(temp_str) > 1:
        temp = float(temp_str)
    HMI_offset = temp
    time.sleep(1)


def L_F1_deburr(ref_c, delta_x, delta_y, delta_z):
    L_F1_points = []
    for i in range(0, len(L_F1)):
        L_Face_point = trans(L_F1[i], [delta_x, 0, delta_z, 0, 0, 0], ref_c, ref_c)
        L_F1_points.append(L_Face_point)
    movej(Global_L_F1_centre_j, vel=jmove_vel, acc=safe_acc)
    movel(L_F1_points[0], vel=deburr_vel, acc=deburr_acc, ref=ref_c)
    movesx(
        [L_F1_points[1], L_F1_points[2], L_F1_points[3], L_F1_points[4], L_F1_points[5], L_F1_points[6], L_F1_points[7],
         L_F1_points[8], L_F1_points[9], L_F1_points[10], L_F1_points[11], L_F1_points[12]], vel=deburr_vel,
        acc=deburr_acc, ref=ref_c)
    movel(Global_L_F1_Backoff, vel=lmove_vel, acc=safe_acc, ref=ref_c)


def L_F2_deburr(ref_c, delta_x, delta_y, delta_z):
    L_F2_points = []
    for i in range(0, len(L_F2)):
        L_Face_point = trans(L_F2[i], [delta_x, 0, delta_z, 0, 0, 0], ref_c, ref_c)
        L_F2_points.append(L_Face_point)
    movej(Global_L_F2_centre_j, vel=jmove_vel, acc=safe_acc)
    movel(L_F2_points[0], vel=deburr_vel, acc=deburr_acc, ref=ref_c)
    movel(L_F2_points[1], vel=deburr_vel, acc=deburr_acc, ref=ref_c)
    movel(Global_L_F2_Backoff, vel=lmove_vel, acc=safe_acc, ref=ref_c)


def L_F3_deburr(ref_c, delta_x, delta_y, delta_z):
    L_F3_points = []
    for i in range(0, len(L_F3)):
        L_Face_point = trans(L_F3[i], [delta_x, 0, delta_z, 0, 0, 0], ref_c, ref_c)
        L_F3_points.append(L_Face_point)
    movej(Global_L_F3_centre_j, vel=jmove_vel, acc=safe_acc)
    movel(L_F3_points[0], vel=deburr_vel, acc=deburr_acc, ref=ref_c)
    movel(L_F3_points[1], vel=deburr_vel, acc=deburr_acc, ref=ref_c)
    movel(Global_L_F3_Backoff, vel=lmove_vel, acc=safe_acc, ref=ref_c)


def L_F4_deburr(ref_c, delta_x, delta_y, delta_z):
    L_F4_points = []
    for i in range(0, len(L_F4)):
        L_Face_point = trans(L_F4[i], [delta_x, 0, delta_z, 0, 0, 0], ref_c, ref_c)
        L_F4_points.append(L_Face_point)
    movej(Global_L_F4_centre_j, vel=jmove_vel, acc=safe_acc)
    movel(L_F4_points[0], vel=deburr_vel, acc=deburr_acc, ref=ref_c)
    movel(L_F4_points[1], vel=deburr_vel, acc=deburr_acc, ref=ref_c)
    movel(Global_L_F4_Backoff, vel=lmove_vel, acc=safe_acc, ref=ref_c)


def L_F5_deburr(ref_c, delta_x, delta_y, delta_z):
    L_F5_points = []
    for i in range(0, len(L_F5)):
        L_Face_point = trans(L_F5[i], [delta_x, 0, delta_z, 0, 0, 0], ref_c, ref_c)
        L_F5_points.append(L_Face_point)
    movej(Global_L_F5_centre_j, vel=jmove_vel, acc=safe_acc)
    movel(L_F5_points[0], vel=deburr_vel, acc=deburr_acc, ref=ref_c)
    movel(L_F5_points[1], vel=deburr_vel, acc=deburr_acc, ref=ref_c)
    movel(Global_L_F5_Backoff, vel=lmove_vel, acc=safe_acc, ref=ref_c)


def L_F6_deburr(ref_c, delta_x, delta_y, delta_z):
    L_F6_points = []
    for i in range(0, len(L_F6)):
        L_Face_point = trans(L_F6[i], [delta_x, 0, delta_z, 0, 0, 0], ref_c, ref_c)
        L_F6_points.append(L_Face_point)
    movej(Global_L_F6_centre_j, vel=jmove_vel, acc=safe_acc)
    movel(L_F6_points[0], vel=deburr_vel, acc=deburr_acc, ref=ref_c)
    movel(L_F6_points[1], vel=deburr_vel, acc=deburr_acc, ref=ref_c)
    movel(Global_L_F6_Backoff, vel=lmove_vel, acc=safe_acc, ref=ref_c)


# Deburr L function
def deburr_L(ref_c):
    global NEW_COORDINATE_SYS_FLAG
    global NEW_COORDINATE_SYS
    new_centre_position = None
    delta = None
    delta_x = None
    delta_y = None
    delta_z = None
    Face_points = []
    L_Face = []
    L_F_j_position = Global_L_F0_centre_j
    L_F_centre_position = Global_L_F0_centre
    amovej(L_F_j_position, vel=jmove_vel, acc=safe_acc)
    mwait(0)
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
    delta_x = delta[0]
    delta_y = delta[1]
    delta_z = delta[2] - 5
    set_ref_coord(ref_c)
    get_HMI_Offset()
    L_F1_deburr(ref_c, delta_x, delta_y, delta_z)
    get_HMI_Offset()
    L_F2_deburr(ref_c, delta_x, delta_y, delta_z)
    get_HMI_Offset()
    L_F3_deburr(ref_c, delta_x, delta_y, delta_z)
    get_HMI_Offset()
    L_F4_deburr(ref_c, delta_x, delta_y, delta_z)
    get_HMI_Offset()
    L_F5_deburr(ref_c, delta_x, delta_y, delta_z)
    get_HMI_Offset()
    L_F6_deburr(ref_c, delta_x, delta_y, delta_z)
    wait(0.5)
    release_force
    NEW_COORDINATE_SYS_FLAG = 0
    set_ref_coord(DR_BASE)


def R_F1_deburr(ref_c, delta_x, delta_y, delta_z):
    R_F1_points = []
    for i in range(0, len(R_F1)):
        R_Face_point = trans(R_F1[i], [delta_x, 0, delta_z, 0, 0, 0], ref_c, ref_c)
        R_F1_points.append(R_Face_point)
    movej(Global_R_F1_centre_j, vel=jmove_vel, acc=safe_acc)
    movel(R_F1_points[0], vel=deburr_vel, acc=deburr_acc, ref=ref_c)
    movesx(
        [R_F1_points[1], R_F1_points[2], R_F1_points[3], R_F1_points[4], R_F1_points[5], R_F1_points[6], R_F1_points[7],
         R_F1_points[8], R_F1_points[9], R_F1_points[10], R_F1_points[11], R_F1_points[12]], vel=deburr_vel,
        acc=deburr_acc, ref=ref_c)
    movel(Global_R_F1_Backoff, vel=lmove_vel, acc=safe_acc, ref=ref_c)


def R_F2_deburr(ref_c, delta_x, delta_y, delta_z):
    R_F2_points = []
    for i in range(0, len(R_F2)):
        R_Face_point = trans(R_F2[i], [delta_x, 0, delta_z, 0, 0, 0], ref_c, ref_c)
        R_F2_points.append(R_Face_point)
    movej(Global_R_F2_centre_j, vel=jmove_vel, acc=safe_acc)
    movel(R_F2_points[0], vel=deburr_vel, acc=deburr_acc, ref=ref_c)
    movel(R_F2_points[1], vel=deburr_vel, acc=deburr_acc, ref=ref_c)
    movel(Global_R_F2_Backoff, vel=lmove_vel, acc=safe_acc, ref=ref_c)


def R_F3_deburr(ref_c, delta_x, delta_y, delta_z):
    R_F3_points = []
    for i in range(0, len(R_F3)):
        R_Face_point = trans(R_F3[i], [delta_x, 0, delta_z, 0, 0, 0], ref_c, ref_c)
        R_F3_points.append(R_Face_point)
    movej(Global_R_F3_centre_j, vel=jmove_vel, acc=safe_acc)
    movel(R_F3_points[0], vel=deburr_vel, acc=deburr_acc, ref=ref_c)
    movel(R_F3_points[1], vel=deburr_vel, acc=deburr_acc, ref=ref_c)
    movel(Global_R_F3_Backoff, vel=lmove_vel, acc=safe_acc, ref=ref_c)


def R_F4_deburr(ref_c, delta_x, delta_y, delta_z):
    R_F4_points = []
    for i in range(0, len(R_F4)):
        R_Face_point = trans(R_F4[i], [delta_x, 0, delta_z, 0, 0, 0], ref_c, ref_c)
        R_F4_points.append(R_Face_point)
    movej(Global_R_F4_centre_j, vel=jmove_vel, acc=safe_acc)
    movel(R_F4_points[0], vel=deburr_vel, acc=deburr_acc, ref=ref_c)
    movel(R_F4_points[1], vel=deburr_vel, acc=deburr_acc, ref=ref_c)
    movel(Global_R_F4_Backoff, vel=lmove_vel, acc=safe_acc, ref=ref_c)


def R_F5_deburr(ref_c, delta_x, delta_y, delta_z):
    R_F5_points = []
    for i in range(0, len(R_F5)):
        R_Face_point = trans(R_F5[i], [delta_x, 0, delta_z, 0, 0, 0], ref_c, ref_c)
        R_F5_points.append(R_Face_point)
    movej(Global_R_F5_centre_j, vel=jmove_vel, acc=safe_acc)
    movel(R_F5_points[0], vel=deburr_vel, acc=deburr_acc, ref=ref_c)
    movel(R_F5_points[1], vel=deburr_vel, acc=deburr_acc, ref=ref_c)
    movel(Global_R_F5_Backoff, vel=lmove_vel, acc=safe_acc, ref=ref_c)


def R_F6_deburr(ref_c, delta_x, delta_y, delta_z):
    R_F6_points = []
    for i in range(0, len(R_F6)):
        R_Face_point = trans(R_F6[i], [delta_x, 0, delta_z, 0, 0, 0], ref_c, ref_c)
        R_F6_points.append(R_Face_point)
    movej(Global_R_F6_centre_j, vel=jmove_vel, acc=safe_acc)
    movel(R_F6_points[0], vel=deburr_vel, acc=deburr_acc, ref=ref_c)
    movel(R_F6_points[1], vel=deburr_vel, acc=deburr_acc, ref=ref_c)
    movel(Global_R_F6_Backoff, vel=lmove_vel, acc=safe_acc, ref=ref_c)


# Deburr R function
def deburr_R(ref_c):
    global NEW_COORDINATE_SYS_FLAG
    global NEW_COORDINATE_SYS
    new_centre_position = None
    delta = None
    delta_x = None
    delta_y = None
    delta_z = None
    Face_points = []
    R_Face = []
    R_F_j_position = Global_R_F0_centre_j
    R_F_centre_position = Global_R_F0_centre
    amovej(R_F_j_position, vel=jmove_vel, acc=safe_acc)
    mwait(0)
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
    delta_x = delta[0] + 1
    delta_y = delta[1]
    delta_z = delta[2] - 7
    set_ref_coord(ref_c)
    get_HMI_Offset()
    R_F1_deburr(ref_c, delta_x, delta_y, delta_z)
    get_HMI_Offset()
    R_F2_deburr(ref_c, delta_x, delta_y, delta_z)
    get_HMI_Offset()
    R_F3_deburr(ref_c, delta_x, delta_y, delta_z)
    get_HMI_Offset()
    R_F4_deburr(ref_c, delta_x, delta_y, delta_z)
    get_HMI_Offset()
    R_F5_deburr(ref_c, delta_x, delta_y, delta_z)
    get_HMI_Offset()
    R_F6_deburr(ref_c, delta_x, delta_y, delta_z)
    wait(0.5)
    release_force
    NEW_COORDINATE_SYS_FLAG = 0
    set_ref_coord(DR_BASE)


def dip_part():
    movej(Global_dipping_point_above_j, vel=basin_vel, acc=basin_acc)
    movej(Global_dipping_point_j, vel=basin_vel, acc=basin_acc)
    movej(Global_rinse_p1, vel=basin_vel, acc=basin_acc)
    movej(Global_rinse_p2, vel=basin_vel, acc=basin_acc)
    movej(Global_dipping_point_j, vel=basin_vel, acc=basin_acc)
    movej(Global_rinse_p3, vel=basin_vel, acc=basin_acc)
    movej(Global_rinse_p4, vel=basin_vel, acc=basin_acc)
    wait(1)
    set_digital_output(AIR_BLADE, 1)
    movej(Global_dry_p1, vel=basin_vel, acc=basin_acc)
    movej(Global_dry_p2, vel=basin_vel, acc=basin_acc)
    wait(0.5)
    set_digital_output(AIR_BLADE, 0)
    movej(Global_basin_backoff_j, vel=basin_vel, acc=basin_acc)
    movej(Global_SR_HOME_j, vel=jmove_vel, acc=convergence_acc)


def place():
    # place part logic, define variables.
    global SIDE
    pallet_map = None
    place_speed = 25
    stiffness = [500, 500, 500, 1000, 1000, 1000]
    force_desired = 10.0  # set desired force
    f_d = [0.0, 0.0, -force_desired, 0.0, 0.0, 0.0]  # set force direction
    f_dir = [0, 0, 1, 0, 0, 0]  # set axis at which force would be applied (x, y, z, a, b, c)
    while True:  # get string of positions from camera, by requesting data through server
        pallet_map = send("r2,cam,r2_send_cam_data", 1)
        if (len(pallet_map)) == 18:
            break
        time.sleep(0.5)
    set_velx(225, 225)  # set movel speed parameters
    set_accx(300, 300)  # set movel acceleration parameters
    tp_log(str(pallet_map))
    cntr = 0
    pallet_place = None
    side_l = 0  # first position coordinate on the pallet for linear move
    side_j = 0  # first position coordinate on the pallet for joint move
    ref_c = 0  # referencecoordinate system, for right or left part
    if SIDE == "L":
        ref_c = SR_L_PALLET_COORD
        side_l = Global_place_L_l
        side_j = Global_place_L_j
    elif SIDE == "R":
        ref_c = SR_R_PALLET_COORD
        side_l = Global_place_R_l
        side_j = Global_place_R_j
    for i in pallet_map:  # detecting an empty spot on the pallet, extracting its number, so robot will placepart in correct spot
        if SIDE == "R" and cntr >= len(
                pallet_map) // 2:  # if side is right, and position counter (iterates throug the string positions) greater or equal 9
            p = int(i)
            tp_log("p is: " + str(p) + ", cntr is" + str(cntr))
            if p == 0:
                pallet_place = cntr - 9  # place part on the right side of the pallet,  in defined position
                break
        elif SIDE == "L" and cntr < len(
                pallet_map) // 2:  # same as right, but for elements positions below 9 (from camera string)
            p = int(i)
            if p == 0:
                pallet_place = cntr
                break
        cntr += 1
    tp_log("pallet_place: " + str(pallet_place))
    # offset logic. basedon position, part will be offset from zero position
    y = 160 * (pallet_place // 3)  # step in x direction is 160mm
    x = -140 * (pallet_place % 3)  # step in y direction is 140mm
    place_above = trans(side_l, [x, y, 100, 0, 0, 0])  # offset z direction above the desiredposition by 100mm
    place = trans(side_l, [x, y, 0, 0, 0, 0])
    place_above = coord_transform(place_above, ref_c,
                                  DR_BASE)  # transform coordinates of chosen position into base coordinate system
    place = coord_transform(place, ref_c, DR_BASE)
    movej(Global_SR_HOME_j)
    movej(side_j)
    movel(place_above)
    movel(place, vel=place_speed)
    # enable compliance and force control
    task_compliance_ctrl(stiffness)
    set_desired_force(f_d, f_dir)
    wait(1)
    # release the part
    set_digital_output(AIRBLOW_OUTPUT, HIGH)
    wait(1)
    # disable compliance and force control
    release_force()
    release_compliance_ctrl()
    # movel above drop position
    movel(place_above)
    tp_log(str(place_above))


def Estop_recovery():
    set_digital_output(DEBURR_MOTOR, STOP)
    set_ref_coord(DR_BASE)
    current_position = get_current_posx()
    current_position = current_position[0]
    safe_position = trans(current_position, [-50, 0, 200, 0, 0, 0], DR_BASE, DR_BASE)
    movel(safe_position, vel=intermediate_vel, acc=safe_acc)
    wait(0.5)
    movej(Global_estop_recovery_point, vel=50, acc=30)
    set_digital_output(AIRBLOW_OUTPUT, HIGH)
    # wait_nudge()
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
    f_d = [force_desired, 0.0, 0.0, 0.0, 0.0, 0.0]  # set force direction
    f_dir = [1, 0, 0, 0, 0, 0]  # set axis at which force would be applied (x, y, z, a, b, c)
    movej(Global_SR_HOME_j)
    movej(Global_handover_j)
    # movel(Handover_above)
    set_digital_output(AIRBLOW_OUTPUT, HIGH)
    wait(0.5)
    while True:
        in_data = send("", 2)
        if in_data == "wake":
            # tp_popup("in_data: "+in_data, DR_PM_MESSAGE)
            send("r2,r1,side", 0)
            break
    while True:
        side = send("", 2)
        tp_log("received side from BR: " + str(side))
        # tp_popup("SIDE: "+SIDE, DR_PM_MESSAGE)
        if side == "L" or side == "R":
            send("r2,r1,ready", 0)
            break
    while True:
        ready_confirm = send("", 2)
        # tp_popup("ready_confirm: "+ready_confirm, DR_PM_MESSAGE)
        if ready_confirm == "okay":
            # tp_popup("moving closer", DR_PM_MESSAGE)
            break
    set_ref_coord(DR_BASE)
    movel(Global_handover_l, vel=handover_speed)
    movel(Global_receive_l, vel=5, acc=1)
    # task_compliance_ctrl(stiffness)
    # set_desired_force(f_d, f_dir)
    # force_condition = check_force_condition(DR_AXIS_X, max=force_desired)
    # while (force_condition):
    #     force_condition = check_force_condition(DR_AXIS_X, max=force_desired)
    #     if PART_PRESENT_SENSOR:
    #         break
    wait(3)
    set_digital_output(AIRBLOW_OUTPUT, LOW)
    wait(0.5)
    send("r2,r1,secured", 0)
    # break
    while True:
        part_status = send("", 2)
        # tp_popup("part_status: "+part_status, DR_PM_MESSAGE)
        if part_status == "part_released":
            send("r2,r1,done", 0)
            break
    # release_force()
    # release_compliance_ctrl()
    movel(Global_handover_l, vel=handover_speed)
    movej(Global_handover_j)
    wait(1)
    movej(Global_SR_HOME_j)
    SIDE = side
    tp_log("global SIDE:" + str(SIDE))