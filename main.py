
# test splitting sequence (0-8 are rights, 9-17 are lefts)
camera_data = [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1]
only_left = 0
only_right = 0
intermittent = 1
side_by_side = 0

if only_left:
    cntr = 0
    for i in camera_data[0:int(len(camera_data) / 2)]:
        if i == 1:
            print(f"Only left selected, pick pos: {cntr}")
        cntr += 1
elif only_right:
    cntr = 9
    for i in camera_data[int(len(camera_data) / 2)::]:
        if i == 1:
            print(f"Only right selected, pick pos: {cntr}")
        cntr += 1
elif intermittent:
    pick_el_1 = 0
    pick_el_2 = 0
    string_of_picks = ""
    for i in range(0, int(len(camera_data) / 2)):
        pick_el_1 = i
        pick_el_2 = i + int(len(camera_data) / 2)
        if camera_data[pick_el_1] == 1:
            string_of_picks += str(i) + ','
        if camera_data[pick_el_2] == 1:
            string_of_picks += str(pick_el_2) + ','
    print(f"parts to be picked {string_of_picks}")
elif side_by_side:
    cntr = 0
    for i in camera_data[0:int(len(camera_data) / 2)]:
        if i == 1:
            print(f"Only left selected, pick pos: {cntr}")
        cntr += 1
    for i in camera_data[int(len(camera_data) / 2)::]:
        if i == 1:
            print(f"Only right selected, pick pos: {cntr}")
        cntr += 1
# flipping certain number of elements of the array
arr_1 = [0, 1, 2, 3, 4]
arr_2 = []
step = 5
ctr = 1
j = min(step - 1, len(arr_1) - 1)
step_over = 0
for i in range(0, int(len(arr_1))):
    if j > len(arr_1) - 1 and step_over:
        break
    if j >= len(arr_1):
        j = j - (j - (len(arr_1) - 1))
        step_over = 1
    print(f"j value: {j}")
    arr_2.append(arr_1[j])
    j -= 1
    if j == (step * ctr) - (step + 1):
        j = step * ctr + step - 1
        ctr += 1

print(arr_2)
# map = "00000"
# if not int(map):
#     map[1] = "1"
#     print(f"the map variable is {map}")
# else:
#     print(map)