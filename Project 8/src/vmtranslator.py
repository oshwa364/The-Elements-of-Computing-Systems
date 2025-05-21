import os.path

from src.code_writer import CodeWriter
from src.parser import Parser


class VMTranslator():

    def __init__(self):
        pass

    def translate_all(self, filenames_in, filename_out):
        self.code_writer = CodeWriter(filename_out)

        for vm_file in filenames_in:
            current_filename = os.path.splitext(os.path.basename(vm_file))[0]
            self.code_writer.setFileName(current_filename)
            self.parser = Parser(vm_file)
            self.file_walk()

        self.code_writer.Close()

    def file_walk(self):
        while self.parser.hasMoreLines():
            self.parser.advance()
            self.code_writer._out_file.write(self.comment_line())

            command_type = self.parser.commandType()
            match command_type:
                case 'C_PUSH' | 'C_POP':
                    self.code_writer.writePushPop(
                        command_type, self.parser.arg1(), self.parser.arg2()
                    )
                case 'C_ARITHMETIC':
                    self.code_writer.writeArithmetic(
                        self.parser.arg1()
                    )
                case 'LABEL':
                    self.code_writer.writeLabel(
                        self.parser.arg1()
                    )
                case 'IF-GOTO':
                    self.code_writer.writeIf(
                        self.parser.arg1()
                    )
                case 'GOTO':
                    self.code_writer.writeGoto(
                        self.parser.arg1()
                    )
                case 'FUNCTION':
                    self.code_writer.writeFunction(
                        self.parser.arg1(), self.parser.arg2()
                    )
                case 'RETURN':
                    self.code_writer.writeReturn()
                case 'CALL':
                    self.code_writer.writeCall(
                        self.parser.arg1(), self.parser.arg2()
                    )
    
    def comment_line(self) -> str:
        line = self.parser.current_command.split('//')[0].strip()
        return f'// {line}\n'
