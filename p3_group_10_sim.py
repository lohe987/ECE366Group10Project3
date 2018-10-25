print("ECE 366 Group 10 Project 3 ISA Simulator")


def simulator(program_name, instr_mem_file, data_mem_file):
    # Initialize pc and register array
    pc = 0
    reg_arr = [0, 0, 0, 0]
    print(program_name)
    print(instr_mem_file)
    print(data_mem_file)


simulator("Program 1 : Modular Exponentiation",
          "p3_group_10_p1_imem.txt",
          "p3_group_10_dmem_A.txt")

simulator("Program 2 : Best Matching Count",
          "p3_group_10_p2_imem.txt",
          "p3_group_10_dmem_A.txt")
