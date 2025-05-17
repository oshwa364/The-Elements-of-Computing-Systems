class Parser():

    def __init__(self, filename):
        with open(filename, 'r') as f:
            self.lines = f.readlines()
        self.current = 0

    def hasMoreLines(self) -> bool:
        return self.current < len(self.lines)

    def advance(self):
        while True:
            if self.hasMoreLines():
                line = self.lines[self.current].strip()
                if line.startswith('//') or line == '':
                    self.current += 1
                    continue
            break
        self.current_command = line
        self.current += 1

    def instructionType(self) -> str:
        if self.current_command.startswith('@'):
            return 'A_INSTRUCTION'
        elif self.current_command.startswith('('):
            return 'L_INSTRUCTION'
        else:
            return 'C_INSTRUCTION'

    def symbol(self) -> str:
        if self.current_command[0] == '@':
            return self.current_command[1:]
        else:
            return self.current_command[1:-1]

    def dest(self) -> str:
        if '=' in self.current_command:
            return self.current_command.split('=')[0]
        return 'null'

    def comp(self) -> str:
        if '=' in self.current_command:
            right_part = self.current_command.split('=')[1]
            return right_part.split(';')[0]
        return self.current_command.split(';')[0]

    def jump(self) -> str:
        if ';' in self.current_command:
            return self.current_command.split(';')[1]
        return 'null'
    
    def reset(self):
        self.current = 0


class Code():
    dest_table = {
        'null': '000', 'M': '001', 'D': '010', 'DM': '011',
        'A': '100', 'AM': '101', 'AD': '110', 'ADM': '111',
        'MD': '011', 'MA': '101', 'DA': '110', 'AMD': '111',
        'DAM': '111', 'DMA': '111', 'MAD': '111', 'MDA': '111'
    }

    comp_table = {
        '0':   '0101010',
        '1':   '0111111',
        '-1':  '0111010',
        'D':   '0001100',
        'A':   '0110000',
        '!D':  '0001101',
        '!A':  '0110001',
        '-D':  '0001111',
        '-A':  '0110011',
        'D+1': '0011111',
        'A+1': '0110111',
        'D-1': '0001110',
        'A-1': '0110010',
        'D+A': '0000010',
        'A+D': '0000010',
        'D-A': '0010011',
        'A-D': '0000111',
        'D&A': '0000000',
        'A&D': '0000000',
        'D|A': '0010101',
        'A|D': '0010101',
        'M':   '1110000',
        '!M':  '1110001',
        '-M':  '1110011',
        'M+1': '1110111',
        'M-1': '1110010',
        'D+M': '1000010',
        'M+D': '1000010',
        'D-M': '1010011',
        'M-D': '1000111',
        'D&M': '1000000',
        'M&D': '1000000',
        'D|M': '1010101',
        'M|D': '1010101',
    }

    jump_table = {
        'null': '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011',
        'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111',
    }

    def dest(self, mnemonic: str) -> str:
        return self.dest_table[mnemonic]

    def comp(self, mnemonic: str) -> str:
        return self.comp_table[mnemonic]

    def jump(self, mnemonic: str) -> str:
        return self.jump_table[mnemonic]


class SymbolTable():

    def __init__(self):
        self.symbol_table = {
            **{f'R{i}': i for i in range(16)},
            'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3,
            'THAT': 4, 'SCREEN': 16384, 'KBD': 24576
        }

    def addEntry(self, symbol: str, address: int):
        self.symbol_table[symbol] = address

    def contains(self, symbol: str) -> bool:
        return symbol in self.symbol_table

    def getAddress(self, symbol: str) -> int:
        return self.symbol_table[symbol]


class AssemblerHack():
    def __init__(self, filename: str):
        self.parser = Parser(filename)
        self.code = Code()
        self.symbol_table = SymbolTable()
        self.output = []
        self.next_available_address = 16
        self.first_pass()
        self.parser.reset()
        self.second_pass()
        self.write_to_file(filename)

    def first_pass(self):
        line_counter = 0
        while self.parser.hasMoreLines():
            self.parser.advance()
            if self.parser.instructionType() == 'L_INSTRUCTION':
                self.symbol_table.addEntry(
                    self.parser.symbol(), line_counter
                )
            else:
                line_counter += 1

    def second_pass(self):
        while self.parser.hasMoreLines():
            self.parser.advance()
            match self.parser.instructionType():
                case 'A_INSTRUCTION':
                    symbol = self.parser.symbol()
                    if symbol.isdigit():
                        address = format(int(symbol), '015b')
                        self.output.append(f'0{address}')
                    else:
                        if self.symbol_table.contains(symbol):
                            address = self.symbol_table.getAddress(symbol)
                        else:
                            address = self.next_available_address
                            self.symbol_table.addEntry(symbol, address)
                            self.next_available_address += 1
                        address = format(address, '015b')
                        self.output.append(f'0{address}')
                        
                case 'C_INSTRUCTION':
                    dest = self.code.dest(self.parser.dest())
                    comp = self.code.comp(self.parser.comp())
                    jump = self.code.jump(self.parser.jump())
                    self.output.append(f'111{comp}{dest}{jump}')

    def write_to_file(self, filename: str):
        filename_output = filename[:-3] + 'hack'
        with open(filename_output, 'w') as file_output:
            file_output.write('\n'.join(self.output))                


if __name__ == '__main__':
    assembly = AssemblerHack('Rect.asm')