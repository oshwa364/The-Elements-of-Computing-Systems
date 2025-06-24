import os, os.path

from src.jack_compiler import JackCompiler


class CompilerFileCollector():

    def __init__(self, path):
        self.path = path
        self.jack_files = self._collect_jack_files()

    def _collect_jack_files(self):
        if os.path.isfile(self.path) and self.path.endswith('.jack'):
            return [self.path]
        elif os.path.isdir(self.path):
            files = []
            for filename in os.listdir(self.path):
                if filename.endswith('.jack'):
                    full_path = os.path.join(self.path, filename)
                    files.append(full_path)
            return sorted(files)

    def get_jack_files(self):
        return self.jack_files

def main():
    collector = CompilerFileCollector('test_data/ComplexArrays')
    files_in = collector.get_jack_files()
    compiler = JackCompiler()
    compiler.compile_all(files_in)

if __name__ == '__main__':
    main()
