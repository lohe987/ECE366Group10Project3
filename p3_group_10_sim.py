print("ECE 366 Group 10 Project 3 ISA Simulator")


# file_to_array: Reads each line of a file into an array as elements
# Inputs: file - file that is to be parsed
# Outputs: return_array - array that contains each line
# of the file as an array element
def file_to_array(file):
    return_array = []
    # Reads in each line into the next array element, and
    # removes the newline character
    for line in file:
        return_array.append(line.rstrip())
    return return_array


def execute_operation(opcode, data_mem, reg_arr, special_reg_arr, pc):
    if(opcode[1:4] == "000"):
        # ADD instruction
        rd = int(format(int(opcode[4:6], 2)))
        rs = int(format(int(opcode[6:8], 2)))
        # rd = rd + rs
        reg_arr[rd] += reg_arr[rs]
    return [data_mem, reg_arr, special_reg_arr, pc]


# simulator: Simulates the ISA
# Inputs:   program_name - name of the program that gets printed
#           instr_mem_file - name of the instruction file that
#               will be read
#           data_mem_file - name of the data memory file
#               that will be read and written to
def simulator(program_name, instr_mem_file, data_mem_file):
    # Initialize pc and register array
    pc = 0
    reg_arr = [0, 0, 40, 5]
    special_reg_arr = [0, 0, 0, 0]

    print(program_name)

    # Create file variables from file name strings
    instr_mem_input = open(instr_mem_file, "r")
    data_mem_input = open(data_mem_file, "r")

    instr_mem = file_to_array(instr_mem_input)
    data_mem = file_to_array(data_mem_input)

    for pc in range(0, len(instr_mem)):
        # data_set is of the following format:
        # [data_mem, reg_arr, special_reg_arr, pc]
        opcode = instr_mem[pc]
        data_set = execute_operation(opcode, data_mem, reg_arr, special_reg_arr, pc)
        pc = data_set[3]
        print(data_set[1])


    #print(instr_mem)
    #print(data_mem)


simulator("Program 1 : Modular Exponentiation",
          "p3_group_10_p1_imem.txt",
          "p3_group_10_dmem_A.txt")

simulator("Program 2 : Best Matching Count",
          "p3_group_10_p2_imem.txt",
          "p3_group_10_dmem_A.txt")
