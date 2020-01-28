"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8

        self.pc = 0
        # self.mar = 0
        # self.mdr = 0
        self.fl = 0

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    # Memory Address Register (MAR) -------?
    def ram_read(self, mar):
        # print(mar) #debug
        return self.ram[mar]

    # Memory Data Register (MDR) ----------?
    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        LDI = 0b10000010 # LDI
        HLT = 0b00000001 # HLT
        PRN = 0b01000111 # PRN R0

        # ir = self.ram_read(self.pc)
        # operand_a = self.ram_read(self.pc+1)
        # operand_b = self.ram_read(self.pc+2)

        running = True

        while running:

            ir = self.ram_read(self.pc)
            # print(f'ir: {ir}, pc: {self.pc}') #debug
            if ir == LDI:
                # print('LDI') #debug
                operand_a = self.ram_read(self.pc+1)
                operand_b = self.ram_read(self.pc+2)

                #-- option 1
                self.ram_write(operand_a, operand_b)

                #-- option 2
                # self.ram[operand_a] = operand_b

                #-- option 3
                # self.reg = operand_b
                self.pc += 3

            if ir == HLT:
                # print('HLT') #debug
                running = False
                self.pc += 1

            if ir == PRN:
                # print('PRN') #debug
                operand_a = self.ram_read(self.pc+1)

                #-- option 1
                print(self.ram_read(operand_a))

                #-- option 2
                # print(self.ram[operand_a])

                #-- option 3
                # print(self.reg)
                self.pc += 2
