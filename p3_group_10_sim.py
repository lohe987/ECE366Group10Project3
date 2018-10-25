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


# simulator: Simulates the ISA
# Inputs:   program_name - name of the program that gets printed
#           instr_mem_file - name of the instruction file that
#               will be read
#           data_mem_file - name of the data memory file
#               that will be read and written to
def simulator(program_name, instr_mem_file, data_mem_file):
    # Initialize pc and register array
    pc = 0
    reg_arr = [0, 0, 0, 0]
    special_reg_arr = [0, 0, 0, 0]

    print(program_name)

    # Create file variables from file name strings
    instr_mem_input = open(instr_mem_file, "r")
    data_mem_input = open(data_mem_file, "r")

    instr_mem = file_to_array(instr_mem_input)
    data_mem = file_to_array(data_mem_input)

    print(instr_mem)
    print(data_mem)


simulator("Program 1 : Modular Exponentiation",
          "p3_group_10_p1_imem.txt",
          "p3_group_10_dmem_A.txt")

simulator("Program 2 : Best Matching Count",
          "p3_group_10_p2_imem.txt",
          "p3_group_10_dmem_A.txt")
