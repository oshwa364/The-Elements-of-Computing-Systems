import os.path

from src.compilaion_engine import CompilationEngine
from src.jack_tokenizer import JackTokenizer
from src.vmwriter import VMWriter



class JackCompiler():

    def __init__(self):
        pass

    def compile_all(self, files: list):

        for jack_file in files:
            
            current_filename = os.path.splitext(os.path.basename(jack_file))[0]
            filename_out = jack_file[:-5] + '.vm'
            self.tokenizer = JackTokenizer(jack_file)

            with open(filename_out, 'w') as f:
                self.vm_writer = VMWriter(f)
                self.compiler = CompilationEngine(self.tokenizer, self.vm_writer)
