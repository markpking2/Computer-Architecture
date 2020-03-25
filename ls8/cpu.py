"""CPU functionality."""

import sys


ADD = 0b10100000
# AND = 0b10101000
# CALL = 0b1010000
# CMP = 0b10100111
DEC = 0b01100110
# DIV = 0b10100011
HLT = 0b00000001
INC = 0b01100101
# INT = 0b01010010
# IRET = 0b00010011
# JEQ = 0b01010101
# JGE = 0b01011010
# JGT = 0b01010111
# JLE = 0b01011001
# JLT = 0b01011000
# JMP = 0b01010100
# JNE = 0b01010110
# LD = 0b10000011
LDI = 0b10000010
# MOD = 0b10100100
MUL = 0b10100010
# NOP = 0b00000000
# NOT = 0b01101001
# OR = 0b10101010
POP = 0b01000110
# PRA = 0b01001000
PRN = 0b01000111
PUSH = 0b01000101
# RET = 0b00010001
# SHL = 0b10101100
# SHR = 0b10101101
# ST = 0b10000100
SUB = 0b10100001
# XOR = 0b10101011


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7
        self.reg[self.sp] = 0xF4
        # self.fl = 0
        # self.ie = 0

        self.branchtable = {}
        # self.branchtable[CALL] = self.handle_call
        self.branchtable[HLT] = self.handle_hlt
        # self.branchtable[INT] = self.handle_int
        # self.branchtable[IRET] = self.handle_iret
        # self.branchtable[JEQ] = self.handle_jeq
        # self.branchtable[JGE] = self.handle_jge
        # self.branchtable[JGT] = self.handle_jgt
        # self.branchtable[JLE] = self.handle_jle
        # self.branchtable[JLT] = self.handle_jlt
        # self.branchtable[JMP] = self.handle_jmp
        # self.branchtable[JNE] = self.handle_jne
        # self.branchtable[LD] = self.handle_ld
        self.branchtable[LDI] = self.handle_ldi
        # self.branchtable[MUL] = self.handle_mul
        # self.branchtable[NOP] = self.handle_nop
        self.branchtable[POP] = self.handle_pop
        # self.branchtable[PRA] = self.handle_pra
        self.branchtable[PRN] = self.handle_prn
        self.branchtable[PUSH] = self.handle_push
        # self.branchtable[RET] = self.handle_ret
        # self.branchtable[ST] = self.handle_st

        self.branchtable[ADD] = self.alu_handle_add
        # self.branchtable[AND] = self.alu_handle_and
        # self.branchtable[CMP] = self.alu_handle_cmp
        self.branchtable[DEC] = self.alu_handle_dec
        # self.branchtable[DIV] = self.alu_handle_div
        self.branchtable[INC] = self.alu_handle_inc
        # self.branchtable[MOD] = self.alu_handle_mod
        self.branchtable[MUL] = self.alu_handle_mul
        # self.branchtable[NOT] = self.alu_handle_not
        # self.branchtable[OR] = self.alu_handle_or
        # self.branchtable[SHL] = self.alu_handle_shl
        # self.branchtable[SHR] = self.alu_handle_shr
        self.branchtable[SUB] = self.alu_handle_sub
        # self.branchtable[XOR] = self.alu_handle_xor

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    def load(self, program):
        """Load a program into memory."""
        try:
            address = 0
            with open(program) as f:
                for line in f:
                    line = line.split('#')[0]
                    line = line.strip()
                    if line == '':
                        continue
                    instruction = int(line, 2)
                    self.ram[address] = instruction
                    address += 1
        except FileNotFoundError:
            print('ERROR: Must have valid file name')
            sys.exit(2)

    # def alu(self, op, reg_a, reg_b):
    #     """ALU operations."""

    #     if op == ADD:
    #         self.reg[reg_a] += self.reg[reg_b]
    #     else:
    #         raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while True:
            ir = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            operand_count = ir >> 6
            instruction_length = operand_count + 1

            self.branchtable[ir](operand_a, operand_b)

            self.pc += instruction_length

    def handle_hlt(self, a, b):
        sys.exit(0)

    def handle_ldi(self, a, b):
        self.reg[a] = b

    def handle_pop(self, reg_num, b):
        val = self.ram[self.reg[self.sp]]
        self.reg[reg_num] = val
        self.reg[self.sp] += 1

    def handle_prn(self, a, b):
        print(self.reg[a])

    def handle_push(self, reg_num, b):
        self.reg[self.sp] -= 1
        reg_val = self.reg[reg_num]
        self.ram[self.reg[self.sp]] = reg_val

    def alu_handle_add(self, a, b):
        self.reg[a] += self.reg[b]

    def alu_handle_dec(self, a, b):
        self.reg[a] -= 1

    def alu_handle_inc(self, a, b):
        self.reg[a] += 1

    def alu_handle_mul(self, a, b):
        self.reg[a] *= self.reg[b]

    def alu_handle_sub(self, a, b):
        self.reg[a] -= self.reg[b]
