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
        self.current_command = line.split('//')[0].strip()
        self.current += 1

    def commandType(self) -> str:
        if self.current_command.startswith('push'):
            return 'C_PUSH'
        elif self.current_command.startswith('pop'):
            return 'C_POP'
        elif self.current_command.startswith(
            ('add', 'sub', 'neg', 'eq', 'lt', 'gt', 'and', 'or', 'not')
            ):
            return 'C_ARITHMETIC'
        elif self.current_command.startswith('label'):
            return 'LABEL'
        elif self.current_command.startswith('if-goto'):
            return 'IF-GOTO'
        elif self.current_command.startswith('goto'):
            return 'GOTO'
        elif self.current_command.startswith('function'):
            return 'FUNCTION'
        elif self.current_command.startswith('return'):
            return 'RETURN'
        elif self.current_command.startswith('call'):
            return 'CALL'

    def arg1(self) -> str:
        if self.commandType() == 'C_ARITHMETIC':
            return self.current_command
        else:
            return self.current_command.split(' ')[1]

    def arg2(self) -> int:
        return self.current_command.split(' ')[2]
