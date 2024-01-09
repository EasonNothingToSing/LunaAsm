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


class InstructionExtension(object):
    instruction_dict = {
        'memc': 0b100001,
        'mnts': 0b100010,
        'dstm0': 0b100101,
        'dstm1': 0b100111,
        'dstm2': 0b101000,
        'ares': 0b100100,
        'iow': 0b101001,
        'dprc': 0b100110,
        'rst': 0b111000,
        'init': 0b111100,
        'smrk': 0b101010,
        'cmrk': 0b101011,
        'macro': 0b011010,
    }
    instruction_dict_merge = {
        # instructions below may have consecutive ones which require merging before parsing
        'dstm0': 0b100101,
        'dstm1': 0b100111,
        'dstm2': 0b101000,
        'ares': 0b100100,
    }

    operand_memc_vals = {
        'one': 0,
        'total': 1,
        'ahb': 0,
        'luna': 1,
        'reg': 1,
    }

    operand_memc_params = [
        # parameters in op without '='
        {
        },
        # parameters in op with '='
        {
            'mode': {'bit': 25, 'val': operand_memc_vals},
            'addr': {'bit': 24, 'val': operand_memc_vals},
            'one-enable': {'bit': 23, 'val': operand_memc_vals},
            'dynamic': {'bit': 22, 'val': operand_memc_vals},
            'access': {'bit': 21, 'val': operand_memc_vals},
            'grp5': {'bit': 17, 'val': operand_memc_vals},
            'grp4': {'bit': 16, 'val': operand_memc_vals},
            'grp3': {'bit': 15, 'val': operand_memc_vals},
            'grp2': {'bit': 14, 'val': operand_memc_vals},
            'grp1': {'bit': 13, 'val': operand_memc_vals},
            'grp0': {'bit': 12, 'val': operand_memc_vals},
            'grp': {'bit': 8, 'val': operand_memc_vals},

            'bsel': {'bit': 0, 'val': operand_memc_vals},
        }
    ]

    operand_mnts_vals = {
        'mas0-0': 0,
        'mas0-1': 1,
        'mas0-2': 2,
        'mas1-0': 3,
        'mas1-1': 4,
        'mas1-2': 5,
        'slv0': 6,
        'slv1': 7,
        'pe': 8,
        'io-rd0': 9,
        'io-rd1': 10,
        'io-wr': 11,
        'io-ahb': 12,
        'p-rd0': 13,
        'p-rd1': 14,
        'p-wr': 15,
        'grp0': 16,
        'grp1': 17,
        'grp2': 18,
        'grp3': 19,
        'grp4': 20,
        'grp5': 21,
        'grp6': 22,
        'grp7': 23,
        'cos': 24,
        'sigmoid': 25,
        'tanh': 26,

    }

    operand_mnts_para_val = {
        'm0l': 1,
        'iord0': 1,
        'iowrl': 1,
        'm0p0': 1,
        'prd0': 1,
        'm0h': 2,
        'iord1': 2,
        'iowrh': 2,
        'm0p1': 2,
        'prd1': 2,
        'm1l': 3,
        'ioahb': 3,
        'iowr': 3,
        'm1p0': 3,
        'm1h': 4,
        'cosl': 4,
        'm1p1': 4,
        's0': 5,
        'cosh': 5,
        's1': 6,
        'r8': 6,
        'pe': 7,
        'r8r9': 7,
        'sigmoid': 8,
        'grp0': 8,
        'm0p0_0': 8,
        's0_0': 8,
        'tanh': 9,
        'grp1': 9,
        'm0p0_1': 9,
        's0_1': 9,
        'grp2': 10,
        'm0p0_2': 10,
        's0_2': 10,
        'grp3': 11,
        'm0p0_3': 11,
        's0_3': 11,
        'grp4': 12,
        'm0p0_4': 12,
        's0_4': 12,
        'grp5': 13,
        'm0p0_5': 13,
        's0_5': 13,
        'grp6': 14,
        'm0p0_6': 14,
        's0_6': 14,
        'grp7': 15,
        'm0p0_7': 15,
        's0_7': 15,
        'm0p1_0': 16,
        's1_0': 16,
        'm0p1_1': 17,
        's1_1': 17,
        'm0p1_2': 18,
        's1_2': 18,
        'm0p1_3': 19,
        's1_3': 19,
        'm0p1_4': 20,
        's1_4': 20,
        'm0p1_5': 21,
        's1_5': 21,
        'm0p1_6': 22,
        's1_6': 22,
        'm0p1_7': 23,
        's1_7': 23,
        'm1p0_0': 24,
        'm1p0_1': 25,
        'm1p0_2': 26,
        'm1p0_3': 27,
        'm1p0_4': 28,
        'm1p0_5': 29,
        'm1p0_6': 30,
        'm1p0_7': 31,
        'm1p1_0': 32,
        'm1p1_1': 33,
        'm1p1_2': 34,
        'm1p1_3': 35,
        'm1p1_4': 36,
        'm1p1_5': 37,
        'm1p1_6': 38,
        'm1p1_7': 39,
    }

    operand_mnts_mode_val = {
        'two_mode': 1,
        'four_mode': 2,
    }

    operand_mnts_params = [
        # parameters in op without '='
        {

        },
        # parameters in op with '='
        {
            'sel': {'bit': 21, 'val': operand_mnts_vals},

            'din': {'bit': 0, 'val': operand_mnts_para_val},
            'mode0': {'bit': 3, 'val': operand_mnts_mode_val},
            'mode1': {'bit': 5, 'val': operand_mnts_mode_val},
            'sync': {'bit': 7, 'val': operand_mnts_para_val},

            'p0-iodat': {'bit': 0, 'val': operand_mnts_para_val},
            'p0-lmdat0': {'bit': 4, 'val': operand_mnts_para_val},
            'p0-lmdat1': {'bit': 8, 'val': operand_mnts_para_val},
            'p0-lmdat2': {'bit': 12, 'val': operand_mnts_para_val},
            'p0-lmdat3': {'bit': 16, 'val': operand_mnts_para_val},

            'p1-iodat': {'bit': 0, 'val': operand_mnts_para_val},
            'p1-lmdat0': {'bit': 4, 'val': operand_mnts_para_val},
            'p1-lmdat1': {'bit': 8, 'val': operand_mnts_para_val},
            'p1-lmdat2': {'bit': 12, 'val': operand_mnts_para_val},
            'p1-lmdat3': {'bit': 16, 'val': operand_mnts_para_val},

            'mode': {'bit': 3, 'val': operand_mnts_mode_val},

            'row': {'bit': 0, 'val': operand_mnts_para_val},
            'col': {'bit': 4, 'val': operand_mnts_para_val},
            'overcheck': {'bit': 20, 'val': operand_mnts_para_val},

            'inside': {'bit': 0, 'val': operand_mnts_para_val},
            'outside': {'bit': 3, 'val': operand_mnts_para_val},

            'rd': {'bit': 0, 'val': operand_mnts_para_val},
            'wr': {'bit': 0, 'val': operand_mnts_para_val},

            'lmrd': {'bit': 0, 'val': operand_mnts_para_val},
            'lmwr': {'bit': 6, 'val': operand_mnts_para_val},

        }
    ]

    operand_ares_mode = {
        'master': 0,
    }

    operand_ares_select = {
        'select0': 0,
        'select1': 1,
        'select2': 2,
        'select3': 3,
    }

    operand_ares_params = [
        # master0 select0
        {
            'chs': {'bit': 16, 'val': None},
            'crs': {'bit': 14, 'val': None},
            'cmc': {'bit': 8, 'val': None},
            'ces': {'bit': 0, 'val': None},
        },

        # master0 select1
        {
            'hes': {'bit': 19, 'val': None},
            'elc': {'bit': 18, 'val': None},
            'efos': {'bit': 16, 'val': None},
            'els': {'bit': 14, 'val': None},
            'elf': {'bit': 8, 'val': None},
            'efcs': {'bit': 0, 'val': None},
        },

        # master0 select2
        {
            'aps': {'bit': 19, 'val': None},
            'hlcs': {'bit': 18, 'val': None},
            'mos': {'bit': 14, 'val': None},
            'eac': {'bit': 8, 'val': None},
            'cas': {'bit': 0, 'val': None},
        },

        # master0 select3
        {
            'rcils': {'bit': 16, 'val': None},
            'rcls': {'bit': 14, 'val': None},
            'dsc': {'bit': 8, 'val': None},
        }
    ]

    operand_mntx_vals = {
        'iord0': 1,
        'iord1': 2,
        'iowr': 3,
        'io': 0,
        'lut': 1,

    }

    operand_mntx_params = [
        # parameters in op without '='
        {
            'slv': {'bit': 21, 'val': 0b00000},
            'pe': {'bit': 21, 'val': 0b00001},
            'sync': {'bit': 21, 'val': 0b01000},
            'master': {'bit': 21, 'val': 0b10000},
            'lmgrp': {'bit': 21, 'val': 0b10001},
            'iolut': {'bit': 21, 'val': 0b10010},
            'port': {'bit': 21, 'val': 0b10011},
            'mode': {'bit': 21, 'val': 0b11000},
        },
        # parameters in op with '='
        {
            'tanh': {'bit': 18, 'val': operand_mntx_vals},
            'sigm': {'bit': 15, 'val': operand_mntx_vals},
            'iowr': {'bit': 12, 'val': operand_mntx_vals},
            'slv1': {'bit': 9, 'val': operand_mntx_vals},
            'slv0': {'bit': 6, 'val': operand_mntx_vals},
            'mas1': {'bit': 3, 'val': operand_mntx_vals},
            'mas0': {'bit': 0, 'val': operand_mntx_vals},
            'pe': {'bit': 12, 'val': operand_mntx_vals},

            'overcheck': {'bit': 20, 'val': operand_mntx_vals},
            'col': {'bit': 4, 'val': operand_mntx_vals},
            'row': {'bit': 0, 'val': operand_mntx_vals},

            'msel': {'bit': 19, 'val': operand_mntx_vals},
            'sel': {'bit': 18, 'val': operand_mntx_vals},
            'iodat': {'bit': 16, 'val': operand_mntx_vals},
            'lmdat3': {'bit': 12, 'val': operand_mntx_vals},
            'lmdat2': {'bit': 8, 'val': operand_mntx_vals},
            'lmdat1': {'bit': 4, 'val': operand_mntx_vals},
            'lmdat0': {'bit': 0, 'val': operand_mntx_vals},

            'grp135w': {'bit': 14, 'val': operand_mntx_vals},
            'grp135r': {'bit': 9, 'val': operand_mntx_vals},
            'grp024w': {'bit': 5, 'val': operand_mntx_vals},
            'grp024r': {'bit': 0, 'val': operand_mntx_vals},

            'ord1': {'bit': 13, 'val': operand_mntx_vals},
            'ord0': {'bit': 9, 'val': operand_mntx_vals},
            'iahb': {'bit': 6, 'val': operand_mntx_vals},
            'ird1': {'bit': 3, 'val': operand_mntx_vals},
            'ird0': {'bit': 0, 'val': operand_mntx_vals},

            'wr': {'bit': 6, 'val': operand_mntx_vals},
            'rd1': {'bit': 3, 'val': operand_mntx_vals},
            'rd0': {'bit': 0, 'val': operand_mntx_vals},

            'm1p1': {'bit': 15, 'val': operand_mntx_vals},
            'm1p0': {'bit': 12, 'val': operand_mntx_vals},
            'm0p1': {'bit': 3, 'val': operand_mntx_vals},
            'm0p0': {'bit': 0, 'val': operand_mntx_vals},
        }
    ]

    operand_dstm0_vals = {

        # master
        'bypass': 0b00,
        'constant': 0b01,
        'ioready': 0b10,

        # slave
        'normal': 0b00,
        'copy': 0b01,
        'rotate': 0b10,
        'fft': 0b11,

        '64bit': 0b00,
        '128bit': 0b01,
        '256bit': 0b10,
        '512bit': 0b11,
    }

    operand_dstm0_params = [
        # parameters in op without '='
        {
            'master0': {'bit': 24, 'val': 0},
            'master1': {'bit': 24, 'val': 1},
            'slave0': {'bit': 24, 'val': 2},
            'slave1': {'bit': 24, 'val': 3},

            'config0': {'bit': 23, 'val': 0},
            'config1': {'bit': 23, 'val': 1},
        },

        # parameters in op with '='
        {
            # master
            'enable': {'bit': 21, 'val': operand_dstm0_vals},
            'hold': {'bit': 14, 'val': operand_dstm0_vals},

            'w-hold': {'bit': 11, 'val': operand_dstm0_vals},
            'h-hold': {'bit': 12, 'val': operand_dstm0_vals},
            'c-hold': {'bit': 13, 'val': operand_dstm0_vals},
            's-hold': {'bit': 8, 'val': operand_dstm0_vals},
            't-hold': {'bit': 9, 'val': operand_dstm0_vals},
            'r-hold': {'bit': 10, 'val': operand_dstm0_vals},
            'i-hold': {'bit': 8, 'val': operand_dstm0_vals},
            'j-hold': {'bit': 9, 'val': operand_dstm0_vals},
            'k-hold': {'bit': 10, 'val': operand_dstm0_vals},
            'x-hold': {'bit': 11, 'val': operand_dstm0_vals},
            'y-hold': {'bit': 12, 'val': operand_dstm0_vals},
            'z-hold': {'bit': 13, 'val': operand_dstm0_vals},

            'w-mode': {'bit': 5, 'val': operand_dstm0_vals},
            'h-mode': {'bit': 6, 'val': operand_dstm0_vals},
            'c-mode': {'bit': 7, 'val': operand_dstm0_vals},
            's-mode': {'bit': 2, 'val': operand_dstm0_vals},
            't-mode': {'bit': 3, 'val': operand_dstm0_vals},
            'r-mode': {'bit': 4, 'val': operand_dstm0_vals},
            'i-mode': {'bit': 2, 'val': operand_dstm0_vals},
            'j-mode': {'bit': 3, 'val': operand_dstm0_vals},
            'k-mode': {'bit': 4, 'val': operand_dstm0_vals},
            'x-mode': {'bit': 5, 'val': operand_dstm0_vals},
            'y-mode': {'bit': 6, 'val': operand_dstm0_vals},
            'z-mode': {'bit': 7, 'val': operand_dstm0_vals},

            'w-input': {'bit': 1, 'val': operand_dstm0_vals},
            'h-input': {'bit': 1, 'val': operand_dstm0_vals},
            'c-input': {'bit': 1, 'val': operand_dstm0_vals},

            'j-input': {'bit': 0, 'val': operand_dstm0_vals},
            'k-input': {'bit': 0, 'val': operand_dstm0_vals},
            't-input': {'bit': 0, 'val': operand_dstm0_vals},
            'r-input': {'bit': 0, 'val': operand_dstm0_vals},

            'i-input': {'bit': 20, 'val': operand_dstm0_vals},
            's-input': {'bit': 20, 'val': operand_dstm0_vals},

            # slave
            'stride': {'bit': 15, 'val': operand_dstm0_vals},
            'max-pool': {'bit': 14, 'val': operand_dstm0_vals},
            'precision': {'bit': 12, 'val': operand_dstm0_vals},
            'blk': {'bit': 10, 'val': operand_dstm0_vals},
            'mode': {'bit': 8, 'val': operand_dstm0_vals},
            'outband': {'bit': 6, 'val': operand_dstm0_vals},
            'inband': {'bit': 4, 'val': operand_dstm0_vals},
            'format': {'bit': 3, 'val': operand_dstm0_vals},

            'filter': {'bit': 2, 'val': operand_dstm0_vals},

            'fft-mode': {'bit': 17, 'val': operand_dstm0_vals},
            'fft-st-cnt': {'bit': 19, 'val': operand_dstm0_vals},
            'fft-sc-out': {'bit': 22, 'val': operand_dstm0_vals},

        }

    ]

    operand_dstm1_vals = {

        's': 0,
        't': 1,
        'r': 2,
        'w': 3,
        'h': 4,
        'c': 5,
        'i': 6,
        'j': 7,
        'k': 1,

    }

    operand_dstm1_params = [
        # parameters in op without '='
        {
            'master0': {'bit': 24, 'val': 0},
            'master1': {'bit': 24, 'val': 1},
            'slave0': {'bit': 24, 'val': 2},
            'slave1': {'bit': 24, 'val': 3},

            'config0': {'bit': 23, 'val': 0},
            'config1': {'bit': 23, 'val': 1},
        },
        # parameters in op with '='
        {
            'source': {'bit': 20, 'val': operand_dstm1_vals},

            'addrm': {'bit': 18, 'val': operand_dstm1_vals},

            'k-enable': {'bit': 17, 'val': operand_dstm1_vals},
            'j-enable': {'bit': 16, 'val': operand_dstm1_vals},
            'i-enable': {'bit': 15, 'val': operand_dstm1_vals},
            'c-enable': {'bit': 14, 'val': operand_dstm1_vals},
            'h-enable': {'bit': 13, 'val': operand_dstm1_vals},
            'w-enable': {'bit': 12, 'val': operand_dstm1_vals},
            'r-enable': {'bit': 11, 'val': operand_dstm1_vals},
            't-enable': {'bit': 10, 'val': operand_dstm1_vals},
            's-enable': {'bit': 9, 'val': operand_dstm1_vals},

            'k-carry': {'bit': 8, 'val': operand_dstm1_vals},
            'j-carry': {'bit': 7, 'val': operand_dstm1_vals},
            'i-carry': {'bit': 6, 'val': operand_dstm1_vals},
            'c-carry': {'bit': 5, 'val': operand_dstm1_vals},
            'h-carry': {'bit': 4, 'val': operand_dstm1_vals},
            'w-carry': {'bit': 3, 'val': operand_dstm1_vals},
            'r-carry': {'bit': 2, 'val': operand_dstm1_vals},
            't-carry': {'bit': 1, 'val': operand_dstm1_vals},
            's-carry': {'bit': 0, 'val': operand_dstm1_vals},
        }

    ]

    operand_dstm2_vals = {

    }

    operand_dstm2_params = [
        # parameters in op without '='
        {
            'master0': {'bit': 24, 'val': 0},
            'master1': {'bit': 24, 'val': 1},
            'slave0': {'bit': 24, 'val': 2},
            'slave1': {'bit': 24, 'val': 3},
        },
        # parameters in op with '='
        {
            'datapath': {'bit': 20, 'val': operand_dstm2_vals},

            'dp-merge': {'bit': 18, 'val': operand_dstm2_vals},

            'k-r-carry': {'bit': 17, 'val': operand_dstm2_vals},
            'j-r-carry': {'bit': 16, 'val': operand_dstm2_vals},
            'i-r-carry': {'bit': 15, 'val': operand_dstm2_vals},
            'c-r-carry': {'bit': 14, 'val': operand_dstm2_vals},
            'h-r-carry': {'bit': 13, 'val': operand_dstm2_vals},
            'w-r-carry': {'bit': 12, 'val': operand_dstm2_vals},
            'r-r-carry': {'bit': 11, 'val': operand_dstm2_vals},
            't-r-carry': {'bit': 10, 'val': operand_dstm2_vals},
            's-r-carry': {'bit': 9, 'val': operand_dstm2_vals},

            'k-l-carry': {'bit': 8, 'val': operand_dstm2_vals},
            'j-l-carry': {'bit': 7, 'val': operand_dstm2_vals},
            'i-l-carry': {'bit': 6, 'val': operand_dstm2_vals},
            'c-l-carry': {'bit': 5, 'val': operand_dstm2_vals},
            'h-l-carry': {'bit': 4, 'val': operand_dstm2_vals},
            'w-l-carry': {'bit': 3, 'val': operand_dstm2_vals},
            'r-l-carry': {'bit': 2, 'val': operand_dstm2_vals},
            't-l-carry': {'bit': 1, 'val': operand_dstm2_vals},
            's-l-carry': {'bit': 0, 'val': operand_dstm2_vals},
        }

    ]

    operand_iow_vals = {

        '16bit': 0,
        '32bit': 1,
        '64bit': 2,
        '128bit': 3,
    }

    operand_iow_params = [
        # parameters in op without '='
        {

        },
        # parameters in op with '='
        {
            'bw': {'bit': 4, 'val': operand_iow_vals},
            'ch3': {'bit': 3, 'val': operand_iow_vals},
            'ch2': {'bit': 2, 'val': operand_iow_vals},
            'ch1': {'bit': 1, 'val': operand_iow_vals},
            'ch0': {'bit': 0, 'val': operand_iow_vals},
        }

    ]

    operand_dprc_vals = {

        'idle': 0,

        'l2': 1,
        'l3': 1,
        'l4': 2,
        'l5': 3,
        'l6': 3,

        '64bit': 0,
        '32bit': 1,
        '16bit': 2,
        '8bit': 3,

        '32-intg': 1,

        'sum': 0,
        'cat': 1,
    }

    operand_dprc_params = [
        # parameters in op without '='
        {

        },
        # parameters in op with '='
        {
            'outlayer': {'bit': 22, 'val': operand_dprc_vals},
            'comshift': {'bit': 20, 'val': operand_dprc_vals},
            'addtree': {'bit': 18, 'val': operand_dprc_vals},
            'intgnet': {'bit': 16, 'val': operand_dprc_vals},
            'sigma': {'bit': 14, 'val': operand_dprc_vals},
            'outlayer-mode': {'bit': 8, 'val': operand_dprc_vals},
            'intgnet-mode': {'bit': 4, 'val': operand_dprc_vals},
            'layer3-mode': {'bit': 2, 'val': operand_dprc_vals},
            'mmac1': {'bit': 1, 'val': operand_dprc_vals},
            'mmac0': {'bit': 0, 'val': operand_dprc_vals},
        }

    ]

    operand_rst_vals = {
        'clock': (0b00),
        'reset': (0b01),
        'counter': (0b11),

        'stop': (0b00),
        'start': (0b01),
        'refresh': (0b11),

    }

    operand_rst_params = [
        # parameters in op without '='
        {
            'master0': {'bit': 0, 'val': 1},
            'master1': {'bit': 1, 'val': 1},
            'slave0': {'bit': 2, 'val': 1},
            'slave1': {'bit': 3, 'val': 1},
            'iord0': {'bit': 4, 'val': 1},
            'iord1': {'bit': 5, 'val': 1},
            'iowr': {'bit': 6, 'val': 1},
            'psram': {'bit': 7, 'val': 1},
            'topctl': {'bit': 8, 'val': 1},
            'cgc': {'bit': 9, 'val': 1},
            'ahbins': {'bit': 10, 'val': 1},
            'ahbreg': {'bit': 11, 'val': 1},
            'ahbmux': {'bit': 12, 'val': 1},
            'pecore': {'bit': 13, 'val': 1},
            'router': {'bit': 14, 'val': 1},
            'regtab0': {'bit': 16, 'val': 1},
            'regtab1': {'bit': 17, 'val': 1},
            'regtab2': {'bit': 18, 'val': 1},
            'regtab3': {'bit': 19, 'val': 1},

            'stop': {'bit': 0, 'val': 0},
            'start': {'bit': 0, 'val': 1},
            'refresh': {'bit': 0, 'val': 3},

        },
        # parameters in op with '='
        {
            'sel': {'bit': 22, 'val': operand_rst_vals},

            'master0': {'bit': 0, 'val': operand_rst_vals},
            'master1': {'bit': 1, 'val': operand_rst_vals},
            'slave0': {'bit': 2, 'val': operand_rst_vals},
            'slave1': {'bit': 3, 'val': operand_rst_vals},
            'iord0': {'bit': 4, 'val': operand_rst_vals},
            'iord1': {'bit': 5, 'val': operand_rst_vals},
            'iowr': {'bit': 6, 'val': operand_rst_vals},
            'psram': {'bit': 7, 'val': operand_rst_vals},
            'pe0': {'bit': 8, 'val': operand_rst_vals},
            'pe1': {'bit': 9, 'val': operand_rst_vals},
            'pe2': {'bit': 10, 'val': operand_rst_vals},
            'pe3': {'bit': 11, 'val': operand_rst_vals},
            'pe4': {'bit': 12, 'val': operand_rst_vals},
            'pe5': {'bit': 13, 'val': operand_rst_vals},
            'pe6': {'bit': 14, 'val': operand_rst_vals},
            'pe7': {'bit': 15, 'val': operand_rst_vals},

            'lcnt': {'bit': 0, 'val': operand_rst_vals},
        }
    ]

    operand_init_vals = {
        'start-master0': 1,
        'start-master1': 2,
    }

    operand_smrk_vals = {
        'block': (0 << 4),
        'non-block': (1 << 4),
        'mark0': (1 << 0),
        'mark1': (1 << 1),
        'mark2': (1 << 2),
        'mark3': (1 << 3),
    }

    operand_cmrk_vals = {
        'mark0': (1 << 0),
        'mark1': (1 << 1),
        'mark2': (1 << 2),
        'mark3': (1 << 3),
    }

    operand_macro_vals = {

    }

    operand_macro_params = [
        # parameters in op without '='
        {

        },
        # parameters in op with '='
        {

        }
    ]

    def __init__(self):
        print("extension module - [InstructionExtension] loaded")

    def ares_started(self, operand):
        operand = operand.replace('\t', ' ').split(',')

        count = 0
        try:
            mode = operand[0].lstrip().rstrip()
            sel = operand[1].lstrip().rstrip()
        except IndexError:
            return -1

        # Mode
        params = mode.split('=')
        if params[0] != "mode":
            return -1

        if len(params) != 2:
            raise ValueError('invalid op: ' + mode)

        if params[1].isdecimal():
            count += int(params[1]) * 4
        else:
            count += int(self.operand_ares_mode[params[1]]) * 4

        # Select
        params = sel.split('=')
        if params[0] != "sel":
            return -1

        if len(params) != 2:
            raise ValueError('invalid op: ' + mode)

        if params[1].isdecimal():
            count += int(params[1])
        else:
            count += int(self.operand_ares_select[params[1]])

        return count

    def merge(self, op_code, operand, op_code_next, operand_next):
        if op_code != op_code_next:
            return False
        if '#' in operand or '#' in operand_next:
            return False

        if op_code not in self.instruction_dict_merge or op_code_next not in self.instruction_dict_merge:
            return False

        bit_dict = {}
        params_dict = {}

        if op_code == 'mnts':
            params_dict = self.operand_mnts_params[0]

        if op_code == 'mntx':
            params_dict = self.operand_mntx_params[0]

        if op_code == 'dstm0':
            params_dict = self.operand_dstm0_params[0]

        if op_code == 'dstm1':
            params_dict = self.operand_dstm1_params[0]

        if op_code == 'dstm2':
            params_dict = self.operand_dstm2_params[0]

        if op_code == 'ares':
            count = 0

            # Find the 'ares' start keyword
            count = self.ares_started(operand)
            if count != -1:
                pass
            else:
                raise ValueError("Ares merge error, can't find the start mode and selection")

            next_count = self.ares_started(operand_next)
            if next_count != -1:
                # restart ares
                return False

            return True

        operand = operand.replace('\t', ' ')
        items = operand.split(',')
        for each in items:
            each = (each.lstrip().rstrip())
            each = each.replace('{', '')
            each = each.replace('}', '')

            if each in params_dict:
                if each not in bit_dict:
                    # bit exists
                    if params_dict[each]['bit'] in bit_dict:
                        return False
                    else:
                        bit_dict[each] = params_dict[each]['bit']

        operand_next = operand_next.replace('\t', ' ')
        items_next = operand_next.split(',')
        for each in items_next:
            each = (each.lstrip().rstrip())
            each = each.replace('{', '')
            each = each.replace('}', '')

            if each in params_dict:
                if each not in bit_dict:
                    # bit exists
                    if params_dict[each]['bit'] in bit_dict.values():
                        return False
                    else:
                        bit_dict[each] = params_dict[each]['bit']

        return True

    def parse_op(self, op_code, operand, inst_label_list, index):
        """
        process the op code and operand
        """
        code = 0
        if op_code in self.instruction_dict:
            code = (self.instruction_dict[op_code] << 26)

        if op_code == 'memc':
            code += self.parse_op_memc(operand)
        if op_code == 'mnts':
            code += self.parse_op_mnts(operand)
        if op_code == 'dstm0':
            code += self.parse_op_dstm0(operand)
        if op_code == 'dstm1':
            code += self.parse_op_dstm1(operand)
        if op_code == 'dstm2':
            code += self.parse_op_dstm2(operand)
        if op_code == 'ares':
            code += self.parse_op_ares(operand)
        if op_code == 'iow':
            code += self.parse_op_iow(operand)
        if op_code == 'dprc':
            code += self.parse_op_dprc(operand)
        if op_code == 'rst':
            code += self.parse_op_rst(operand)
        if op_code == 'init':
            code += self.parse_op_init(operand)
        if op_code == 'smrk':
            code += self.parse_op_smrk(operand)
        if op_code == 'cmrk':
            code += self.parse_op_cmrk(operand)
        if op_code == 'macro':
            code += self.parse_op_macro(operand)

        return code

    def parse_op_memc(self, operand):
        if len(operand) < 1:
            raise ValueError('instruction operand length error')
        imm = 0
        if '#' in operand[0]:
            imm += (int(operand[0][1:]))
            return imm

        for op in operand:
            params = op.split('=')
            if len(params) == 1:
                imm |= (self.operand_memc_params[0][params[0]]['val'] << self.operand_memc_params[0][params[0]]['bit'])
            if len(params) == 2:
                if params[1].isdecimal():
                    val = int(params[1])
                else:
                    val = self.operand_memc_params[1][params[0]]['val'][params[1]]
                imm |= (val << self.operand_memc_params[1][params[0]]['bit'])
            if len(params) > 2:
                raise ValueError('invalid op: ' + op)

        return imm

    def parse_op_mnts(self, operand):
        if len(operand) < 1:
            raise ValueError('instruction operand length error')
        imm = 0
        if '#' in operand[0]:
            imm += (int(operand[0][1:]))
            return imm

        for op in operand:
            params = op.split('=')
            if len(params) == 1:
                imm |= (self.operand_mnts_params[0][params[0]]['val'] << self.operand_mnts_params[0][params[0]]['bit'])
            if len(params) == 2:
                if params[1].isdecimal():
                    val = int(params[1])
                else:
                    val = self.operand_mnts_params[1][params[0]]['val'][params[1]]
                imm |= (val << self.operand_mnts_params[1][params[0]]['bit'])
            if len(params) > 2:
                raise ValueError('invalid op: ' + op)

        return imm

    def parse_op_ares(self, operand):
        if len(operand) < 1:
            raise ValueError('instruction operand length error')
        imm = 0
        if '#' in operand[0]:
            imm += (int(operand[0][1:]))
            return imm

        counter = 0

        mode = operand[0]
        sel = operand[1]

        # Mode
        params = mode.split('=')
        if params[0] != "mode":
            raise ValueError('invalid op: ' + mode)

        if len(params) != 2:
            raise ValueError('invalid op: ' + mode)
        if params[1].isdecimal():
            counter += int(params[1]) * 4
            imm += int(params[1]) << 22
        else:
            counter += int(self.operand_ares_mode[params[1]]) * 4
            imm += int(self.operand_ares_mode[params[1]]) << 22

        # Select
        params = sel.split('=')
        if params[0] != "sel":
            raise ValueError('invalid op: ' + mode)

        if len(params) != 2:
            raise ValueError('invalid op: ' + mode)

        if params[1].isdecimal():
            counter += int(params[1])
            imm += int(params[1]) << 12
        else:
            counter += int(self.operand_ares_select[params[1]])
            imm += int(self.operand_ares_select[params[1]]) << 12

        operand = operand[2:]

        for op in operand:
            params = op.split('=')
            if len(params) == 2:
                if params[1].isdecimal():
                    val = int(params[1])
                else:
                    val = self.operand_ares_params[counter][params[0]]['val'][params[1]]
                imm |= (val << self.operand_ares_params[counter][params[0]]['bit'])
            if len(params) > 2:
                raise ValueError('invalid op: ' + op)

        return imm

    def parse_op_mntx(self, operand):
        if len(operand) < 1:
            raise ValueError('instruction operand length error')
        imm = 0
        if '#' in operand[0]:
            imm += (int(operand[0][1:]))
            return imm

        for op in operand:
            params = op.split('=')
            if len(params) == 1:
                imm |= (self.operand_mntx_params[0][params[0]]['val'] << self.operand_mntx_params[0][params[0]]['bit'])
            if len(params) == 2:
                if params[1].isdecimal():
                    val = int(params[1])
                else:
                    val = self.operand_mntx_params[1][params[0]]['val'][params[1]]
                imm |= (val << self.operand_mntx_params[1][params[0]]['bit'])
            if len(params) > 2:
                raise ValueError('invalid op: ' + op)

        return imm

    def parse_op_dstm0(self, operand):
        if len(operand) < 1:
            raise ValueError('instruction operand length error')
        imm = 0
        if '#' in operand[0]:
            imm += (int(operand[0][1:]))
            return imm

        for op in operand:
            params = op.split('=')
            if len(params) == 1:
                imm |= (self.operand_dstm0_params[0][params[0]]['val'] << self.operand_dstm0_params[0][params[0]]
                ['bit'])
            if len(params) == 2:
                if params[1].isdecimal():
                    val = int(params[1])
                else:
                    val = self.operand_dstm0_params[1][params[0]]['val'][params[1]]
                imm |= (val << self.operand_dstm0_params[1][params[0]]['bit'])
            if len(params) > 2:
                raise ValueError('invalid op: ' + op)

        return imm

    def parse_op_dstm1(self, operand):
        if len(operand) < 1:
            raise ValueError('instruction operand length error')
        imm = 0
        if '#' in operand[0]:
            imm += (int(operand[0][1:]))
            return imm

        for op in operand:
            params = op.split('=')
            if len(params) == 1:
                imm |= (self.operand_dstm1_params[0][params[0]]['val'] << self.operand_dstm1_params[0][params[0]]
                ['bit'])
            if len(params) == 2:
                if params[1].isdecimal():
                    val = int(params[1])
                else:
                    val = self.operand_dstm1_params[1][params[0]]['val'][params[1]]
                imm |= (val << self.operand_dstm1_params[1][params[0]]['bit'])
            if len(params) > 2:
                raise ValueError('invalid op: ' + op)

        return imm

    def parse_op_dstm2(self, operand):
        if len(operand) < 1:
            raise ValueError('instruction operand length error')
        imm = 0
        if '#' in operand[0]:
            imm += (int(operand[0][1:]))
            return imm

        for op in operand:
            params = op.split('=')
            if len(params) == 1:
                imm |= (self.operand_dstm2_params[0][params[0]]['val'] << self.operand_dstm2_params[0][params[0]]
                ['bit'])
            if len(params) == 2:
                if params[1].isdecimal():
                    val = int(params[1])
                else:
                    val = self.operand_dstm2_params[1][params[0]]['val'][params[1]]
                imm |= (val << self.operand_dstm2_params[1][params[0]]['bit'])
            if len(params) > 2:
                raise ValueError('invalid op: ' + op)

        return imm

    def parse_op_iow(self, operand):
        if len(operand) < 1:
            raise ValueError('instruction operand length error')
        imm = 0
        if '#' in operand[0]:
            imm += (int(operand[0][1:]))
            return imm

        for op in operand:
            params = op.split('=')
            if len(params) == 1:
                imm |= (self.operand_iow_params[0][params[0]]['val'] << self.operand_iow_params[0][params[0]]['bit'])
            if len(params) == 2:
                if params[1].isdecimal():
                    val = int(params[1])
                else:
                    val = self.operand_iow_params[1][params[0]]['val'][params[1]]
                imm |= (val << self.operand_iow_params[1][params[0]]['bit'])
            if len(params) > 2:
                raise ValueError('invalid op: ' + op)

        return imm

    def parse_op_dprc(self, operand):
        if len(operand) < 1:
            raise ValueError('instruction operand length error')
        imm = 0
        if '#' in operand[0]:
            imm += (int(operand[0][1:]))
            return imm
        for op in operand:
            params = op.split('=')
            if len(params) == 1:
                imm |= (self.operand_dprc_params[0][params[0]]['val'] << self.operand_dprc_params[0][params[0]]['bit'])
            if len(params) == 2:
                if params[1].isdecimal():
                    val = int(params[1])
                else:
                    val = self.operand_dprc_params[1][params[0]]['val'][params[1]]
                imm |= (val << self.operand_dprc_params[1][params[0]]['bit'])
            if len(params) > 2:
                raise ValueError('invalid op: ' + op)

        return imm

    def parse_op_rst(self, operand):
        if len(operand) < 1:
            raise ValueError('instruction operand length error')
        imm = 0
        if '#' in operand[0]:
            imm += (int(operand[0][1:]))
            return imm
        for op in operand:
            params = op.split('=')
            if len(params) == 1:
                imm |= (self.operand_rst_params[0][params[0]]['val'] << self.operand_rst_params[0][params[0]]['bit'])
            if len(params) == 2:
                if params[1].isdecimal():
                    val = int(params[1])
                else:
                    val = self.operand_rst_params[1][params[0]]['val'][params[1]]
                imm |= (val << self.operand_rst_params[1][params[0]]['bit'])
            if len(params) > 2:
                raise ValueError('invalid op: ' + op)

        return imm

        return imm

    def parse_op_init(self, operand):
        if len(operand) < 1:
            raise ValueError('instruction operand length error')
        imm = 0
        if '#' in operand[0]:
            imm += (int(operand[0][1:]))
            return imm
        for op in operand:
            params = op.split('=')
            if len(params) == 1:
                imm |= (self.operand_init_vals[params[0]])
            if len(params) > 1:
                raise ValueError('invalid op: ' + op)

        return imm

    def parse_op_smrk(self, operand):
        if len(operand) < 1:
            raise ValueError('instruction operand length error')
        imm = 0
        if '#' in operand[0]:
            imm += (int(operand[0][1:]))
            return imm
        for op in operand:
            params = op.split('=')
            if len(params) == 1:
                imm |= (self.operand_smrk_vals[params[0]])
            if len(params) > 1:
                raise ValueError('invalid op: ' + op)

        return imm

    def parse_op_cmrk(self, operand):
        if len(operand) < 1:
            raise ValueError('instruction operand length error')
        imm = 0
        if '#' in operand[0]:
            imm += (int(operand[0][1:]))
            return imm
        for op in operand:
            params = op.split('=')
            if len(params) == 1:
                imm |= (self.operand_cmrk_vals[params[0]])
            if len(params) > 1:
                raise ValueError('invalid op: ' + op)

        return imm

    def parse_op_macro(self, operand):
        if len(operand) < 1:
            raise ValueError('instruction operand length error')
        imm = 0
        if '#' in operand[0]:
            imm += (int(operand[0][1:]))
            return imm
        for op in operand:
            params = op.split('=')
            if len(params) == 1:
                imm |= (self.operand_macro_params[0][params[0]]['val'] << self.operand_macro_params[0][params[0]]
                ['bit'])
            if len(params) == 2:
                if params[1].isdecimal():
                    val = int(params[1])
                else:
                    val = self.operand_macro_params[1][params[0]]['val'][params[1]]
                imm |= (val << self.operand_macro_params[1][params[0]]['bit'])
            if len(params) > 2:
                raise ValueError('invalid op: ' + op)

        return imm


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
            self.inst_extension = InstructionExtension()

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
    args = parse_args()
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


