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


def execute_operation(opcode, data_mem, reg_arr, special_reg_arr, pc, branch):
    if opcode[1:4] == "000":
        # ADD instruction
        rd = int(opcode[4:6], 2)
        rs = int(opcode[6:8], 2)
        # rd = rd + rs
        print(rs, rd)
        print(reg_arr)
        reg_arr[rd] += int(reg_arr[rs])
        pc += 1
    elif opcode[1:4] == "001":
        # ADDI instruction
        rd = int(opcode[4:6], 2)
        imm = int(opcode[6:8], 2)
        imm_values = [0, 1, -2, -1]
        reg_arr[rd] += imm_values[imm]
        pc += 1
    elif opcode[1:4] == "010":
        # SLT instruction
        rd = int(opcode[4:6], 2)
        rs = int(opcode[6:8], 2)
        # check if rd is smaller or not
        rd = reg_arr[rd]
        rs = reg_arr[rs]
        if rd < rs:
            branch = 1
        elif rd > rs or rd == rs:
            branch = 0
        pc += 1
    elif opcode[1:4] == "100":
        imm = int(opcode[4:8], 2)
        imm_values = [0, 1, 2, 3, 4, 5, 6, 7, -8, -7, -6, -5, -4, -3, -2, 1]
        imm = imm_values[imm]
        # b instruction (branch)
        if branch ==  1:
            pc += imm
        # this instruction will branch based on SLT being true
        elif branch == 0:
            pc += 1
    elif opcode[1:4] == "011":
        # J instruction
        # instruction for jumping number of lines to new line location in program
        # the immediate number is number of lines ahead/backward pc will travel
        imm = int(opcode[4:8], 2)
        imm_values = [0, 1, 2, 3, 4, 5, 6, 7, -8, -7, -6, -5, -4, -3, -2, 1]
        imm = imm_values[imm]
        pc += imm
    elif opcode[1:5] == "1010":
        # load instruction
        rd = int(opcode[5:7], 2)
        rs = int(opcode[7:8], 2)
        # rd = mem[rs]
        reg_arr[rd] = int(data_mem[rs], 2)
        pc += 1
    elif opcode[1:5] == "1011":
        # store instruction
        rd = int(opcode[5:7], 2)
        rs = int(opcode[7:8], 2)
        # mem[rs] = rd
        # TODO: Convert this into a 16 bit binary value to store back into the data_mem array
        data_mem[rs] = reg_arr[rd]
        pc += 1
    elif opcode[1:6] == "11000":
        # left shift logic instruction
        rd = int(opcode[6:8], 2)
        # multiply the register by 2
        reg_arr[rd] *= 2
        pc += 1
    elif opcode[1:6] == "11001":
        # nxor instruction
        rd = int(opcode[6:7], 2)
        rs = int(opcode[7:8], 2)
        # this line below nots an xor
        reg_arr[rd] = not(reg_arr[rd] ^ reg_arr[rs])
        pc += 1
    elif opcode[1:6] == "11010":
        # EQZ instruction
        # this is the instruction for checking if rd = 0
        rd = int(opcode[6:8], 2)
        if reg_arr[rd] == 0:
            branch = 1
        else:
            branch = 0
        pc += 1
    elif opcode[1:6] == "11011":
        # COMP instruction
        # This performs the 2's complement of a number
        rd = int(opcode[6:8], 2)
        reg_arr[rd] *= -1
        pc += 1
    elif opcode[1:6] == "11100":
        # RCVP instruction
        # This retrieves $rd from a special register $srd
        rd = int(opcode[6:8], 2)
        # our regular register receives specially stored values in a different array of registers
        reg_arr[rd] = special_reg_arr[rd]
        pc += 1
    elif opcode[1:6] == "11101":
        # RST instruction
        # this resets rd to equal 0
        rd = int(opcode[6:8], 2)
        reg_arr[rd] = 0  # reset
        pc += 1
    elif opcode[1:6] == "11110":
        # STSH instruction
        # This saves value in rd to array of special registers indicated in srd
        # for example   reg_arr [0  1  2   rd]  rd is at location reg_arr[3]
        # so this "stashes" into special_reg_arr[3] as well in special_reg_arr[0 1 2 rd]
        rd = int(opcode[6:8], 2)
        special_reg_arr[rd] = reg_arr[rd]
        pc += 1
    elif opcode == "01111110":
        # END
        pc += 500
    return [data_mem, reg_arr, special_reg_arr, pc, branch]


# simulator: Simulates the ISA
# Inputs:   program_name - name of the program that gets printed
#           instr_mem_file - name of the instruction file that
#               will be read
#           data_mem_file - name of the data memory file
#               that will be read and written to
def simulator(program_name, instr_mem_file, data_mem_file):
    # Initialize pc and register array
    pc = 0
    branch = 0
    reg_arr = [0, 0, 0, 0]
    special_reg_arr = [0, 0, 0, 0]

    print(program_name)

    # Create file variables from file name strings
    instr_mem_input = open(instr_mem_file, "r")
    data_mem_input = open(data_mem_file, "r")

    instr_mem = file_to_array(instr_mem_input)
    data_mem = file_to_array(data_mem_input)

    while pc < len(instr_mem):
        # data_set is of the following format:
        # [data_mem, reg_arr, special_reg_arr, pc, branch]
        opcode = instr_mem[pc]
        data_set = execute_operation(opcode, data_mem, reg_arr, special_reg_arr, pc, branch)
        data_mem = data_set[0]
        reg_arr = data_set[1]
        special_reg_arr = data_set[2]
        pc = data_set[3]
        branch = data_set[4]
        print(data_set[3])
        print(data_set[2])
        print(opcode)


    #print(instr_mem)
    #print(data_mem)


simulator("Program 1 : Modular Exponentiation",
          "p3_group_10_p1_imem.txt",
          "p3_group_10_dmem_A.txt")

#simulator("Program 2 : Best Matching Count",
          #"p3_group_10_p2_imem.txt",
          #"p3_group_10_dmem_A.txt")
