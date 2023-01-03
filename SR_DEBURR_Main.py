GREET = 0
SIDE = "L"

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

while True:
    receive_part()
    if SIDE == "R":
        send("r2,HMI,start_SRR", 0)
    elif SIDE == "L":
        send("r2,HMI,start_SRL", 0)
    set_digital_output(DEBURR_MOTOR, START)
    if SIDE == "L":
        deburr_L(L_COORD_SYS)
        # pass
    elif SIDE == "R":
        deburr_R(R_COORD_SYS)
        # pass
    set_digital_output(DEBURR_MOTOR, STOP)
    if not get_digital_input(WATER_LEVEL_SENSOR):
        dip_part()
    else:
        send("r2,HMI,r2_faulted", 0)
    place()
    if SIDE == "R":
       send("r2,HMI,qsr", 0)
       send("r2,HMI,stop_SRR", 0)
    elif SIDE == "L":
       send("r2,HMI,qsl", 0)
       send("r2,HMI,stop_SRL", 0)