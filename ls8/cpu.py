"""CPU functionality."""

import sys

LDI = 0b10000010 # LDI
HLT = 0b00000001 # HLT
PRN = 0b01000111 # PRN R0
MUL = 0b10100010 # MUL R0,R1
PUSH = 0b01000101 # PUSH R0
POP = 0b01000110 # POP R0

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8

        self.pc = 0
        self.sp = 7
        self.reg[self.sp] = 0xF4
        # self.mar = 0
        # self.mdr = 0
        self.fl = 0
        self.branchtable = {}
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[PRN] = self.handle_prn
        self.branchtable[MUL] = self.handle_mul
        self.branchtable[PUSH] = self.handle_push
        self.branchtable[POP] = self.handle_pop

    def load(self, filename):
        """Load a program into memory."""
        try:
            address = 0
            with open(filename) as f:
                for line in f:
                    comment_split = line.split('#')
                    num = comment_split[0].strip()

                    if num == "":
                        continue

                    value = int(num, 2)

                    self.ram[address] = value
                    address += 1
            # print(self.ram)

        except FileNotFoundError:
            print(f'{sys.argv[0]}: {filename} not found')
            sys.exit(2)

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

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
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]

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

    def handle_ldi(self):
        operand_a = self.ram_read(self.pc+1)
        operand_b = self.ram_read(self.pc+2)

        self.reg[operand_a] = operand_b
        self.pc += 3

    def handle_prn(self):
        operand_a = self.ram_read(self.pc+1)

        print(self.reg[operand_a])
        self.pc += 2

    def handle_mul(self):
        operand_a = self.ram_read(self.pc+1)
        operand_b = self.ram_read(self.pc+2)

        self.alu('MUL', operand_a, operand_b)

        self.pc += 3

    def handle_push(self):
        operand_a = self.ram_read(self.pc+1)
        self.reg[self.sp] -= 1
        self.ram_write(self.reg[self.sp], self.reg[operand_a])

        self.pc += 2

    def handle_pop(self):
        operand_a = self.ram_read(self.pc+1)
        value = self.ram_read(self.reg[self.sp])
        self.reg[operand_a] = value
        self.reg[self.sp] += 1

        self.pc += 2

    def run(self):
        """Run the CPU."""

        # LDI = 0b10000010 # LDI
        HLT = 0b00000001 # HLT
        # PRN = 0b01000111 # PRN R0
        # MUL = 0b10100010 # MUL R0,R1

        # ir = self.ram_read(self.pc)
        # operand_a = self.ram_read(self.pc+1)
        # operand_b = self.ram_read(self.pc+2)

        running = True

        while running:
            # print(self.reg)
            # print(self.ram[self.reg[self.sp]])
            ir = self.ram_read(self.pc)
            # print(f'ir: {ir}, pc: {self.pc}') #debug
            if ir == HLT:
                # print('HLT') #debug
                running = False
                self.pc += 1
            elif ir != HLT:
                self.branchtable[ir]()

            # if ir == LDI:
                # # print('LDI') #debug
                # operand_a = self.ram_read(self.pc+1)
                # operand_b = self.ram_read(self.pc+2)

                # #-- option 1
                # # self.ram_write(operand_a, operand_b)

                # #-- option 2
                # # self.ram[operand_a] = operand_b

                # #-- option 3
                # self.reg[operand_a] = operand_b
                # self.pc += 3

            # if ir == PRN:
            #     # print('PRN') #debug
            #     operand_a = self.ram_read(self.pc+1)

            #     #-- option 1
            #     # print(self.ram_read(operand_a))

            #     #-- option 2
            #     # print(self.ram[operand_a])

            #     #-- option 3
            #     print(self.reg[operand_a])
            #     self.pc += 2

            # if ir == MUL:
            #     operand_a = self.ram_read(self.pc+1)
            #     operand_b = self.ram_read(self.pc+2)

            #     self.alu('MUL', operand_a, operand_b)

            #     self.pc += 3
