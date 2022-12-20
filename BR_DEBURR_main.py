pallet_place = None
camera_map = 0
pallet_map = []
GREET = 0
cntr = 0

if get_digital_input(PART_PRESENT_SENSOR):
    Estop_recovery()
    wait(1)

# greet the server and establish connection
tp_log("Now greeting...")
if GREET == 0:
    tp_log("Greet complete!")
    move_home(DR_HOME_TARGET_USER)
    greet()
    GREET = 1

# if not (get_digital_input(PART_PRESENT_SENSOR)):
#     movej(Global_part_remove)

HMI_Offset_th_id = thread_run(fn_th_HMI_Offset, loop=True)

while True:
    tp_log("Entering big loop...")
    # PAUSE = int(send("r1,HMI,is_r1_paused"))
    PAUSE = 0
    tp_log(str(PAUSE))
    if PAUSE:
        time.sleep(1)
    else:
        # request camera map constantly until gets string of len 18
        while True:
            camera_map = send("r1,cam,r1_send_cam_data", 1)
            time.sleep(1)
            camera_map = camera_map.strip("z")
            if len(camera_map) == 18:
                break
        pallet_map = []
        pallet_map_str = camera_map
        for i in pallet_map_str:
            pallet_map.append(int(i))
        tp_log("pallet_map " + str(pallet_map))

        while True:
            PICK_MODE = send("r1,HMI,PICK_MODE", 1)
            time.sleep(1)
            PICK_MODE = PICK_MODE.strip("z")
            tp_log("Pick mode:" + PICK_MODE)
            if PICK_MODE in ["left_only", "right_only", "intermittent", "side_by_side"]:
                break

        if sum(pallet_map) == 0:
            time.sleep(2)

        else:
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

                if SIDE == "R":
                    send("r1,HMI,start_LRR", 0)
                elif SIDE == "L":
                    send("r1,HMI,start_LRL", 0)

                PICK_FLAG = pick(pick_pos)
                # PICK_FLAG = 1
                # SIDE = "R"

                if PICK_FLAG:

                    if SIDE == "L":
                        deburr_L_B1(R_BRUSH_COORD_SYS)
                        deburr_L_B2(L_BRUSH_COORD_SYS)
                        # pass
                    elif SIDE == "R":
                        deburr_R_B1(R_BRUSH_COORD_SYS)
                        deburr_R_B2(L_BRUSH_COORD_SYS)
                        # pass

                    handover()

                    if SIDE == "R":
                        send("r1,HMI,stop_LRR", 0)
                    elif SIDE == "L":
                        send("r1,HMI,stop_LRL", 0)

                if SIDE == "R":
                    cntr = pick_pos
                elif SIDE == "L":
                    cntr = pick_pos + 9
                pallet_map[cntr] = 0
                tp_log("cntr is: " + str(cntr))
                tp_log(str(pallet_map))
                if sum(pallet_map) == 0:
                    tp_log("out of parts")
                    break