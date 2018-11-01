import time

print("ECE 366 Group 10 Project 3 ISA Simulator")

# file_to_array: Reads each line of a file into an array as elements
# Inputs: file - file that is to be parsed
# Outputs: return_array - array that contains each line
# of the file as an array element
def file_to_array(file):
    return_array = []
    # Reads in each line into the next array element, and
    # removes the newline character
    # Ignoring all comments and indents
    for line in file:
        line = line.partition('#')[0]
        line = line.rstrip()
        if line[0:1] == '1' or line[0:1] == '0':
            return_array.append(line)

    return return_array

def execute_operation(opcode, data_mem, reg_arr, special_reg_arr, pc, branch):
    if opcode[1:4] == "000":
        # ADD instruction
        print("ADD")
        rd = int(opcode[4:6], 2)
        rs = int(opcode[6:8], 2)
        # rd = rd + rs
        print(reg_arr)
        reg_arr[rd] += int(reg_arr[rs])
        pc += 1
    elif opcode[1:4] == "001":
        # ADDI instruction
        print("ADDI")
        rd = int(opcode[4:6], 2)
        imm = int(opcode[6:8], 2)
        imm_values = [0, 1, -2, -1]#These are the only immediate values allowed to be added to registers
        reg_arr[rd] += imm_values[imm]
        pc += 1
    elif opcode[1:4] == "010":
        # SLT instruction
        print("SLT")
        rd = int(opcode[4:6], 2)
        rs = int(opcode[6:8], 2)
        # check if rd is smaller or not
        rd = reg_arr[rd]
        rs = reg_arr[rs]
        if rd < rs:
            branch = 1   #condition is true
        elif rd > rs or rd == rs:
            branch = 0   #condition is false
        pc += 1
    elif opcode[1:4] == "100":
        # B Instruction
        print("B")
        imm = int(opcode[4:8], 2)
        imm_values = [0, 1, 2, 3, 4, 5, 6, 7, -8, -7, -6, -5, -4, -3, -2, -1] #pass immediate from this array to be used in function
        imm = imm_values[imm]
        # b instruction (branch)
        if branch == 1:
            pc += imm
        # this instruction will branch based on SLT being true
        elif branch == 0:
            pc += 1
    elif opcode[1:4] == "011":
        # J instruction
        # instruction for jumping number of lines to new line location in program
        # the immediate number is number of lines ahead/backward pc will travel
        print("J")
        imm = int(opcode[4:8], 2)
        imm_values = [0, 1, 2, 3, 4, 5, 6, 7, -8, -7, -6, -5, -4, -3, -2, -1]
        imm = imm_values[imm]
        pc += imm
    elif opcode[1:5] == "1010":
        # load instruction
        print("LOAD")
        rd = int(opcode[5:7], 2)
        rs = int(opcode[7:8], 2)
        rs_value = reg_arr[rs]
        data_value = data_mem[rs_value]
        # Checks if memory address is out of range
        if rs_value < 0 or rs_value > 108:
            print("OUT OF MEMORY BOUNDS:")
            pc += 1
        print("Data Value: ")
        print(data_value)
        # Negative Value
        value = 0
        if data_value[0] == "1":
            value = 0b1111111111111111 - int(data_value, 2) + 1 #take 2's compliment
            reg_arr[rd] = 0 - value
        else:   #this if else section helped us debug errors for our load instruction
            reg_arr[rd] = int(data_mem[rs_value], 2)
        pc += 1
    elif opcode[1:5] == "1011":
        # store instruction
        print("STORE")
        rd = int(opcode[5:7], 2)
        rs = int(opcode[7:8], 2)
        # converts into 16 bit binary value
        print("reg_arr value")
        print(reg_arr[rd])
        a = 0#initiate a
        if reg_arr[rd] < 0:
            print("NEGATIVE STORE")
            pos_value = 0 - reg_arr[rd]#this is meant store a negative value
            a = 0b1111111111111111 - pos_value + 1#2's complement
            a = '{0:016b}'.format(a)#formating the 2's complemented value
        else:
            a = '{0:016b}'.format(reg_arr[rd])
        print("A")
        print(a)#this if else is meant for debugging to show us what's going on during the runtime of this simulator
        data_mem[reg_arr[rs]] = a
        pc += 1
    elif opcode[1:6] == "11000":
        # left shift logic instruction
        print("LSL")
        rd = int(opcode[6:8], 2)
        dec_value = reg_arr[rd]
        a = ""
        if dec_value < 0:
            print("NEGATIVE LEFT SHIFT")
            pos_value = 0 - dec_value#flip rd value
            a = 0b1111111111111111 - pos_value + 1#obtain 2's C for debugging
            a = str('{0:016b}'.format(a))#shows us base 2
            print("A: ", a)
        else:#This instruction was a pain because it would shift the decimal value from -20000 to -40000 which is technically out of range so in this if else statement you see where we got the idea for our method of debugging
            a = str('{0:016b}'.format(reg_arr[rd]))
        print("BINARY VALUE:  ", a)
        bin_value = '{0:016b}'.format(int(a))#We adjust the binary value to accept a zero being added to it
        new_bin_str = a[1:16] + "0"#since we begin writing from [1:16] we can shift everything over to 0:15 then add the zero to LSB 
        #print("bin_value:     ", str(bin_value)) --ignore this line, it didn't work
        print("new_bin_value: ", new_bin_str)
        if new_bin_str[0] == "1":
            value = 0b1111111111111111 - int(new_bin_str, 2) + 1
            reg_arr[rd] = 0 - value
        else:
            reg_arr[rd] = int(new_bin_str, 2)
        print("ORIGINAL VALUE: ", dec_value)
        print("NEW VALUE: ", reg_arr[rd])
        #reg_arr[rd] = (reg_arr[rd] * 2) % 33678 --ignore this line, it was 1/4 of our attempts at computing logic shift left
        pc += 1
    elif opcode[1:6] == "11001":
        # nxor instruction
        print("NXOR")
        rd = int(opcode[6:7], 2)
        rs = int(opcode[7:8], 2)
        rd_value = reg_arr[rd]
        rs_value = reg_arr[rs]
        rd_bin = 0
        rs_bin = 0
        if rd_value < 0:#this if else helps us properly perform 2's complement of a decimal number to binary
            pos_value = 0 - rd_value
            a = 0b1111111111111111 - pos_value + 1
            rd_bin = '{0:016b}'.format(a)
        else:
            rd_bin = '{0:016b}'.format(reg_arr[rd])

        if rs_value < 0:#this also helps us change from deci to bin in 2's Complement
            pos_value = 0 - rs_value
            a = 0b1111111111111111 - pos_value + 1
            rs_bin = '{0:016b}'.format(a)
        else:
            rs_bin = '{0:016b}'.format(reg_arr[rs])


        nxor_value = ~(reg_arr[rd] ^ reg_arr[rs])#this performs the nxor bitwise computation
        nxor_bin = 0
        if nxor_value < 0:#this if else helped us debug by seeing what value were computed
            pos_value = 0 - nxor_value
            a = 0b1111111111111111 - pos_value + 1
            nxor_bin = '{0:016b}'.format(a)
        else:
            nxor_bin = '{0:016b}'.format(reg_arr[rd])

        print("RD VALUE: ", rd_value)#These print statements helped us view what was going on during the instruction
        print("RS VALUE: ", rs_value)#They would allow us to debug this instruction more accurately
        print("NXOR VAL: ", nxor_value)
        print("RD BIN:   ", rd_bin)
        print("RS BIN:   ", rs_bin)
        print("NXOR BIN: ", nxor_bin)
        reg_arr[rd] = ~(reg_arr[rd] ^ reg_arr[rs])
        print()
        pc += 1
    elif opcode[1:6] == "11010":
        # EQZ instruction
        # this is the instruction for checking if rd = 0
        #if rd == 0 then branch = 1
        print("EQZ")
        rd = int(opcode[6:8], 2)
        if reg_arr[rd] == 0:
            branch = 1
        else:
            branch = 0
        pc += 1
    elif opcode[1:6] == "11011":
        # COMP instruction
        # This performs the 2's complement of a number
        print("COMP")
        rd = int(opcode[6:8], 2)
        reg_arr[rd] *= -1
        pc += 1
    elif opcode[1:6] == "11100":
        # RCVP instruction
        # This retrieves $rd from a special register $srd
        print("RCVR")
        rd = int(opcode[6:8], 2)
        # our regular register receives specially stored values in a different array of registers
        reg_arr[rd] = special_reg_arr[rd]
        pc += 1
    elif opcode[1:6] == "11101":
        # RST instruction
        # this resets rd to equal 0
        print("RST")
        rd = int(opcode[6:8], 2)
        reg_arr[rd] = 0  # reset
        pc += 1
    elif opcode[1:6] == "11110":
        # STSH instruction
        # This saves value in rd to array of special registers indicated in srd
        # for example   reg_arr [0  1  2   rd]  rd is at location reg_arr[3]
        # so this "stashes" into special_reg_arr[3] as well in special_reg_arr[0 1 2 rd]
        print("STSH")
        rd = int(opcode[6:8], 2)
        special_reg_arr[rd] = reg_arr[rd]
        pc += 1
    elif opcode[0:8] == "11111111":
        # END
        print("END")
        pc += 500
    else:
        pc += 1
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
    reg_arr = [0, 0, 0, 0]#positions[$R0, $R1, $R2, $R3]
    special_reg_arr = [0, 0, 0, 0]#positions[$SR0, $SR1, $SR2, $SR3]

    print(program_name)

    # Create file variables from file name strings
    instr_mem_input = open(instr_mem_file, "r")#read file for our programming instructions
    data_mem_input = open(data_mem_file, "r")#read file for memory on what to compute

    instr_mem = file_to_array(instr_mem_input)
    data_mem = file_to_array(data_mem_input)
    dic = 0#at the end of program run we will display the DIC
    while pc < len(instr_mem):
        # data_set is of the following format:
        # [data_mem, reg_arr, special_reg_arr, pc, branch]
        opcode = instr_mem[pc]
        print("PC: ", pc)
        data_set = execute_operation(opcode, data_mem, reg_arr, special_reg_arr, pc, branch)
        data_mem = data_set[0]
        reg_arr = data_set[1]
        special_reg_arr = data_set[2]
        pc = data_set[3]
        branch = data_set[4]
        print("reg_arr: ",reg_arr)#These lines print for each instruction so we know what is being stored in each register
        print("special_Reg_arr: ", special_reg_arr)#special register
        print("MEM[4]: Highest Score ", data_mem[4])#memory locations so we know we're getting the right values stored
        print("MEM[5]: Count         ", data_mem[5])
        print("\n")
        dic += 1#increment DIC by 1 everytime we perform an instruction
        #time.sleep(.001)  --we left this at value .2 originally so we could look for bugs in our jump and branch instructions
    print("Dynamic Instruction Count: ", dic)

    #print(instr_mem)
    #print(data_mem)
#you can delete the "#" on any of these blocks of code below to see that the code runs correctly, note that both p1 and p2 work
#simulator("Program 0 : Simulator Testing",
#          "p3_group_10_p0_imem.txt",
#          "p3_group_10_dmem_A.txt")

simulator("Program 1 : Modular Exponentiation",
            "p3_group_10_p1_imem.txt",
            "p3_group_10_dmem_B.txt")

#simulator("Program 2 : Best Matching Count",
#          "p3_group_10_p2_imem.txt",
#          "p3_group_10_dmem_A.txt")
