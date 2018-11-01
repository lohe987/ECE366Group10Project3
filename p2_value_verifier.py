#We created this program after finishing p2 so we can make sure the S and C
#values were correct when compared
#In short we wanted to make sure values stored into 4 and 5 for Dmem B were in
#fact 12 matching bits with a total 4 numbers having this count
print("Tests the values of P2 using pure python")

def file_to_array(file):
    array = []
    for line in file:
        array.append(line.rstrip())
    return array


def best_matching_count(data_mem_file_name):
    data_mem_file = open(data_mem_file_name, "r")
    mem_array = file_to_array(data_mem_file)
    target_value = mem_array[3]

    best_matching_score = 0
    best_matching_count = 0
    for i in range(8, 108):
        current_value = mem_array[i]
        temp_score = 0
        for j in range(0, 16):
            if target_value[j] == current_value[j]:
                temp_score += 1
        if temp_score > best_matching_score:
            best_matching_score = temp_score
            best_matching_count = 1
        elif temp_score == best_matching_score:
            best_matching_count += 1

        print("\n")
        i += 1
    print("BEST MATCHING SCORE: ", best_matching_score)
    print("BEST MATCHING COUNT: ", best_matching_count)


best_matching_count("p3_group_10_dmem_A.txt")
