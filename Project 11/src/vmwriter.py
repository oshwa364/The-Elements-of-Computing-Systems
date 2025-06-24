class VMWriter():

    def __init__(self, out_file):
        self.out_file = out_file
    
    def writePush(self, segment, index):
        self.out_file.write(f'    push {segment} {index}\n')

    def writePop(self, segment, index):
        self.out_file.write(f'    pop {segment} {index}\n')

    def writeArithmetic(self, command):
        self.out_file.write(f'    {command}\n')

    def writeLabel(self, label):
        self.out_file.write(f'label {label}\n')

    def writeGoto(self, label):
        self.out_file.write(f'    goto {label}\n')

    def writeIf(self, label):
        self.out_file.write(f'    if-goto {label}\n')

    def writeCall(self, full_name, count_args):
        self.out_file.write(f'    call {full_name} {count_args}\n')

    def writeFunction(self, name, count):
        self.out_file.write(f'function {name} {count}\n')

    def writeReturn(self):
        self.out_file.write(f'    return\n')
