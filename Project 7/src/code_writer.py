class CodeWriter():

    def __init__(self, filename):
        self.filename_output = filename[:-2] + 'asm'
        self.file = open(self.filename_output, 'w')
        self.SP = 256
        self.unique_number = 0

    def writeArithmetic(self, operator):
        output = ''
        if operator == 'add':
            output = (
                '@SP\n'
                'AM=M-1\n'
                'D=M\n'
                'A=A-1\n'
                'M=D+M\n'
            )
        elif operator == 'sub':
            output = (
                '@SP\n'
                'AM=M-1\n'
                'D=M\n'
                'A=A-1\n'
                'M=M-D\n'
            )
        elif operator == 'neg':
            output = (
                '@SP\n'
                'A=M-1\n'
                'M=-M\n'
            )
        elif operator == 'eq':
            output = (
                '@SP\n'
                'AM=M-1\n'
                'D=M\n'
                'A=A-1\n'
                'D=M-D\n'
                f'@EQ_TRUE{self.unique_number}\n'
                'D;JEQ\n'
                '@SP\n'
                'A=M-1\n'
                'M=0\n'
                f'@EQ_END{self.unique_number}\n'
                '0;JMP\n'
                f'(EQ_TRUE{self.unique_number})\n'
                '@SP\n'
                'A=M-1\n'
                'M=-1\n'
                f'(EQ_END{self.unique_number})\n'
            )
            self.unique_number += 1
        elif operator == 'lt':
            output = (
                '@SP\n'
                'AM=M-1\n'
                'D=M\n'
                'A=A-1\n'
                'D=M-D\n'
                f'@LT_TRUE{self.unique_number}\n'
                'D;JLT\n'
                '@SP\n'
                'A=M-1\n'
                'M=0\n'
                f'@LT_END{self.unique_number}\n'
                '0;JMP\n'
                f'(LT_TRUE{self.unique_number})\n'
                '@SP\n'
                'A=M-1\n'
                'M=-1\n'
                f'(LT_END{self.unique_number})\n'
            )
            self.unique_number += 1
        elif operator == 'gt':
            output = (
                '@SP\n'
                'AM=M-1\n'
                'D=M\n'
                'A=A-1\n'
                'D=M-D\n'
                f'@GT_TRUE{self.unique_number}\n'
                'D;JGT\n'
                '@SP\n'
                'A=M-1\n'
                'M=0\n'
                f'@GT_END{self.unique_number}\n'
                '0;JMP\n'
                f'(GT_TRUE{self.unique_number})\n'
                '@SP\n'
                'A=M-1\n'
                'M=-1\n'
                f'(GT_END{self.unique_number})\n'
            )
            self.unique_number += 1
        elif operator == 'and':
            output = (
                '@SP\n'
                'AM=M-1\n'
                'D=M\n'
                'A=A-1\n'
                'M=D&M\n'
            )
        elif operator == 'or':
            output = (
                '@SP\n'
                'AM=M-1\n'
                'D=M\n'
                'A=A-1\n'
                'M=D|M\n'
            )
        elif operator == 'not':
            output = (
                '@SP\n'
                'A=M-1\n'
                'M=!M\n'
            )

        self.file.write(output)

    def writePushPop(self, command_type, segment, index):
        output = ''
        match command_type:
            case 'C_PUSH':
                match segment:
                    case 'constant':
                        output = (
                            f'@{index}\n'
                            'D=A\n'
                            '@SP\n'
                            'A=M\n'
                            'M=D\n'
                            '@SP\n'
                            'M=M+1\n'
                        )
                    case 'argument':
                        output = (
                            '@ARG\n'
                            'D=M\n'
                            f'@{index}\n'
                            'A=D+A\n'
                            'D=M\n'
                            '@SP\n'
                            'A=M\n'
                            'M=D\n'
                            '@SP\n'
                            'M=M+1\n'
                        )
                    case 'local':
                        output = (
                            '@LCL\n'
                            'D=M\n'
                            f'@{index}\n'
                            'A=D+A\n'
                            'D=M\n'
                            '@SP\n'
                            'A=M\n'
                            'M=D\n'
                            '@SP\n'
                            'M=M+1\n'
                        )
                    case 'this':
                        output = (
                            '@THIS\n'
                            'D=M\n'
                            f'@{index}\n'
                            'A=D+A\n'
                            'D=M\n'
                            '@SP\n'
                            'A=M\n'
                            'M=D\n'
                            '@SP\n'
                            'M=M+1\n'
                        )
                    case 'that':
                        output = (
                            '@THAT\n'
                            'D=M\n'
                            f'@{index}\n'
                            'A=D+A\n'
                            'D=M\n'
                            '@SP\n'
                            'A=M\n'
                            'M=D\n'
                            '@SP\n'
                            'M=M+1\n'
                        )
                    case 'temp':
                        index = int(index) + 5
                        output = (
                            f'@{index}\n'
                            'D=M\n'
                            '@SP\n'
                            'A=M\n'
                            'M=D\n'
                            '@SP\n'
                            'M=M+1\n'
                        )
                    case 'pointer':
                        index = int(index) + 3
                        output = (
                            f'@{index}\n'
                            'D=M\n'
                            '@SP\n'
                            'A=M\n'
                            'M=D\n'
                            '@SP\n'
                            'M=M+1\n'
                        )
                    case 'static':
                        name = self.filename_output[:-3] + index
                        output = (
                            f'@{name}\n'
                            'D=M\n'
                            '@SP\n'
                            'A=M\n'
                            'M=D\n'
                            '@SP\n'
                            'M=M+1\n'
                        )
            case 'C_POP':
                match segment:
                    case 'local':
                        output = (
                            '@LCL\n'
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
                    case 'argument':
                        output = (
                            '@ARG\n'
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
                    case 'this':
                        output = (
                            '@THIS\n'
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
                    case 'that':
                        output = (
                            '@THAT\n'
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
                    case 'temp':
                        index = int(index) + 5
                        output = (
                            '@SP\n'
                            'AM=M-1\n'
                            'D=M\n'
                            f'@{index}\n'
                            'M=D\n'
                        )
                    case 'pointer':
                        index = int(index) + 3
                        output = (
                            '@SP\n'
                            'AM=M-1\n'
                            'D=M\n'
                            f'@{index}\n'
                            'M=D\n'
                        )
                    case 'static':
                        name = self.filename_output[:-3] + index
                        output = (
                            '@SP\n'
                            'AM=M-1\n'
                            'D=M\n'
                            f'@{name}\n'
                            'M=D\n'
                        )

        self.file.write(output)

    def writeEndCycle(self):
        output = (
            '(END)\n'
            '@END\n'
            '0;JMP'
        )
        self.file.write(output)