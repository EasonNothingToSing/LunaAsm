#!/usr/bin/env python3

import os
import argparse
import io
import re
import glob

# user defined content for the prefix and suffix in hex file
prefix_hex = [
#    '0x00000000',
#    'bl #1',
#    'push {lr}',
]
suffix_hex = [
#    'pop {lr}',
#    'b lr',
#    '0x00000000',
]

# user defined content for the prefix and suffix in .c file
prefix_c = [
    '#include "test.h"\n',
]
suffix_c = [
    '',
]

# user defined content for the prefix and suffix in .h file
prefix_h = [
    '#ifndef __TEST_H__\n'
    '#define __TEST_H__\n\n',
    '#include "stdint.h"\n\n',
]
suffix_h = [
    '\n#endif\n',
]

class InstFuncLabel:
    def __init__(self):
        self.size = 0
        self.list_inst = []
        self.list_label = []

    def find_label_pos(self,label):        
        return self.list_label.index(label)

    def add(self,inst, label):        
        self.list_inst.append(inst)
        self.list_label.append(label)
        self.size += 1

    def length(self):
        return self.size     

class InstructionParser(object):

    instruction_dict = {
        'jump'  :   0b000001, 
        'repeat':   0b001000,
        'wait'  :   0b100000, 
        'cmp'   :   0b000010, 
        'b'     :   0b000011, 
        'bl'    :   0b000011, 
        'bx'    :   0b000011, 
        'beq'   :   0b000011, 
        'blt'   :   0b000011, 
        'bgt'   :   0b000011, 
        'bne'   :   0b000011, 
        'ble'   :   0b000011, 
        'bge'   :   0b000011,
        'ldro'  :   0b000100,
        'lea'   :   0b000101,
        'ldr'   :   0b001010, 
        'ldrb'  :   0b001010, 
        'ldrh'  :   0b001010, 
        'ldrsb' :   0b001010, 
        'ldrsh' :   0b001010, 
        'ldm'   :   0b001010, 
        'pop'   :   0b001010,
        'stro'  :   0b000110,
        'str'   :   0b001011, 
        'strb'  :   0b001011, 
        'strh'  :   0b001011, 
        'strsb' :   0b001011, 
        'strsh' :   0b001011, 
        'stm'   :   0b001011, 
        'push'  :   0b001011, 
        'setr'  :   0b010000, 
        'setrh' :   0b010000, 
        'setrl' :   0b010000, 
        'seti'  :   0b010111, 
        'setih' :   0b010111, 
        'setil' :   0b010111, 
        'gopr'  :   0b010001,
        'addl'  :   0b010001, 
        'addm'  :   0b010001, 
        'add'   :   0b010001, 
        'subl'  :   0b010001,
        'subm'  :   0b010001,
        'sub'   :   0b010001,
        'andl'  :   0b010010, 
        'andm'  :   0b010010, 
        'and'   :   0b010010,
        'notl'  :   0b010010,
        'notm'  :   0b010010,
        'not'   :   0b010010,
        'orrl'  :   0b010011, 
        'orrm'  :   0b010011, 
        'orr'   :   0b010011,
        'xorl'  :   0b010011,
        'xorm'  :   0b010011,
        'xor'   :   0b010011,
        'asr'   :   0b010100, 
        'lsr'   :   0b010100, 
        'lsl'   :   0b010101,
        'mul'   :   0b010110,
        'muls'  :   0b010110,
        'mulsb' :   0b010110,
        'mulb'  :   0b010110,
        'mulshl':   0b010110,
        'mulhl' :   0b010110,
        'mulshm':   0b010110,
        'mulhm' :   0b010110,
        'mov'   :   0b011000, 
        'movb'  :   0b011000, 
        'movh'  :   0b011000, 
        'movl'  :   0b011000, 
        'cmov'  :   0b011001,
        'cmoveq':   0b011001,
        'cmovgt':   0b011001,
        'cmovlt':   0b011001,
        'cmovne':   0b011001,
        'cmovle':   0b011001,
        'cmovge':   0b011001,
        }

    operand_wait = {
        'non-block' : 1<<25,
        'block'     : 0<<25,
        'interrupt' : 1<<24,
        'event'     : 1<<23,
        'status'    : 1<<22,
        'id'        : 1<<8, 
        'iow'       : 1<<5, 
        'master0'   : 1<<4, 
        'master1'   : 1<<3, 
        'slave0'    : 1<<2, 
        'slave1'    : 1<<1, 
        'pe'        : 1<<0,     
        }

    inst_extension = None

    
    IMM_BOTH = 2  
    IMM_SIGNED = 1  
    IMM_UNSIGNED = 0

    def __init__(self, extension = False):
        if extension == True:
            inst_parser_ext = self.module_exists("luna_asm_extension")
            if inst_parser_ext is not None:
                self.inst_extension = inst_parser_ext.InstructionExtension()

    def module_exists(self, module_name):
        import importlib
        from importlib import util
        module = None
        if importlib.util.find_spec(module_name):
            module = importlib.import_module(module_name)
        return module


    def imm_validate(self, val, bits, signed):
        if bits < 1 or bits > 32:
            raise ValueError('the immediate number has invalid bits')
        if signed != self.IMM_SIGNED and signed != self.IMM_UNSIGNED and signed != self.IMM_BOTH :
            raise ValueError('the immediate number has invalid sign')

        max_val = 0
        min_val = 0
        if signed == self.IMM_SIGNED:
            max_val = ((2**(bits-1))-1)
            min_val = (-(2**(bits-1)))
        elif signed == self.IMM_UNSIGNED:
            max_val = ((2**bits)-1)
            min_val = 0
        else: # can be signed or unsigned depends on the sign bit
            max_val = ((2**bits)-1)
            min_val = (-(2**(bits-1)))
        
        if val < min_val or val > max_val:
            raise ValueError('the immediate number is out of range [%d : %d]' % (min_val, max_val))

    def parse_op_jump(self, operand):
        if len(operand) != 1:
            raise ValueError('instruction operand length not equal to 1')

        dst = operand[0]
        self.imm_validate(int(dst[1:]), 24, self.IMM_SIGNED)

        imm = 0

        if '-' in dst:
            imm += (0x1000000 - int(dst[2:]))
        else:
            imm += int(dst[1:])

        return imm

    def parse_op_repeat(self, operand):
        if len(operand) != 3:
            raise ValueError('instruction operand length not equal to 3')

        loop_id = operand[0]
        self.imm_validate(int(loop_id[1:]), 1, self.IMM_UNSIGNED)
        loop_num = operand[1]
        self.imm_validate(int(loop_num[1:]), 16, self.IMM_UNSIGNED)
        offset = operand[2]
        self.imm_validate(int(offset[1:]), 5, self.IMM_UNSIGNED)

        imm = 0
        imm += (int(loop_id[1:])<<24)
        imm += (int(loop_num[1:])<<8)
        imm += (int(offset[1:]))

        return imm

    def parse_op_wait(self, operand):
        if len(operand) < 1:
            raise ValueError('instruction operand length error')
        imm = 0
        if '#' in operand[0]:
            self.imm_validate(int(operand[0][1:]), 26, self.IMM_UNSIGNED)
            imm += (int(operand[0][1:]))
            return imm

        for each in operand:
            if each not in self.operand_wait:
                if re.match('id([0-3]?[0-9]?)', each) != None:
                    imm += (int(each[2:])<<8)
                else:
                    print('********************************')
                    print('unrecognized operand: '+each+'\n')
                    print('supported operands for WAIT: ')
                    print(self.operand_wait.keys())
                    print('********************************\n')
                    raise ValueError('operand unrecognized')
            else:
                imm += (self.operand_wait[each])

        return imm

    def parse_op_cmp(self, operand):
        if len(operand) != 2:
            raise ValueError('instruction operand length not equal to 2')

        dst = operand[0]
        src = operand[1]

        imm = 0
        if '#' in src:
            self.imm_validate(int(src[1:]), 16, self.IMM_BOTH)
            imm += (1<<24)
            if '-' in src:
                imm += (0x10000 - int(src[2:]))
            else:
                imm += int(src[1:])
            if int(src[1:]) > 0x7FFF:
                imm += (0b1<<25)
        else:
            imm += (int(src[1:])<<8)
        imm += (int(dst[1:])<<16)

        return imm

    def parse_op_b(self, operand, cond, inst_label_list, index):
        if len(operand) != 1:
            raise ValueError('instruction operand length not equal to 1')

        dst = operand[0]

        imm = 0

        imm += (cond<<19)

        if dst.startswith('#'): 
            self.imm_validate(int(dst[1:]), 16, self.IMM_SIGNED)
            imm += (0b1 << 24) 
            if '-' in dst:
                imm += (0x10000 - int(dst[2:]))
            else:
                imm += int(dst[1:])
        elif re.match('r([0-3]?[0-9]?)', dst) != None:
            imm += (int(dst[1:])<<8)
            imm += (0b1<<23) # direct pc mode
        else:# label needs an offset
            imm += (1<<24)
            dst_pos = inst_label_list.find_label_pos(dst)
            offset = (dst_pos-index)
            if offset > 32767 or offset < -32768:
                raise ValueError('b instruction has an out range offset: ' + offset)
            if offset < 0:
                offset = 0x10000 + offset
            imm += offset

        return imm

    def parse_op_ldro(self, operand):
        if len(operand) != 3:
            raise ValueError('instruction operand length not equal to 3')

        dst = operand[0]
        src = operand[1]
        imm = operand[2]

        data = 0
        data += (int(dst[1:]) << 20)
        data += (int(src[1:]) << 15)

        if '#' in imm:
            self.imm_validate(int(imm[1:]), 15, self.IMM_SIGNED)
            if '-' in imm:
                data += (0x8000 - int(imm[2:]))
            else:
                data += int(imm[1:])
        else:
            raise ValueError('the immediate data format error')

        return data

    def parse_op_lea(self, operand):
        if len(operand) != 3:
            raise ValueError('instruction operand length not equal to 3')

        dst = operand[0]
        src = operand[1]
        imm = operand[2]

        data = 0
        data += (int(dst[1:]) << 21)
        data += (int(src[1:]) << 16)

        if '#' in imm:
            self.imm_validate(int(imm[1:]), 16, self.IMM_SIGNED)
            if '-' in imm:
                data += (0x10000 - int(imm[2:]))
            else:
                data += int(imm[1:])
        else:
            raise ValueError('the immediate data format error')

        return data

    def parse_op_ldr(self, operand):
        if len(operand) != 2:
            raise ValueError('instruction operand length not equal to 2')

        dst = operand[0]
        src = operand[1]

        imm = 0
        imm += (int(dst[1:])<<15)
        if '[' in src:
            src = src.replace('[','')
        if ']' in src:
            src = src.replace(']','')

        imm += (int(src[1:])<<8)

        return imm

    def parse_op_ldrb(self, operand):
        return (0b1<<25) + (0b10<<21) + self.parse_op_ldr(operand)

    def parse_op_ldrh(self, operand):
        return (0b1<<25) + (0b01<<21) + self.parse_op_ldr(operand)

    def parse_op_ldrsb(self, operand):
        return (0b10<<21) + self.parse_op_ldr(operand)

    def parse_op_ldrsh(self, operand):
        return (0b01<<21) + self.parse_op_ldr(operand)

    def parse_op_ldm(self, operand):
        reglist = []
        if '-' in operand[1]:
            reglist.append(1)
            regs = operand[1].split('-')
            operand[1] = regs[0]
            rng = int(regs[1][1:]) - int(regs[0][1:])
            if  rng> 7 or rng < 0:
                raise ValueError('reglist is invalid')
            for each in range(rng):
                reglist.append(1)
            for each in range(7-rng):
                reglist.append(0)
        else:
            reglist = [1,0,0,0,0,0,0,0]
            regs = operand[1:]
            base = int(regs[0][1:])
            for each in regs[1:]:
                if int(each[1:]) - base > 7 or int(each[1:]) - base < 0:
                    raise ValueError('reglist is invalid')
                else:
                    reglist[(int(each[1:]) - base)] = 1
        msk = 0b00000000
        for i in range(8):
            if reglist[i] == 0:
                msk = msk | (0b1<<i)
        operand = [operand[1], operand[0]]
        return (0b01<<23) + msk + self.parse_op_ldr(operand)

    def parse_op_pop(self, operand):
        if len(operand) != 1:
            raise ValueError('instruction operand length not equal to 1')

        operand.append('[r31]') # append [sp]
        if '-' in operand[0]:
            operand[0] = operand[0][:operand[0].find('-')]
            return (0b1<<24) + (0b01<<23) + self.parse_op_ldr(operand)
        else:
            return (0b1<<24) + self.parse_op_ldr(operand)

    def parse_op_stro(self, operand):
        return self.parse_op_ldro(operand)

    def parse_op_str(self, operand):
        return self.parse_op_ldr(operand)

    def parse_op_strb(self, operand):
        return self.parse_op_ldrb(operand)

    def parse_op_strh(self, operand):
        return self.parse_op_ldrh(operand)

    def parse_op_strsb(self, operand):
        return self.parse_op_ldrsb(operand)

    def parse_op_strsh(self, operand):
        return self.parse_op_ldrsh(operand)

    def parse_op_stm(self, operand):
        if '-' in operand[1]:
            regs = operand[1].split('-')
            operand[1] = regs[0]
        operand = [operand[1], operand[0]]    
        return (0b01<<23) + self.parse_op_str(operand)

    def parse_op_push(self, operand):
        if len(operand) != 1:
            raise ValueError('instruction operand length not equal to 1')
        
        operand.append('[r31]') # append [sp]
        if '-' in operand[0]:
            operand[0] = operand[0][:operand[0].find('-')]
            return (0b1<<24) + (0b01<<23) + self.parse_op_str(operand)
        else:
            return (0b1<<24) + self.parse_op_str(operand)

    def parse_op_setr(self, operand):
        if len(operand) != 3:
            raise ValueError('instruction operands not equal to 3')

        dst = operand[0]
        mod = operand[1]
        self.imm_validate(int(mod[1:]), 5, self.IMM_UNSIGNED)
        src = operand[2]
        self.imm_validate(int(src[1:]), 16, self.IMM_UNSIGNED)
        
        imm = 0
        imm += (int(dst[1:])<<16)
        imm += (int(mod[1:])<<21)
        imm += (int(src[1:]))

        return imm

    def parse_op_setrh(self, operand):
        mod = '#3' # 0b00011, only apply to 16 MSB, preserve the 16 LSB
        operand.insert(1, mod)
        return self.parse_op_setr(operand)

    def parse_op_setrl(self, operand):
        mod = '#12' # 0b01100, only apply to 16 LSB, preserve the 16 MSB
        operand.insert(1, mod)
        return self.parse_op_setr(operand)

    def parse_op_seti(self, operand):
        if len(operand) != 3:
            raise ValueError('instruction operands not equal to 3')

        dst = operand[0]
        mod = operand[1]
        self.imm_validate(int(mod[1:]), 1, self.IMM_UNSIGNED)
        src = operand[2]
        self.imm_validate(int(src[1:]), 16, self.IMM_UNSIGNED)
        
        imm = 0
        imm += (int(dst[1:])<<16)
        imm += (int(mod[1:])<<24)
        imm += (int(src[1:]))

        return imm

    def parse_op_setih(self, operand):
        mod = '#1' # only apply to 16 MSB, preserve the 16 LSB
        operand.insert(1, mod)
        return self.parse_op_seti(operand)

    def parse_op_setil(self, operand):
        mod = '#0' # only apply to 16 LSB, preserve the 16 MSB
        operand.insert(1, mod)
        return self.parse_op_seti(operand)

    def parse_op_gopr(self, operand):
        if len(operand) != 3:
            raise ValueError('instruction operands not equal to 3')

        mod = operand[0]
        self.imm_validate(int(mod[1:]), 3, self.IMM_UNSIGNED)
        dst = operand[1]
        src = operand[2]

        imm = 0
        imm += (int(mod[1:])<<21)
        imm += (int(dst[1:])<<16)

        if '#' in src:
            self.imm_validate(int(src[1:]), 16, self.IMM_BOTH)
            imm += (0b1 << 24) 
            if '-' in src:
                imm += (0x10000 - int(src[2:]))
            else:
                imm += int(src[1:])
            if int(src[1:]) > 0x7FFF:
                imm += (0b1<<25)
        else:
            imm += (int(src[1:])<<8)

        return imm

    def parse_op_add(self, operand):
        return self.parse_op_gopr(operand)

    def parse_op_sub(self, operand):
        return self.parse_op_gopr(operand)

    def parse_op_and(self, operand):
        if len(operand) != 2:
            raise ValueError('instruction operands not equal to 2')

        dst = operand[0]
        src = operand[1]

        imm = 0
        imm += (int(dst[1:])<<16)

        imm += (0b1<<25) # bit 25 reserved 1 for AND and ORR

        if '#' in src:
            self.imm_validate(int(src[1:]), 16, self.IMM_UNSIGNED)
            imm += (0b1 << 24) 
            imm += int(src[1:])
        else:
            imm += (int(src[1:])<<8)

        return imm

    def parse_op_not(self, operand):
        if len(operand) != 2:
            raise ValueError('instruction operands not equal to 2')

        dst = operand[0]
        src = operand[1]

        imm = 0
        imm += (int(dst[1:])<<16)

        if '#' in src:
            self.imm_validate(int(src[1:]), 16, self.IMM_UNSIGNED)
            imm += (0b1 << 24)
            imm += int(src[1:])
        else:
            imm += (int(src[1:])<<8)

        return imm

    def parse_op_orr(self, operand):
        return self.parse_op_and(operand)

    def parse_op_xor(self, operand):
        return self.parse_op_not(operand)

    def parse_op_lsr(self, operand):
        if len(operand) != 2:
            raise ValueError('instruction operands not equal to 2')

        dst = operand[0]
        src = operand[1]

        imm = 0
        imm += (int(dst[1:])<<16)

        if '#' in src:
            self.imm_validate(int(src[1:]), 5, self.IMM_UNSIGNED)
            imm += (0b1 << 24) 
            imm += int(src[1:])
        else:
            imm += (int(src[1:])<<8)

        return imm

    def parse_op_asr(self, operand):
        return (0b1<<25) + self.parse_op_lsr(operand)

    def parse_op_lsl(self, operand):
        return self.parse_op_lsr(operand)

    def parse_op_mul(self, operand):
        if len(operand) != 2:
            raise ValueError('instruction operands not equal to 2')

        dst = operand[0]
        src = operand[1]


        imm = 0
        imm += (int(dst[1:])<<16)

        imm += (int(src[1:])<<8)

        return imm

    def parse_op_mov(self, operand):
        if len(operand) != 2:
            raise ValueError('instruction operands not equal to 2')

        dst = operand[0]
        src = operand[1]

        imm = 0
        imm += (int(dst[1:])<<16)

        if '#' in src:
            self.imm_validate(int(src[1:]), 16, self.IMM_BOTH)
            imm += (0b1 << 24) 
            if '-' in src:
                imm += (0x10000 - int(src[2:]))
            else:
                imm += int(src[1:])
            if int(src[1:]) > 0x7FFF:
                imm += (0b1<<25)                
        else:
            imm += (0b1 << 25)
            imm += (int(src[1:])<<8)

        return imm

    def parse_op_move(self, operand, cond):
        if len(operand) != 2:
            raise ValueError('instruction operands not equal to 2')

        dst = operand[0]
        src = operand[1]

        imm = 0
        imm += (cond << 22)

        imm += (int(dst[1:])<<16)

        if '#' in src:
            self.imm_validate(int(src[1:]), 16, self.IMM_BOTH)
            imm += (0b1 << 24)
            if '-' in src:
                imm += (0x10000 - int(src[2:]))
            else:
                imm += int(src[1:])
            if int(src[1:]) > 0x7FFF:
                imm += (0b1<<25)
        else:
            imm += (0b1 << 25)
            imm += (int(src[1:])<<8)

        return imm

    def parse_op(self, op_code, operand, inst_label_list, index):
        """
        process the op code and operand 
        """
        code = 0
        if op_code in self.instruction_dict:
            code = (self.instruction_dict[op_code]<<26)

        if op_code == 'jump':
            code += self.parse_op_jump(operand)
        if op_code == 'repeat':
            code += self.parse_op_repeat(operand)
        if op_code == 'wait':
            code += self.parse_op_wait(operand)
        if op_code == 'cmp':
            code += self.parse_op_cmp(operand)
        if op_code == 'b' or op_code == 'bl' or op_code == 'bx' or op_code == 'beq' or op_code == 'bgt' or op_code == 'blt' or op_code == 'bne' or op_code == 'ble' or op_code == 'bge':
            cond = 0b110
            if op_code == 'bgt':
                cond = 0b000
            if op_code == 'beq':
                cond = 0b010
            if op_code == 'blt':
                cond = 0b100
            if op_code == 'bne':
                cond = 0b011
            if op_code == 'ble':
                cond = 0b001
            if op_code == 'bge':
                cond = 0b101

            if op_code == 'bl': # branch with LR updated
                code += (0b1<<22)
            code += self.parse_op_b(operand, cond, inst_label_list, index)
        if op_code == 'ldro':
            code += self.parse_op_ldro(operand)
        if op_code == 'ldr':
            code += self.parse_op_ldr(operand)
        if op_code == 'ldrb':
            code += self.parse_op_ldrb(operand)
        if op_code == 'ldrh':
            code += self.parse_op_ldrh(operand)
        if op_code == 'ldrsb':
            code += self.parse_op_ldrsb(operand)
        if op_code == 'ldrsh':
            code += self.parse_op_ldrsh(operand)
        if op_code == 'ldm':
            code += self.parse_op_ldm(operand)
        if op_code == 'pop':
            code += self.parse_op_pop(operand)
        if op_code == 'lea':
            code += self.parse_op_lea(operand)
        if op_code == 'str':
            code += self.parse_op_str(operand)
        if op_code == 'stro':
            code += self.parse_op_stro(operand)
        if op_code == 'strb':
            code += self.parse_op_strb(operand)
        if op_code == 'strh':
            code += self.parse_op_strh(operand)
        if op_code == 'strsb':
            code += self.parse_op_strsb(operand)
        if op_code == 'stm':
            code += self.parse_op_stm(operand)
        if op_code == 'strsh':
            code += self.parse_op_strsh(operand)
        if op_code == 'push':
            code += self.parse_op_push(operand)
        if op_code == 'setr':
            code += self.parse_op_setr(operand)
        if op_code == 'setrh':
            code += self.parse_op_setrh(operand)
        if op_code == 'setrl':
            code += self.parse_op_setrl(operand)
        if op_code == 'seti':
            code += self.parse_op_seti(operand)
        if op_code == 'setih':
            code += self.parse_op_setih(operand)
        if op_code == 'setil':
            code += self.parse_op_setil(operand)
        if op_code == 'gopr':
            code += self.parse_op_gopr(operand)
        if op_code == 'add' or op_code == 'addm' or op_code == 'addl':
            mod = ''
            if op_code == 'addl':
                mod = '#2' # 0b010, only apply to 16 LSB
            if op_code == 'addm':
                mod = '#1' # 0b001, only apply to 16 MSB
            if op_code == 'add':
                mod = '#0' # 0b000, immediate with signed extended & apply to the word  
            operand.insert(0, mod)  
            code += self.parse_op_add(operand)
        if op_code == 'sub' or op_code == 'subm' or op_code == 'subl':
            mod = ''
            if op_code == 'subl':
                mod = '#6' # 0b110, only apply to 16 LSB
            if op_code == 'subm':
                mod = '#5' # 0b101, only apply to 16 MSB
            if op_code == 'sub':
                mod = '#4' # 0b100, immediate with signed extended & apply to the word      
            operand.insert(0, mod)  
            code += self.parse_op_sub(operand)
        if op_code == 'and' or op_code == 'andm' or op_code == 'andl':
            if op_code == 'andl':
                code += (0b10<<21) # only apply to 16 LSB
            if op_code == 'andm':
                code += (0b01<<21) # only apply to 16 MSB
            if op_code == 'and':
                code += (0b00<<21) # immediate with 0 extended & apply to the word     
            code += self.parse_op_and(operand)
        if op_code == 'not' or op_code == 'notm' or op_code == 'notl':
            if op_code == 'notl':
                code += (0b10<<21) # only apply to 16 LSB
            if op_code == 'notm':
                code += (0b01<<21) # only apply to 16 MSB
            if op_code == 'not':
                code += (0b00<<21) # immediate with 0 extended & apply to the word
            code += self.parse_op_not(operand)
        if op_code == 'orr' or op_code == 'orrm' or op_code == 'orrl':
            if op_code == 'orrl':
                code += (0b10<<21) # only apply to 16 LSB
            if op_code == 'orrm':
                code += (0b01<<21) # only apply to 16 MSB
            if op_code == 'orr':
                code += (0b00<<21) # immediate with 0 extended & apply to the word     
            code += self.parse_op_orr(operand)
        if op_code == 'xor' or op_code == 'xorm' or op_code == 'xorl':
            if op_code == 'xorl':
                code += (0b10<<21) # only apply to 16 LSB
            if op_code == 'xorm':
                code += (0b01<<21) # only apply to 16 MSB
            if op_code == 'xor':
                code += (0b00<<21) # immediate with 0 extended & apply to the word
            code += self.parse_op_xor(operand)
        if op_code == 'lsl':
            code += self.parse_op_lsl(operand)
        if op_code == 'lsr':
            code += self.parse_op_lsr(operand)
        if op_code == 'asr':
            code += self.parse_op_asr(operand)
        if op_code == 'mul' or op_code == 'muls' or op_code == 'mulsb' or op_code == 'mulb' or op_code == 'mulshl' or op_code == 'mulhl' or op_code == 'mulshm' or op_code == 'mulhm':
            if op_code == 'mul':
                code += (0b100 << 21)
            if op_code == 'muls':
                pass
            if op_code == 'mulsb':
                code += (0b010 << 21)
            if op_code == 'mulb':
                code += (0b110 << 21)
            if op_code == 'mulshl':
                code += (0b001 << 21)
            if op_code == 'mulhl':
                code += (0b101 << 21)
            if op_code == 'mulshm':
                code += (0b011 << 21)
            if op_code == 'mulhm':
                code += (0b111 << 21)
            code += self.parse_op_mul(operand)
        if op_code == 'mov' or op_code == 'movb' or op_code == 'movh' or op_code == 'movl':
            if op_code == 'movb':
                code += (0b10<<21) # only apply to 8 LSB
            if op_code == 'movh':
                code += (0b11<<21) # only apply to 16 MSB
            if op_code == 'movl':
                code += (0b01<<21) # only apply to 16 LSB
            code += self.parse_op_mov(operand)
        if op_code == 'cmov' or op_code == 'cmoveq' or op_code == 'cmovgt' or op_code == 'cmovlt' or op_code == 'cmovne' or op_code == 'cmovle' or op_code == 'cmovge':
            cond = 0b110
            if op_code == 'cmovgt':
                cond = 0b000
            if op_code == 'cmoveq':
                cond = 0b010
            if op_code == 'cmovlt':
                cond = 0b100
            if op_code == 'cmovne':
                cond = 0b011
            if op_code == 'cmovle':
                cond = 0b001
            if op_code == 'cmovge':
                cond = 0b101
            code += self.parse_op_move(operand, cond)

        return code

    def parse_instruction(self, inst, inst_label_list, index):
        """
        convert to a 32 bit machine code 
        """
        operand = []
        inst = inst.replace('\t',' ')  
        index_op = inst.find(' ')
        op_code = inst[:index_op]
        tmp_operand = inst[index_op:]
        items = tmp_operand.split(',')
        
        if op_code not in self.instruction_dict:
            if self.inst_extension:
                if op_code not in self.inst_extension.instruction_dict:
                    raise ValueError('instruction op code not exist: '+ op_code)
            else:
                raise ValueError('instruction op code not exist: '+ op_code + '\n you may need to include an extension module')

        for each in items:
            each = (each.lstrip().rstrip())
            each = each.replace('{', '')
            each = each.replace('}', '')
            if each == 'sp':
                each = 'r31'
            if each == 'lr':
                each = 'r30'
            if each == 'pc':
                each = 'r29'
            if each == 'st':
                each = 'r28'
            if each.startswith('#'):
                if '0x' in each:
                    tmp = int(each[1:],16)
                    each = '#'+str(tmp)
                if '0b' in each:
                    tmp = int(each[1:],2)
                    each = '#'+str(tmp)
            operand.append(each)

        try:
            if op_code in self.instruction_dict:
                code = self.parse_op(op_code, operand, inst_label_list, index)
            else:
                if self.inst_extension:
                    code = self.inst_extension.parse_op(op_code, operand, inst_label_list, index)
                else:
                    raise ValueError('the extension module was not loaded properly')
        except:
            raise ValueError('parse_op error with: '+op_code+', '+str(operand)+', '+str(index))
        
        if code >= 0x100000000:
            raise ValueError('parsed instruction code - '+str(code)+' is out of range: '+op_code+', '+str(operand)+', '+str(index))
        
        code_str = '0x{:08x}'.format(code)
        return code_str

    def strip_content(self, content):
        """
        strip out the unrelated content
        """
        index_start = content.find('/*')
        while index_start>=0:
            index_end = content.find('*/')
            if index_end < 0:
                raise ValueError('no matched */ found')
            replace_str = content[index_start:index_end+2]
            content = content.replace(replace_str, '')

            index_start = content.find('/*')

        buf = io.StringIO(content)
        tmp_content = ''
        line = buf.readline()
        while line != '':
            tmp_line = line.lstrip()

            if '//' in tmp_line:
                tmp_line = tmp_line[:tmp_line.find('//')]+'\n'

            if tmp_line.startswith('.'):
                tmp_content += ''
            else:
                if tmp_line != '' and tmp_line != '\n':
                    tmp_content += tmp_line
            line = buf.readline()

        return tmp_content

    def merge_instruction(self, inst_list):
        """
        merge the consecutive instructions into a single one if applicable  
        """    
        instruction_list = InstFuncLabel()

        index = 0
        while index < inst_list.length():
            inst = inst_list.list_inst[index]
            label = inst_list.list_label[index]
            
            #operand = []
            inst = inst.replace('\t',' ')  
            index_op = inst.find(' ')
            if index_op < 0:
                op_code = inst
                operand = ''
            else:
                op_code = inst[:index_op]
                operand = inst[index_op:]

            tmp_index = index 
            if self.inst_extension:  
                if op_code in self.inst_extension.instruction_dict_merge:
                    tmp_index = index+1
                    while tmp_index < inst_list.length():
                        tmp_inst = inst_list.list_inst[tmp_index]
                        tmp_inst = tmp_inst.replace('\t',' ')  
                        tmp_index_op = tmp_inst.find(' ')
                        tmp_op_code = tmp_inst[:tmp_index_op]
                        tmp_operand = tmp_inst[tmp_index_op:]
                        if self.inst_extension.merge(op_code, operand, tmp_op_code, tmp_operand):
                            operand += (',' + tmp_operand)
                            tmp_index += 1
                        else:
                            break
                else:
                    tmp_index += 1
            else:
                tmp_index += 1

            inst = op_code + ' ' + operand
            instruction_list.add(inst, label)
            index = tmp_index

        return instruction_list

    def validate_instruction(self, inst_list):
        label_list = inst_list.list_label
        # print(label_list)
        stripped_list = list(filter(None,label_list))
        # print(stripped_list)
        no_duplicated_list = list(set(stripped_list))
        # print(no_duplicated_list)   

        if len(stripped_list) != len(no_duplicated_list):
            for each in no_duplicated_list:
                stripped_list.remove(each)

            print('********************************')
            print("found duplicated labels: " + str(stripped_list))
            print('********************************\n')
            return False

        return True


    def syntax_to_instruction(self, content, hex_file, c_file, h_file):
        """
        convert the syntax to detailed instruction 
        """
        buf = io.StringIO(content)
        tmp_content = ''
        instruction_list = InstFuncLabel()

        line = buf.readline()
        label = ''
        while line != '':

            tmp_line = line.lstrip()
            tmp_line = tmp_line.rstrip()
            # function or label
            if tmp_line.endswith(':'):
                label = tmp_line[0:-1]
                if ' ' in label:
                    raise ValueError('invalid label with space in "'+label+'"')
            else:
                # change to lower case
                tmp_line = tmp_line.lower()
                instruction_list.add(tmp_line, label)
                label = ''

            line = buf.readline()

        # check the validity of instructions
        if not self.validate_instruction(instruction_list):
            raise ValueError('invalid instruction set')

        # merge the consecutive ones
        instruction_list = self.merge_instruction(instruction_list)

        for i in range(instruction_list.length()):
            inst = instruction_list.list_inst[i]
            label = instruction_list.list_label[i]
            if label.startswith('__'):
                tmp_content += '                 // '+label+':\n'
            elif label != '':
                    tmp_content += ('};\n\n')
                    tmp_content += ('const uint32_t '+label+'[] = {\n')
                    # save into the .h file
                    if h_file:
                        h_file.write('extern const uint32_t '+label+'[];\n')

            code_str = self.parse_instruction(inst, instruction_list, i)
            tmp_content += ('    '+code_str+',' + '  //     ' + inst+'\n')
            # save into the hex file
            if hex_file:
                hex_file.write(code_str[2:]+'\n')
            
        tmp_content += ('};\n\n')

        tmp_content = tmp_content.replace('};', '', 1)
        # save into the .c file
        if c_file:
            c_file.write(tmp_content)


