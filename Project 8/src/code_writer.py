class CodeWriter():

    SEGMENT_TABLE = {
        'argument': 'ARG', 'local': 'LCL',
        'this': 'THIS', 'that': 'THAT'
    }

    def __init__(self, filename):
        self.filename_output = filename + '.asm'
        self._out_file = open(self.filename_output, 'w')
        self._function_name = ''
        self._function_count = 0
        self.current_filename = ''
        self.label_number = 0
        self._write_init_SP()
        self._write_sysinit()

    def setFileName(self, filename):
        self.current_filename = filename

    def writeArithmetic(self, operator):
        match operator:
            case 'add':
                self._binary('M=D+M\n')
            case 'sub':
                self._binary('M=M-D\n')
            case 'neg':
                self._unary('M=-M\n')
            case 'eq' | 'lt' | 'gt':
                self._compare(operator)
            case 'and':
                self._binary('M=D&M\n')
            case 'or':
                self._binary('M=D|M\n')
            case 'not':
                self._unary('M=!M\n')

    def writePushPop(self, command, segment, index):
        match command:
            case 'C_PUSH':
                match segment:
                    case 'constant':
                        self._val_to_mem(index, 'A')
                        self._mem_to_stack()
                    case 'argument' | 'local' | 'this' | 'that':
                        self._seg_to_mem(segment, index)
                        self._mem_to_stack()
                    case 'temp':
                        index = int(index) + 5
                        self._val_to_mem(index, 'M')
                        self._mem_to_stack()
                    case 'pointer':
                        index = int(index) + 3
                        self._val_to_mem(index, 'M')
                        self._mem_to_stack()
                    case 'static':
                        name = self.current_filename + '.' + index
                        self._val_to_mem(name, 'M')
                        self._mem_to_stack()
            case 'C_POP':
                match segment:
                    case 'argument' | 'local' | 'this' | 'that':
                        self._stack_to_seg(segment, index)
                    case 'temp':
                        index = int(index) + 5
                        self._stack_to_reg(index)
                    case 'pointer':
                        index = int(index) + 3
                        self._stack_to_reg(index)
                    case 'static':
                        name = self.current_filename + '.' + index
                        self._stack_to_reg(name)

    def writeLabel(self, name):
        label = self._get_label(name)
        self._l_command(label)

    def writeGoto(self, name):
        label = self._get_label(name)
        self._a_command(label)
        self._c_command(None, '0', 'JMP')

    def writeIf(self, name):
        label = self._get_label(name)
        self._stack_to_mem()
        self._a_command(label)
        self._c_command(None, 'D', 'JNE')

    def writeFunction(self, function_name, number_vars):
        self._function_name = function_name
        self._l_command(function_name)
        if int(number_vars) > 0:
            # self._a_command('SP')
            # self._c_command('D', 'M')
            # self._a_command('R14')
            # self._c_command('M', 'D')
            for _ in range(int(number_vars)):
                self._val_to_mem('0', 'A')
                self._mem_to_stack()
            # self._a_command('R14')
            # self._c_command('D', 'M')
            # self._a_command('SP')
            # self._c_command('M', 'D')

    def writeCall(self, function_name, num_args):
        return_address = f'{function_name}.ret${self._function_count}'
        self._val_to_mem(return_address, 'A')
        self._function_count += 1
        self._mem_to_stack()
        self._val_to_mem('LCL', 'M')
        self._mem_to_stack()
        self._val_to_mem('ARG', 'M')
        self._mem_to_stack()
        self._val_to_mem('THIS', 'M')
        self._mem_to_stack()
        self._val_to_mem('THAT', 'M')
        self._mem_to_stack()
        
        output = (
                '@SP\n'
                'D=M\n'
                '@5\n'
                'D=D-A\n'
                f'@{num_args}\n'
                'D=D-A\n'
                '@ARG\n'
                'M=D\n'
                '@SP\n'
                'D=M\n'
                '@LCL\n'
                'M=D\n'
                f'@{function_name}\n'
                '0;JMP\n'
                f'({return_address})\n'
        )
        self._out_file.write(output)

    def writeReturn(self):
        # self._val_to_mem('ARG', 'M+1')
        # self._a_command('R13')
        # self._c_command('M', 'D')  # set SP after return in R13

        # self._stack_to_mem()
        # self._mem_to_point_reg('ARG') # from stack to ARG[0]

        # output = (
        #         '@LCL\n'
        #         'D=M\n'
        #         '@SP\n'
        #         'M=D\n'
        # )
        # self._out_file.write(output)

        # self._stack_to_base('THAT')
        # self._stack_to_base('THIS')
        # self._stack_to_base('ARG')
        # self._stack_to_base('LCL')
        # self._stack_to_base('R15')
        
        # self._val_to_mem('R13', 'M')
        # self._a_command('SP')
        # self._c_command('M', 'D')
        
        # self._a_command('R15')
        # self._c_command('A', 'M')
        # self._c_command(None, '0', 'JMP')
        output = (
                '@LCL\n'
                'D=M\n'
                '@R13\n'
                'M=D\n'

                '@5\n'
                'A=D-A\n'
                'D=M\n'
                '@R14\n'
                'M=D\n'

                '@SP\n'
                'AM=M-1\n'
                'D=M\n'
                '@ARG\n'
                'A=M\n'
                'M=D\n'

                '@ARG\n'
                'D=M+1\n'
                '@SP\n'
                'M=D\n'

                '@R13\n'
                'AM=M-1\n'
                'D=M\n'
                '@THAT\n'
                'M=D\n'

                '@R13\n'
                'AM=M-1\n'
                'D=M\n'
                '@THIS\n'
                'M=D\n'

                '@R13\n'
                'AM=M-1\n'
                'D=M\n'
                '@ARG\n'
                'M=D\n'

                '@R13\n'
                'AM=M-1\n'
                'D=M\n'
                '@LCL\n'
                'M=D\n'

                '@R14\n'
                'A=M\n'
                '0;JMP\n'
        )
        self._out_file.write(output)

    def Close(self):
        self._out_file.close()

    def _write_sysinit(self):
        self._a_command('Sys.init')
        self._c_command(None, '0', 'JMP')

    def _write_init_SP(self):
        self._val_to_mem('256', 'A')
        self._a_command('SP')
        self._c_command('M', 'D')

    def _binary(self, line: str):
        output = (
                '@SP\n'
                'AM=M-1\n'
                'D=M\n'
                'A=A-1\n'
        ) + line
        self._out_file.write(output)

    def _unary(self, line: str):
        output = (
                '@SP\n'
                'A=M-1\n'
        ) + line
        self._out_file.write(output)

    def _compare(self, operator):
        operator = operator.upper()
        jump = f'J{operator}'
        output = (
                '@SP\n'
                'AM=M-1\n'
                'D=M\n'
                'A=A-1\n'
                'D=M-D\n'
                f'@{operator}_TRUE{self.label_number}\n'
                f'D;{jump}\n'
                '@SP\n'
                'A=M-1\n'
                'M=0\n'
                f'@{operator}_END{self.label_number}\n'
                '0;JMP\n'
                f'({operator}_TRUE{self.label_number})\n'
                '@SP\n'
                'A=M-1\n'
                'M=-1\n'
                f'({operator}_END{self.label_number})\n'
            )
        self.label_number += 1
        self._out_file.write(output)
    
    def _mem_to_point_reg(self, reg):
        output = (
            f'@{reg}\n'
            'A=M\n'
            'M=D\n'
        )
        self._out_file.write(output)

    def _mem_to_stack(self):
        output = (
            '@SP\n'
            'A=M\n'
            'M=D\n'
            '@SP\n'
            'M=M+1\n'
        )
        self._out_file.write(output)

    def _val_to_mem(self, index, comp):
        self._a_command(index)
        self._c_command('D', comp)

    def _seg_to_mem(self, segment, index):
        segment = self.SEGMENT_TABLE[segment]
        output = (
            f'@{segment}\n'
            'D=M\n'
            f'@{index}\n'
            'A=D+A\n'
            'D=M\n'
        )
        self._out_file.write(output)

    def _stack_to_seg(self, segment, index):
        segment = self.SEGMENT_TABLE[segment]
        output = (
            f'@{segment}\n'
            'D=M\n'
            f'@{index}\n'
            'D=D+A\n'
            '@R13\n'
            'M=D\n'
            '@SP\n'
            'AM=M-1\n'
            'D=M\n'
            '@R13\n'
            'A=M\n'
            'M=D\n'
        )
        self._out_file.write(output)

    def _stack_to_reg(self, index):
        output = (
            '@SP\n'
            'AM=M-1\n'
            'D=M\n'
            f'@{index}\n'
            'M=D\n'
        )
        self._out_file.write(output)

    def _stack_to_mem(self):
        output = (
            '@SP\n'
            'AM=M-1\n'
            'D=M\n'
        )
        self._out_file.write(output)
    
    def _stack_to_base(self, segment_name):
        self._stack_to_mem()
        self._a_command(segment_name)
        self._c_command('M', 'D')

    def _a_command(self, address: str):
        self._out_file.write(f'@{address}\n')

    def _c_command(self, dest: str, comp: str, jump=None):
        if dest != None:
            self._out_file.write(f'{dest}=')
        self._out_file.write(comp)
        if jump != None:
            self._out_file.write(f';{jump}')
        self._out_file.write('\n')

    def _get_label(self, name):
        label = f'{self._function_name}${name}'
        return label
    
    def _l_command(self, label: str):
        label = f'({label})\n'
        self._out_file.write(label)
