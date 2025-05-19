from src.code_writer import CodeWriter
from src.parser import Parser


class VMTranslator():

    def __init__(self, filename: str):
        self.parser = Parser(filename)
        self.code = CodeWriter(filename)
        self.output = []
        self.file_walk()
        self.add_cycle_end()

    def file_walk(self):
        while self.parser.hasMoreLines():
            self.parser.advance()
            self.code.file.write(self.comment_line())

            command_type = self.parser.commandType()
            if command_type in ('C_PUSH', 'C_POP'):
                self.code.writePushPop(
                    command_type, self.parser.arg1(), self.parser.arg2()
                )
            elif command_type == 'C_ARITHMETIC':
                self.code.writeArithmetic(
                    self.parser.arg1()
                )
    
    def comment_line(self) -> str:
        return f'// {self.parser.current_command}\n'
    
    def add_cycle_end(self):
        self.code.writeEndCycle()
