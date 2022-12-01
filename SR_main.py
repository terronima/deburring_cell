GREET = 0
SIDE = ""

# greet the server and establish connection
tp_log("Now greeting...")
if GREET == 0:
    tp_log("Greet complete!")
    move_home(DR_HOME_TARGET_USER)
    greet()
    GREET = 1

while True:
    receive_part()
    set_digital_output(DEBURR_MOTOR, 1)
    if SIDE == "L":
        deburr_L(L_F0, L_F1, L_F2, L_F3, L_F4, L_F5, L_F6, ref_c=L_COORD_SYS)
    elif SIDE == "R":
        deburr_R(R_F0, R_F1, R_F2, R_F3, R_F4, R_F5, R_F6, ref_c= R_COORD_SYS) 
    set_digital_output(DEBURR_MOTOR, 0)
    #dip_part()
    place()