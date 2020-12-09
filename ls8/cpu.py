"""CPU functionality."""

import sys
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
ADD = 0b10100000
MUL = 0b10100010
SP = 0b00000111
PUSH = 0b01000101
POP = 0b01000110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.running = False
        self.ram = [0] * 256
        self.registers = [0] * 8
        self.pc = 0                  # Program Counter
        self.registers[SP] = 0xf4
        self.ops = {}
        self.ops[HLT] = self.HLT
        self.ops[LDI] = self.LDI
        self.ops[PRN] = self.PRN
        self.ops[ADD] = self.ADD
        self.ops[MUL] = self.MUL
        self.ops[PUSH] = self.PUSH
        self.ops[POP] = self.POP


    def ram_read(self, address):
        print(self.registers[address])

    def ram_write(self, address, value):
        self.registers[address] = value

    def HLT(self):
        self.running = False

    def LDI(self):
        address = self.ram[self.pc + 1]
        value = self.ram[self.pc + 2]

        self.ram_write(address, value)
        self.pc += 3

    def PRN(self):
        address = self.ram[self.pc + 1]
        self.ram_read(address)
        self.pc += 2

    def ADD(self):
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]
        self.alu('ADD', reg_a, reg_b)
        self.pc += 3

    def MUL(self):
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]

        self.alu('MUL', reg_a, reg_b)
        self.pc += 3

    def PUSH(self):
            address = self.ram[self.pc + 1]
            value = self.registers[address]
            self.registers[SP] -= 1
            self.ram[self.registers[SP]] = value
            self.pc += 2

    def POP(self):
        address = self.ram[self.pc + 1]
        value = self.ram[self.registers[SP]]
        self.registers[address] = value
        self.registers[SP] += 1
        self.pc += 2

    def load(self):
        """Load a program into memory."""
        try:
            if len(sys.argv) < 2:
                print(f'Error from {sys.argv[0]}: Missing Filename Argument')
                print(f'Usage: {sys.argv[0]} <filename>')

                sys.exit(1)

            # counter to add to ram
            ram_index = 0
            path = sys.argv[1]
            with open('./examples/' + path) as f:
                lines = f.readlines()

            program = []

            for line in lines:
                line = line.strip()
                if '#' in line:
                    comment_start = line.index('#')
                    if comment_start == 0:
                        continue
                    else:
                        binary = int(line[:comment_start].strip(), 2)
                        program.append(binary)

                elif line:
                    binary = int(line, 2)
                    program.append(binary)

            address = 0
            for instruction in program:
                self.ram[address] = instruction
                address += 1

        except FileNotFoundError:
            print(f'Error from {sys.argv[0]}: File Not Found')
            print('Please check the file name and try again')

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]

        elif op == "SUB":
            self.registers[reg_a] -= self.registers[reg_b]

        elif op == "MUL":
            self.registers[reg_a] *= self.registers[reg_b]

        elif op == "AND":
            self.registers[reg_a] &= self.registers[reg_b]

        elif op == "OR":
            self.registers[reg_a] |= self.registers[reg_b]

        elif op == "XOR":
            self.registers[reg_a] ^= self.registers[reg_b]


        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.running = True

        while self.running:
            ir = self.ram[self.pc]
            self.ops[ir]()
