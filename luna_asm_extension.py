

class InstructionExtension(object):

    instruction_dict = {
        'memc'  :   0b100001,
        'mnts'  :   0b100010,
        'dstm0' :   0b100101,
        'dstm1' :   0b100111,
        'dstm2' :   0b101000,
        'ares'  :   0b100100,
        'iow'   :   0b101001,
        'dprc'  :   0b100110,
        'rst'   :   0b111000,
        'init'  :   0b111100,
        'smrk'  :   0b101010,
        'cmrk'  :   0b101011,
        'macro' :   0b011010,
    }
    instruction_dict_merge = {
        # instructions below may have consecutive ones which require merging before parsing
        'dstm0' :   0b100101, 
        'dstm1' :   0b100111, 
        'dstm2' :   0b101000,
        'ares'  :   0b100100,
        }

    operand_memc_vals = {
        'one'   : 0,
        'total' : 1,
        'ahb'   : 0,
        'luna'  : 1,
        'reg'   : 1,
    }

    operand_memc_params = [
        # parameters in op without '='
        {
        },
        # parameters in op with '='
        {
            'mode'      :   {'bit' :25, 'val' :operand_memc_vals},
            'addr'      :   {'bit' :24, 'val' :operand_memc_vals},
            'one-enable':   {'bit' :23, 'val' :operand_memc_vals},
            'dynamic'   :   {'bit' :22, 'val' :operand_memc_vals},
            'access'    :   {'bit' :21, 'val' :operand_memc_vals},
            'grp5'      :   {'bit' :17, 'val' :operand_memc_vals},
            'grp4'      :   {'bit' :16, 'val' :operand_memc_vals},
            'grp3'      :   {'bit' :15, 'val' :operand_memc_vals},
            'grp2'      :   {'bit' :14, 'val' :operand_memc_vals},
            'grp1'      :   {'bit' :13, 'val' :operand_memc_vals},
            'grp0'      :   {'bit' :12, 'val' :operand_memc_vals},
            'grp'       :   {'bit' :8,  'val' :operand_memc_vals},

            'bsel'      :   {'bit' :0,  'val' :operand_memc_vals},
        }
    ]

    operand_mnts_vals = {
        'mas0-0'    : 0,
        'mas0-1'    : 1,
        'mas0-2'    : 2,
        'mas1-0'    : 3,
        'mas1-1'    : 4,
        'mas1-2'    : 5,
        'slv0'      : 6,
        'slv1'      : 7,
        'pe'        : 8,
        'io-rd0'    : 9,
        'io-rd1'    : 10,
        'io-wr'     : 11,
        'io-ahb'    : 12,
        'p-rd0'     : 13,
        'p-rd1'     : 14,
        'p-wr'      : 15,
        'grp0'      : 16,
        'grp1'      : 17,
        'grp2'      : 18,
        'grp3'      : 19,
        'grp4'      : 20,
        'grp5'      : 21,
        'grp6'      : 22,
        'grp7'      : 23,
        'cos'       : 24,
        'sigmoid'   : 25,
        'tanh'      : 26,

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
        'two_mode'  : 1,
        'four_mode' : 2,
    }

    operand_mnts_params = [
        # parameters in op without '='
        {

        },
        # parameters in op with '='
        {
            'sel'       :   {'bit' :21, 'val' :operand_mnts_vals},

            'din'       :   {'bit' :0, 'val' :operand_mnts_para_val},
            'mode0'     :   {'bit' :3, 'val' :operand_mnts_mode_val},
            'mode1'     :   {'bit' :5, 'val' :operand_mnts_mode_val},
            'sync'      :   {'bit' :7, 'val' :operand_mnts_para_val},

            'p0-iodat'  :   {'bit' :0, 'val' :operand_mnts_para_val},
            'p0-lmdat0' :   {'bit' :4, 'val' :operand_mnts_para_val},
            'p0-lmdat1' :   {'bit' :8, 'val' :operand_mnts_para_val},
            'p0-lmdat2' :   {'bit' :12 ,'val' :operand_mnts_para_val},
            'p0-lmdat3' :   {'bit' :16 ,'val' :operand_mnts_para_val},

            'p1-iodat'  :   {'bit' :0, 'val' :operand_mnts_para_val},
            'p1-lmdat0' :   {'bit' :4, 'val' :operand_mnts_para_val},
            'p1-lmdat1' :   {'bit' :8, 'val' :operand_mnts_para_val},
            'p1-lmdat2' :   {'bit' :12 ,'val' :operand_mnts_para_val},
            'p1-lmdat3' :   {'bit' :16 ,'val' :operand_mnts_para_val},

            'mode'      :   {'bit' :3, 'val' :operand_mnts_mode_val},

            'row'       :   {'bit' :0,  'val' :operand_mnts_para_val},
            'col'       :   {'bit' :4,  'val' :operand_mnts_para_val},
            'overcheck' :   {'bit' :20, 'val' :operand_mnts_para_val},

            'inside'    :   {'bit' :0,  'val' :operand_mnts_para_val},
            'outside'   :   {'bit' :3,  'val' :operand_mnts_para_val},

            'rd'        :   {'bit' :0,  'val' :operand_mnts_para_val},
            'wr'        :   {'bit' :0,  'val' :operand_mnts_para_val},

            'lmrd'      :   {'bit' :0,  'val' :operand_mnts_para_val},
            'lmwr'      :   {'bit' :6,  'val' :operand_mnts_para_val},

        }
    ]

    operand_ares_mode = {
        'master'  : 0,
    }

    operand_ares_select = {
        'select0' : 0,
        'select1' : 1,
        'select2' : 2,
        'select3' : 3,
    }

    operand_ares_params = [
        # master0 select0
        {
            'chs' : {'bit' :16, 'val' :None},
            'crs' : {'bit' :14, 'val' :None},
            'cmc' : {'bit' :8 , 'val' :None},
            'ces' : {'bit' :0, 'val' :None},
        },

        # master0 select1
        {
            'elc' : {'bit': 19, 'val': None},
            'hes' : {'bit': 18, 'val': None},
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
        'iord0' : 1,
        'iord1' : 2,
        'iowr'  : 3,
        'io'    : 0,
        'lut'   : 1,

    }

    operand_mntx_params = [
        # parameters in op without '='
        {
            'slv'       :   {'bit' :21, 'val' :0b00000},
            'pe'        :   {'bit' :21, 'val' :0b00001},
            'sync'      :   {'bit' :21, 'val' :0b01000},
            'master'    :   {'bit' :21, 'val' :0b10000},
            'lmgrp'     :   {'bit' :21, 'val' :0b10001},
            'iolut'     :   {'bit' :21, 'val' :0b10010},
            'port'      :   {'bit' :21, 'val' :0b10011},
            'mode'      :   {'bit' :21, 'val' :0b11000},
        },
        # parameters in op with '='
        {
            'tanh'      :   {'bit' :18, 'val' :operand_mntx_vals},
            'sigm'      :   {'bit' :15, 'val' :operand_mntx_vals},
            'iowr'      :   {'bit' :12, 'val' :operand_mntx_vals},
            'slv1'      :   {'bit' :9,  'val' :operand_mntx_vals},
            'slv0'      :   {'bit' :6,  'val' :operand_mntx_vals},
            'mas1'      :   {'bit' :3,  'val' :operand_mntx_vals},
            'mas0'      :   {'bit' :0,  'val' :operand_mntx_vals},
            'pe'        :   {'bit' :12, 'val' :operand_mntx_vals},

            'overcheck' :   {'bit' :20, 'val' :operand_mntx_vals},
            'col'       :   {'bit' :4,  'val' :operand_mntx_vals},
            'row'       :   {'bit' :0,  'val' :operand_mntx_vals},

            'msel'      :   {'bit' :19, 'val' :operand_mntx_vals},
            'sel'       :   {'bit' :18, 'val' :operand_mntx_vals},
            'iodat'     :   {'bit' :16, 'val' :operand_mntx_vals},
            'lmdat3'    :   {'bit' :12, 'val' :operand_mntx_vals},
            'lmdat2'    :   {'bit' :8,  'val' :operand_mntx_vals},
            'lmdat1'    :   {'bit' :4,  'val' :operand_mntx_vals},
            'lmdat0'    :   {'bit' :0,  'val' :operand_mntx_vals},

            'grp135w'   :   {'bit' :14, 'val' :operand_mntx_vals},
            'grp135r'   :   {'bit' :9,  'val' :operand_mntx_vals},
            'grp024w'   :   {'bit' :5,  'val' :operand_mntx_vals},
            'grp024r'   :   {'bit' :0,  'val' :operand_mntx_vals},

            'ord1'      :   {'bit' :13, 'val' :operand_mntx_vals},
            'ord0'      :   {'bit' :9,  'val' :operand_mntx_vals},
            'iahb'      :   {'bit' :6,  'val' :operand_mntx_vals},
            'ird1'      :   {'bit' :3,  'val' :operand_mntx_vals},
            'ird0'      :   {'bit' :0,  'val' :operand_mntx_vals},

            'wr'        :   {'bit' :6,  'val' :operand_mntx_vals},
            'rd1'       :   {'bit' :3,  'val' :operand_mntx_vals},
            'rd0'       :   {'bit' :0,  'val' :operand_mntx_vals},

            'm1p1'      :   {'bit' :15, 'val' :operand_mntx_vals},
            'm1p0'      :   {'bit' :12, 'val' :operand_mntx_vals},
            'm0p1'      :   {'bit' :3,  'val' :operand_mntx_vals},
            'm0p0'      :   {'bit' :0,  'val' :operand_mntx_vals},
        }
    ]

    operand_dstm0_vals = {

        # master
        'bypass'    : 0b00,
        'constant'  : 0b01,
        'ioready'   : 0b10,

        # slave
        'normal'    : 0b00,
        'copy'      : 0b01,
        'rotate'    : 0b10,
        'fft'       : 0b11,

        '64bit'     : 0b00,
        '128bit'    : 0b01,
        '256bit'    : 0b10,
        '512bit'    : 0b11,
    }

    operand_dstm0_params = [
        # parameters in op without '='
        {
            'master0'   :   {'bit' :24, 'val' :0},
            'master1'   :   {'bit' :24, 'val' :1},
            'slave0'    :   {'bit' :24, 'val' :2},
            'slave1'    :   {'bit' :24, 'val' :3},

            'config0'   :   {'bit' :23, 'val' :0},
            'config1'   :   {'bit' :23, 'val' :1},
        },

        # parameters in op with '='
        {
            # master
            'enable'    :   {'bit' :21, 'val' :operand_dstm0_vals},
            'hold'      :   {'bit' :14, 'val' :operand_dstm0_vals},

            'w-hold'    :   {'bit' :11, 'val' :operand_dstm0_vals},
            'h-hold'    :   {'bit' :12, 'val' :operand_dstm0_vals},
            'c-hold'    :   {'bit' :13, 'val' :operand_dstm0_vals},
            's-hold'    :   {'bit' :8, 'val' :operand_dstm0_vals},
            't-hold'    :   {'bit' :9, 'val' :operand_dstm0_vals},
            'r-hold'    :   {'bit' :10, 'val' :operand_dstm0_vals},
            'i-hold'    :   {'bit' :8, 'val' :operand_dstm0_vals},
            'j-hold'    :   {'bit' :9, 'val' :operand_dstm0_vals},
            'k-hold'    :   {'bit' :10, 'val' :operand_dstm0_vals},
            'x-hold'    :   {'bit' :11, 'val' :operand_dstm0_vals},
            'y-hold'    :   {'bit' :12, 'val' :operand_dstm0_vals},
            'z-hold'    :   {'bit' :13, 'val' :operand_dstm0_vals},

            'w-mode'    :   {'bit' :5, 'val' :operand_dstm0_vals},
            'h-mode'    :   {'bit' :6, 'val' :operand_dstm0_vals},
            'c-mode'    :   {'bit' :7, 'val' :operand_dstm0_vals},
            's-mode'    :   {'bit' :2, 'val' :operand_dstm0_vals},
            't-mode'    :   {'bit' :3, 'val' :operand_dstm0_vals},
            'r-mode'    :   {'bit' :4, 'val' :operand_dstm0_vals},
            'i-mode'    :   {'bit' :2, 'val' :operand_dstm0_vals},
            'j-mode'    :   {'bit' :3, 'val' :operand_dstm0_vals},
            'k-mode'    :   {'bit' :4, 'val' :operand_dstm0_vals},
            'x-mode'    :   {'bit' :5, 'val' :operand_dstm0_vals},
            'y-mode'    :   {'bit' :6, 'val' :operand_dstm0_vals},
            'z-mode'    :   {'bit' :7, 'val' :operand_dstm0_vals},

            'w-input'   :   {'bit' :1, 'val' :operand_dstm0_vals},
            'h-input'   :   {'bit' :1, 'val' :operand_dstm0_vals},
            'c-input'   :   {'bit' :1, 'val' :operand_dstm0_vals},

            'j-input'   :   {'bit' :0, 'val' :operand_dstm0_vals},
            'k-input'   :   {'bit' :0, 'val' :operand_dstm0_vals},
            't-input'   :   {'bit' :0, 'val' :operand_dstm0_vals},
            'r-input'   :   {'bit' :0, 'val' :operand_dstm0_vals},

            'i-input'   :   {'bit' :20, 'val' :operand_dstm0_vals},
            's-input'   :   {'bit' :20, 'val' :operand_dstm0_vals},

            # slave
            'stride'    :   {'bit' :15, 'val' :operand_dstm0_vals},
            'max-pool'  :   {'bit' :14, 'val' :operand_dstm0_vals},
            'precision' :   {'bit' :12, 'val' :operand_dstm0_vals},
            'blk'       :   {'bit' :10, 'val' :operand_dstm0_vals},
            'mode'      :   {'bit' :8,  'val' :operand_dstm0_vals},
            'outband'   :   {'bit' :6,  'val' :operand_dstm0_vals},
            'inband'    :   {'bit' :4,  'val' :operand_dstm0_vals},
            'format'    :   {'bit' :3,  'val' :operand_dstm0_vals},

            'filter'    :   {'bit' :2,  'val' :operand_dstm0_vals},

            'fft-mode'  :   {'bit' :17,  'val' :operand_dstm0_vals},
            'fft-st-cnt':   {'bit' :19,  'val' :operand_dstm0_vals},
            'fft-sc-out':   {'bit' :22,  'val' :operand_dstm0_vals},

        }

    ]


    operand_dstm1_vals = {

        's'     : 0,
        't'     : 1,
        'r'     : 2,
        'w'     : 3,
        'h'     : 4,
        'c'     : 5,
        'i'     : 6,
        'j'     : 7,
        'k'     : 1,

    }

    operand_dstm1_params = [
        # parameters in op without '='
        {
            'master0'   :   {'bit' :24, 'val' :0},
            'master1'   :   {'bit' :24, 'val' :1},
            'slave0'    :   {'bit' :24, 'val' :2},
            'slave1'    :   {'bit' :24, 'val' :3},

            'config0'   :   {'bit' :23, 'val' :0},
            'config1'   :   {'bit' :23, 'val' :1},
        },
        # parameters in op with '='
        {
            'source'    :   {'bit' :20, 'val' :operand_dstm1_vals},

            'addrm'     :   {'bit' :18, 'val' :operand_dstm1_vals},

            'k-enable'  :   {'bit' :17, 'val' :operand_dstm1_vals},
            'j-enable'  :   {'bit' :16, 'val' :operand_dstm1_vals},
            'i-enable'  :   {'bit' :15, 'val' :operand_dstm1_vals},
            'c-enable'  :   {'bit' :14, 'val' :operand_dstm1_vals},
            'h-enable'  :   {'bit' :13, 'val' :operand_dstm1_vals},
            'w-enable'  :   {'bit' :12, 'val' :operand_dstm1_vals},
            'r-enable'  :   {'bit' :11, 'val' :operand_dstm1_vals},
            't-enable'  :   {'bit' :10, 'val' :operand_dstm1_vals},
            's-enable'  :   {'bit' :9, 'val' :operand_dstm1_vals},

            'k-carry'   :   {'bit' :8, 'val' :operand_dstm1_vals},
            'j-carry'   :   {'bit' :7, 'val' :operand_dstm1_vals},
            'i-carry'   :   {'bit' :6, 'val' :operand_dstm1_vals},
            'c-carry'   :   {'bit' :5, 'val' :operand_dstm1_vals},
            'h-carry'   :   {'bit' :4, 'val' :operand_dstm1_vals},
            'w-carry'   :   {'bit' :3, 'val' :operand_dstm1_vals},
            'r-carry'   :   {'bit' :2, 'val' :operand_dstm1_vals},
            't-carry'   :   {'bit' :1, 'val' :operand_dstm1_vals},
            's-carry'   :   {'bit' :0, 'val' :operand_dstm1_vals},
        }

    ]


    operand_dstm2_vals = {

    }

    operand_dstm2_params = [
        # parameters in op without '='
        {
            'master0'   :   {'bit' :24, 'val' :0},
            'master1'   :   {'bit' :24, 'val' :1},
            'slave0'    :   {'bit' :24, 'val' :2},
            'slave1'    :   {'bit' :24, 'val' :3},
        },
        # parameters in op with '='
        {
            'datapath'  :   {'bit' :20, 'val' :operand_dstm2_vals},

            'dp-merge'  :   {'bit' :18, 'val' :operand_dstm2_vals},

            'k-r-carry' :   {'bit' :17, 'val' :operand_dstm2_vals},
            'j-r-carry' :   {'bit' :16, 'val' :operand_dstm2_vals},
            'i-r-carry' :   {'bit' :15, 'val' :operand_dstm2_vals},
            'c-r-carry' :   {'bit' :14, 'val' :operand_dstm2_vals},
            'h-r-carry' :   {'bit' :13, 'val' :operand_dstm2_vals},
            'w-r-carry' :   {'bit' :12, 'val' :operand_dstm2_vals},
            'r-r-carry' :   {'bit' :11, 'val' :operand_dstm2_vals},
            't-r-carry' :   {'bit' :10, 'val' :operand_dstm2_vals},
            's-r-carry' :   {'bit' :9, 'val' :operand_dstm2_vals},

            'k-l-carry' :   {'bit' :8, 'val' :operand_dstm2_vals},
            'j-l-carry' :   {'bit' :7, 'val' :operand_dstm2_vals},
            'i-l-carry' :   {'bit' :6, 'val' :operand_dstm2_vals},
            'c-l-carry' :   {'bit' :5, 'val' :operand_dstm2_vals},
            'h-l-carry' :   {'bit' :4, 'val' :operand_dstm2_vals},
            'w-l-carry' :   {'bit' :3, 'val' :operand_dstm2_vals},
            'r-l-carry' :   {'bit' :2, 'val' :operand_dstm2_vals},
            't-l-carry' :   {'bit' :1, 'val' :operand_dstm2_vals},
            's-l-carry' :   {'bit' :0, 'val' :operand_dstm2_vals},
        }

    ]


    operand_iow_vals = {

        '32bit' : 0,
        '64bit' : 1,
        '128bit': 2,
        '256bit': 3,
    }

    operand_iow_params = [
        # parameters in op without '='
        {

        },
        # parameters in op with '='
        {
            'bw'    :   {'bit' :4, 'val' :operand_iow_vals},
            'ch3'   :   {'bit' :3, 'val' :operand_iow_vals},
            'ch2'   :   {'bit' :2, 'val' :operand_iow_vals},
            'ch1'   :   {'bit' :1, 'val' :operand_iow_vals},
            'ch0'   :   {'bit' :0, 'val' :operand_iow_vals},
        }

    ]


    operand_dprc_vals = {

        'idle'  : 0,

        'l2'    : 1,
        'l3'    : 1,
        'l4'    : 2,
        'l5'    : 3,
        'l6'    : 3,

        '64bit' : 0,
        '32bit' : 1,
        '16bit' : 2,
        '8bit'  : 3,

        '32-intg'  : 1,

        'sum'   : 0,
        'cat'   : 1,
    }

    operand_dprc_params = [
        # parameters in op without '='
        {

        },
        # parameters in op with '='
        {
            'outlayer'      :   {'bit' :22, 'val' :operand_dprc_vals},
            'comshift'      :   {'bit' :20, 'val' :operand_dprc_vals},
            'addtree'       :   {'bit' :18, 'val' :operand_dprc_vals},
            'intgnet'       :   {'bit' :16, 'val' :operand_dprc_vals},
            'sigma'         :   {'bit' :14, 'val' :operand_dprc_vals},
            'outlayer-mode' :   {'bit' :8,  'val' :operand_dprc_vals},
            'intgnet-mode'  :   {'bit' :4,  'val' :operand_dprc_vals},
            'layer3-mode'   :   {'bit' :2,  'val' :operand_dprc_vals},
            'mmac1'         :   {'bit' :1,  'val' :operand_dprc_vals},
            'mmac0'         :   {'bit' :0,  'val' :operand_dprc_vals},
        }

    ]


    operand_rst_vals = {
        'clock'     : (0b00),
        'reset'     : (0b01),
        'counter'   : (0b11),

        'stop'      : (0b00),
        'start'     : (0b01),
        'refresh'   : (0b11),

    }

    operand_rst_params = [
        # parameters in op without '='
        {
            'master0'   :   {'bit' :0,   'val' :1},
            'master1'   :   {'bit' :1,   'val' :1},
            'slave0'    :   {'bit' :2,   'val' :1},
            'slave1'    :   {'bit' :3,   'val' :1},
            'iord0'     :   {'bit' :4,   'val' :1},
            'iord1'     :   {'bit' :5,   'val' :1},
            'iowr'      :   {'bit' :6,   'val' :1},
            'psram'     :   {'bit' :7,   'val' :1},
            'topctl'    :   {'bit' :8,   'val' :1},
            'cgc'       :   {'bit' :9,   'val' :1},
            'ahbins'    :   {'bit' :10,  'val' :1},
            'ahbreg'    :   {'bit' :11,  'val' :1},
            'ahbmux'    :   {'bit' :12,  'val' :1},
            'pecore'    :   {'bit' :13,  'val' :1},
            'router'    :   {'bit' :14,  'val' :1},
            'regtab0'   :   {'bit' :16,  'val' :1},
            'regtab1'   :   {'bit' :17,  'val' :1},
            'regtab2'   :   {'bit' :18,  'val' :1},
            'regtab3'   :   {'bit' :19,  'val' :1},

            'stop'      :   {'bit' :0,   'val' :0},
            'start'     :   {'bit' :0,   'val' :1},
            'refresh'   :   {'bit' :0,   'val' :3},

        },
        # parameters in op with '='
        {
            'sel'       :   {'bit' :22,  'val' :operand_rst_vals},

            'master0'   :   {'bit' :0,   'val' :operand_rst_vals},
            'master1'   :   {'bit' :1,   'val' :operand_rst_vals},
            'slave0'    :   {'bit' :2,   'val' :operand_rst_vals},
            'slave1'    :   {'bit' :3,   'val' :operand_rst_vals},
            'iord0'     :   {'bit' :4,   'val' :operand_rst_vals},
            'iord1'     :   {'bit' :5,   'val' :operand_rst_vals},
            'iowr'      :   {'bit' :6,   'val' :operand_rst_vals},
            'psram'     :   {'bit' :7,   'val' :operand_rst_vals},
            'pe0'       :   {'bit' :8,   'val' :operand_rst_vals},
            'pe1'       :   {'bit' :9,   'val' :operand_rst_vals},
            'pe2'       :   {'bit' :10,  'val' :operand_rst_vals},
            'pe3'       :   {'bit' :11,  'val' :operand_rst_vals},
            'pe4'       :   {'bit' :12,  'val' :operand_rst_vals},
            'pe5'       :   {'bit' :13,  'val' :operand_rst_vals},
            'pe6'       :   {'bit' :14,  'val' :operand_rst_vals},
            'pe7'       :   {'bit' :15,  'val' :operand_rst_vals},

            'lcnt'      :   {'bit' :0,   'val' :operand_rst_vals},
        }
    ]

    operand_init_vals = {
        'start-master0' : 1,
        'start-master1' : 2,
    }

    operand_smrk_vals = {
        'block'         : ( 0<<4),
        'non-block'     : ( 1<<4),
        'mark0'         : ( 1<<0),
        'mark1'         : ( 1<<1),
        'mark2'         : ( 1<<2),
        'mark3'         : ( 1<<3),
    }

    operand_cmrk_vals = {
        'mark0'         : ( 1<<0),
        'mark1'         : ( 1<<1),
        'mark2'         : ( 1<<2),
        'mark3'         : ( 1<<3),
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
        operand = operand.replace('\t',' ').split(',')

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

        operand = operand.replace('\t',' ') 
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

        operand_next = operand_next.replace('\t' ,' ')
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
            code = (self.instruction_dict[op_code ]<<26)

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
                raise ValueError('invalid op:  ' +op)

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
                raise ValueError('invalid op:  ' +op)

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
                raise ValueError('invalid op:  ' +op)

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
                raise ValueError('invalid op:  ' +op)

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
                raise ValueError('invalid op:  ' +op)

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
                raise ValueError('invalid op:  ' +op)

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
                raise ValueError('invalid op:  ' +op)

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
                raise ValueError('invalid op:  ' +op)

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
                raise ValueError('invalid op:  ' +op)

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
                raise ValueError('invalid op:  ' +op)

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
                raise ValueError('invalid op:  ' +op)

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
                raise ValueError('invalid op:  ' +op)

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
                raise ValueError('invalid op:  ' +op)

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
                raise ValueError('invalid op:  ' +op)

        return imm
