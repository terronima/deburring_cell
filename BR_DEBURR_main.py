pallet_place = None
camera_map = 0
pallet_map = []
GREET = 0
cntr = 0

if get_digital_input(PART_PRESENT_SENSOR):
    #Estop_recovery()
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

while True:
    tp_log("Entering big loop...")
    #PAUSE = int(send("r1,HMI,is_r1_paused"))
    PAUSE = 0
    tp_log(str(PAUSE))
    if PAUSE:
        time.sleep(1)
    else:
        # request camera map
        while True:
            camera_map = send("r1,cam,r1_send_cam_data", 1)
            time.sleep(1)
            camera_map = camera_map.strip("z")
            if len(camera_map) == 18:
                break
        tp_log("Original_camera_map before" + str(camera_map))        
        tp_log("Original_camera_map " + str(camera_map))
           
        pallet_map = []
        tp_log("cleared pallet map: " + str(pallet_map))
        pallet_map_str = camera_map
        for i in pallet_map_str:
            pallet_map.append(int(i))
        tp_log("updated_pallet_map " + str(pallet_map))
        while True:
            PICK_MODE = send("r1,HMI,PICK_MODE", 1)   
            time.sleep(1)
            PICK_MODE = PICK_MODE.strip("z")
            tp_log("Pick mode:" + PICK_MODE) 
            if  PICK_MODE in [ "left_only", "right_only", "intermittent", "side_by_side"]:
                break
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

            #PICK_FLAG = pick(pick_pos)
            PICK_FLAG = 1
            SIDE = "L"

            if PICK_FLAG:
                
                if SIDE == "L":
                    set_digital_output(LEFT_MOTOR, 1)
                    deburr_L_B1(L_1_COORD_SYS)
                    deburr_L_B2(L_2_COORD_SYS)
                    #pass
                elif SIDE == "R":
                    set_digital_output(RIGHT_MOTOR, 1)
                    deburr_R_B1(R_1_COORD_SYS)
                    deburr_R_B2(L_2_COORD_SYS)
                    #pass
                    
                if PICK_MODE == "left_only":
                    L_pallet_sum = 0
                    for i in range(int(len(pallet_map[9::])), int(len(pallet_map))):
                        L_pallet_sum += i
                        if L_pallet_sum == 0:
                            set_digital_output(LEFT_MOTOR, 0)
                
                elif PICK_MODE == "right_only":
                    R_pallet_sum = 0
                    for i in range(0, int(len(pallet_map[0:9]))):
                        R_pallet_sum += i
                        if R_pallet_sum == 0:
                            set_digital_output(RIGHT_MOTOR, 0)

                elif PICK_MODE == "intermittent":
                    if SIDE == "L":
                        set_digital_output(LEFT_MOTOR, 0) 
                    elif SIDE == "R":
                        set_digital_output(RIGHT_MOTOR, 0)

                elif PICK_MODE == "side_by_side":
                    if SIDE == "R":
                        R_pallet_sum = 0
                        for i in range(0, int(len(pallet_map[0:9]))):
                            R_pallet_sum += i
                        if R_pallet_sum == 0:
                            set_digital_output(RIGHT_MOTOR, 0)
                    elif SIDE == "L":
                        L_pallet_sum = 0
                        for i in range(int(len(pallet_map[9::])), int(len(pallet_map))):
                            L_pallet_sum += i
                        if L_pallet_sum == 0:
                            set_digital_output(LEFT_MOTOR, 0)
                handover()
                
            if SIDE == "R":
                cntr = pick_pos
            elif SIDE == "L":
                cntr = pick_pos + 9
            pallet_map[cntr] = 0
            tp_log("cntr is: " + str(cntr))    
            tp_log(str(pallet_map))
            if sum(pallet_map) == 0:
                tp_log("camera map is empty")
                set_digital_output(RIGHT_MOTOR, 0)
                set_digital_output(LEFT_MOTOR, 0)
                break
    tp_log("small loop breaked")