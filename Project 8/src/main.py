import os, os.path

from src.vmtranslator import VMTranslator

class VMFileCollector:
    def __init__(self, path):
        self.path = path
        self.vm_files = self._collect_vm_files()
        self.name = self._extract_name()

    def _collect_vm_files(self):
        if os.path.isfile(self.path) and self.path.endswith('.vm'):
            return [self.path]
        elif os.path.isdir(self.path):
            files = []
            for filename in os.listdir(self.path):
                if filename.endswith('.vm'):
                    full_path = os.path.join(self.path, filename)
                    files.append(full_path)
            return sorted(files)
        
    def _extract_name(self):
        if os.path.isfile(self.path):
            return os.path.splitext(os.path.basename(self.path))[0]
        else:
            return os.path.basename(os.path.abspath(self.path))

    def get_vm_files(self):
        return self.vm_files
    
    def get_name(self):
        return self.name

def main():
    collector = VMFileCollector('StaticsTest')
    filenames_in = collector.get_vm_files()
    filename_out = collector.get_name()
    translation = VMTranslator()
    translation.translate_all(filenames_in, filename_out)

if __name__ == '__main__':
    main()
