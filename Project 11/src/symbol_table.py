class SymbolTable():

    def __init__(self):
        self.table = {}
        self.counts = {
            'static': 0,
            'field': 0,
            'arg': 0,
            'var': 0
        }

    def reset(self):
        self.table = {}
        self.counts = {
            'static': 0,
            'field': 0,
            'arg': 0,
            'var': 0
        }

    def define(self, name, type_, kind):
        index = self.counts[kind]
        self.table[name] = {
            'type': type_,
            'kind': kind,
            'index': index
        }
        self.counts[kind] += 1

    def varCount(self, kind):
        return self.counts[kind]

    def kindOf(self, name):
        if name in self.table:
            return self.table[name]['kind']
        return None

    def typeOf(self, name):
        if name in self.table:
            return self.table[name]['type']
        return None

    def indexOf(self, name):
        if name in self.table:
            return self.table[name]['index']
        return None