def read_from_file(file_path):
    file_path = os.path.abspath(file_path)
    f = open(file_path, 'r')
    s = f.read()
    return (s)

def parse_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-i', type=str, required=True,
                            help='path to input file or a file list separated by commas.')
    arg_parser.add_argument('-o', type=str, default=argparse.SUPPRESS,
                            help='path to output file.')
    arg_parser.add_argument('-f', type=str, default=argparse.SUPPRESS,
                            help='specified output format. Can be [ hex / c / h ] or any combination of the three(separated by commas). Default with .c & .h files output.')
    args = vars(arg_parser.parse_args())
    return args

if __name__ == "__main__":
    args = {}
    args["i"] = "luna_repeat.s"
    args["o"] = "luna_repeat"
    input = args['i']
    formats = {'hex':0, 'h':0, 'c':0}
    h_file = None
    c_file = None
    hex_file = None

    inst_parser = InstructionParser(True)

    if 'o' in args:
        output = args['o']
    else:
        if input.find('.'):
            output = input[:input.find('.')]
        else:
            output = input

    if 'f' in args:
        ls = args['f'].split(',')
        for each in ls:
            if each in formats:
                formats[each] = 1
    else:
        formats['h'] = 1
        formats['c'] = 1

    if formats['h']:
        h_file = open(output+'.h', 'w')
    if formats['c']:
        c_file = open(output+'.c', 'w')
    if formats['hex']:
        hex_file = open(output+'.hex', 'w')

    # add a prefix to head file
    if formats['h']:
        for each in prefix_h:
            h_file.write(each)

    # add a prefix to c file
    if formats['c']:
        for each in prefix_c:
            c_file.write(each)

    # add a prefix to hex format file
    if formats['hex']:
        for each in prefix_hex:
            if each.startswith('0x'):
                hex_file.write(each[2:]+'\n')
            else:
                each = each.lower()
                hex_file.write(inst_parser.parse_instruction(each, [], 0)[2:]+'\n')

    if '*.s' in args['i']:
        inputs = glob.glob('*.s')
    else:
        inputs = args['i'].split(',')

    print("The following files will be parsed: " + str(inputs))

    for each in inputs:
        content = read_from_file(each)
        content_stripped = inst_parser.strip_content(content)
        inst_parser.syntax_to_instruction(content_stripped, hex_file, c_file, h_file)

    # add a suffix to head file
    if formats['h']:
        for each in suffix_h:
            h_file.write(each)

    # add a suffix to c file
    if formats['c']:
        for each in suffix_c:
            c_file.write(each)

    # add a suffix to hex file
    if formats['hex']:
        for each in suffix_hex:
            if each.startswith('0x'):
                hex_file.write(each[2:]+'\n')
            else:
                each = each.lower()
                hex_file.write(inst_parser.parse_instruction(each, [], 0)[2:]+'\n')

    if formats['hex']:
        hex_file.close()
        print('--- '+output+'.hex generated')
    if formats['c']:
        c_file.close()
        print('--- '+output+'.c generated')
    if formats['h']:
        h_file.close()
        print('--- '+output+'.h generated')


