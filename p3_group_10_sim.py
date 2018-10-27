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
        print(reg_arr[rd])
    elif(opcode[1:4] == "001"):
        #ADDI instruction
        rd = int(format(int(opcode[4:6], 2)))
        if(opcode[6][0] =='1'):                #check if MSB in imm is 1
            imm = int(opcode[6:8],2)    
            imm = int(format(imm - 4))            #convert 2's compliment to decimal
        else:
            imm = int(format(int(opcode[6:8], 2)))   #if MSB in imm is 0 
        
        print(imm)
        # rd = rd + imm
        reg_arr[rd] += imm
        
    elif(opcode[1:4] == "010"):
        #SLT instruction
        rd = int(format(int(opcode[4:6], 2)))
        rs = int(format(int(opcode[6:8], 2)))
        #check if rd is smaller or not
        if(rd < rs):
            branch=1
        elif(rd > rs or rd == rs):
            branch=0
    elif(opcode[1:4] == "100"):
        if(opcode[4][0] =='1'):                #check if MSB in imm is 1
            imm = int(opcode[4:8],2)    
            imm = int(format(imm - 16))            #convert 2's compliment to decimal
        else:
            imm = int(format(int(opcode[4:8], 2)))   #if MSB in imm is 0 
        #b instruction (branch)
        if(branch ==  1):
            pc+=imm
        #this instruction will branch based on SLT being true
        elif(branch == 0):
            pc+=1
    elif(opcode[1:4] == "011"):
        #J instruction
        #instruction for jumping number of lines to new line location in program
        if(opcode[4][0] =='1'):                #check if MSB in imm is 1
            imm = int(opcode[4:8],2)    
            imm = int(format(imm - 16))            #convert 2's compliment to decimal
        else:
            imm = int(format(int(opcode[4:8], 2)))   #if MSB in imm is 0 
        #the immediate number is number of lines ahead/backward pc will travel
        pc+=imm
    elif(opcode[1:5] == "1010"):
        #load instruction
        rd = int(format(int(opcode[5:7], 2)))
        rs = int(format(int(opcode[7:8], 2)))
        #rd = mem[rs]
        reg_arr[rd] = data_mem[rs]
    elif(opcode[1:5] == "1011"):
        #store instruction
        rd = int(format(int(opcode[5:7], 2)))
        rs = int(format(int(opcode[7:8], 2)))
        #mem[rs] = rd
        data_mem[rs] = reg_arr[rd]
    elif(opcode[1:6] == "11000"):
        #left shift logic instruction
        rd = int(format(int(opcode[6:8], 2)))
        reg_arr[rd] *=2
        #multiply the register by 2
    elif(opcode[1:6] == "11001"):
        #nxor instruction
        rd = int(format(int(opcode[6:7], 2)))
        rs = int(format(int(opcode[7:8], 2)))
        #this line below nots an xor
        reg_arr[rd] = not(reg_arr[rd] ^ reg_arr[rs])
    elif(opcode[1:6] == "11010"):
        #EQZ instrustion
        #this is the instruction for checking if rd = 0
        rd = int(format(int(opcode[6:8], 2)))
        if (rd == 0):
            branch = 1
        else:
            branch = 0
            pc+=1
    elif(opcode[1:6] == "11011"):
        #COMP instruction
        #This performs the 2's complement of a number
        rd = int(format(int(opcode[6:8], 2)))
        reg_arr[rd] = -1*(rd)
    elif(opcode[1:6] == "11100"):
        #RCVP instruction
        #This retrieves $rd from a special register $srd
        rd = int(format(int(opcode[6:8], 2)))
        reg_arr[rd] = special_reg_arr[rd]
        #our regular register recieves specially stored values in a different array of registers
    elif(opcode[1:6] == "11101"):
        #RST instruction
        #this resets rd to equal 0
        rd = int(format(int(opcode[6:8], 2)))
        reg_arr[rd] = 0  #reset
    elif(opcode[1:6] == "11110"):
        #STSH instruction
        #This saves value in rd to array of special registers indicated in srd
        #for example   reg_arr [0  1  2   rd]  rd is at location reg_arr[3]
        #so this "stashes" into special_reg_arr[3] as well in special_reg_arr[0 1 2 rd]
        rd = int(format(int(line[6:8],2)))
        special_reg_arr[rd] = reg_arr[rd]
    elif(opcode == "01111110"):
        #END
        for a in range(8):
            a+=1
            #we need to determine how to pass rd into this function
            
            
    #need to update pc by 1 every cycle
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

#simulator("Program 2 : Best Matching Count",
          #"p3_group_10_p2_imem.txt",
          #"p3_group_10_dmem_A.txt")
