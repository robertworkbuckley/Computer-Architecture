"""CPU functionality."""

import sys
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # self.running = True
        self.memory = [0] * 256
        self.registers = [0] * 8
        self.pc = 0

    def ram_read(self, MAR):
        """
        address: addres to read
        returns value stored at that slot in memory
        """
        return self.memory[MAR]

    def ram_write(self, MDR, MAR):
        """
        value: value to write
        address: address to write value to
        """
        self.memory[MAR] = MDR


    def load(self, filename):
        """Load a program into memory."""
        try:
            address = 0
            with open(filename) as f:
                for line in f:
                    comment_split = line.split("#")
                    n = comment_split[0].strip()
                    if n == "":
                        continue

                    val = int(n, 2)
                    self.memory[address] = val

                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found")
            sys.exit(2)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.registers[reg_a] *= self.registers[reg_b]
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
            print(" %02X" % self.registers[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        ADD = 0b10100000
        POP = 0b01000110
        PUSH = 0b01000101
        RET = 0b00010001
        CALL = 0b01010000
        CMP = 0b10100111
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110

        stack_pointer = 244
        run = True
        IR = self.ram_read(self.pc)

        while run:
            # IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            
            if IR == HLT:
                run = False
            elif IR == LDI:
                self.registers[operand_a] = operand_b
                self.pc += 3
            elif IR == PRN:
                print(self.registers[operand_a])
                self.pc +=2
            elif IR == MUL:
                self.alu('MUL', operand_a, operand_b)
                self.pc += 3
            elif IR == ADD:
                self.alu('ADD', operand_a, operand_b)
                self.pc += 3
            elif IR == PUSH:
                stack_pointer -= 1
                self.memory[stack_pointer] = self.registers[operand_a]
                self.pc += 2
            elif IR == POP:
                if stack_pointer < 244:
                    self.registers[operand_a] = self.memory[stack_pointer]
                    stack_pointer += 1
                    self.pc += 2
            elif IR == CALL:
                stack_pointer -= 1
                self.memory[stack_pointer] = self.pc + 2
                self.pc = self.registers[operand_a]
            elif IR == RET:
                self.pc = self.memory[stack_pointer]
                stack_pointer += 1
            #CMP
            elif IR == CMP:
                if self.registers[operand_a] == self.registers[operand_b]:
                    eflag = 1
                    gflag = 0
                    lflag = 0
                elif self.registers[operand_a] > self.registers[operand_b]:
                    eflag = 0
                    gflag = 1
                    lflag = 0
                else:
                    eflag = 0
                    gflag = 0
                    lflag = 1

                self.pc +=3
            #JMP
            elif IR == JMP:
                self.pc = self.registers[operand_a]

            #JEQ
            elif IR == JEQ:
                if eflag == 1:
                    self.pc = self.registers[operand_a]
                else:
                    self.pc += 2
            #JNE
            elif IR == JNE:
                if eflag == 0:
                    self.pc = self.registers[operand_a]
                else:
                    self.pc += 2
            else:
                print(f"Unknown instruction {IR} at address {self.pc}")
                self.pc += 1

            # self.trace()

            IR = self.memory[self.pc]

# cpu = CPU()
# cpu.load()
# cpu.run()