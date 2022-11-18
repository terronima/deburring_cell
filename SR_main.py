GREET = 0

# greet the server and establish connection
tp_log("Now greeting...")
if GREET == 0:
    tp_log("Greet complete!")
    greet()
    GREET = 1

while True:
    receive_part()
    SIDE = "R"
    if SIDE == "L":
        pass
        #deburr_L(L_F1, L_F2, L_F3, L_F4, L_F5, L_F6, ref_c= DR_BASE)
    elif SIDE == "R":
        deburr_R(R_F1, R_F2, R_F3, R_F4, R_F5, R_F6, ref_c= DR_BASE) 
    #dip_part()
    place()