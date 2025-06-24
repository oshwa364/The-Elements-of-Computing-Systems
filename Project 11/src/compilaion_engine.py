from src.symbol_table import SymbolTable


class CompilationEngine():
    
    def __init__(self, tokenizer, vm_writer):
        self.tokenizer = tokenizer
        self.vm_writer = vm_writer
        self.current_class = ''
        self.class_table = SymbolTable()
        self.subroutine_table = SymbolTable()
        self.label_count = 0
        self.compileClass()

    def compileClass(self):
        self._advance()
        self._pass_token('class')
        self.current_class = self.token
        self._advance()
        self._pass_token('{')

        while self._is_class_var_dec():
            self.compileClassVarDec()
        while self._is_subroutine():
            self.compileSubroutine()

    def compileClassVarDec(self):
        kind = self.token
        self._advance()
        type_ = self.token
        self._advance()
        name = self.token
        self.class_table.define(name, type_, kind)
        self._advance()
        while self.token == ',':
            self._advance()
            name = self.token
            self.class_table.define(name, type_, kind)
            self._advance()
        self._pass_token(';')

    def compileSubroutine(self):
        self.subroutine_table.reset()
        subroutine_type = self.token
        self._advance()
        self.return_type = self.token
        self._advance()
        subroutine_name = self.token
        self._advance()

        full_subroutine_name = f'{self.current_class}.{subroutine_name}'

        if subroutine_type == 'method':
            self.subroutine_table.define('this', self.current_class, 'arg')

        self._pass_token('(')
        self.compileParameterList()
        self._pass_token(')')

        self.compileSubroutineBody(full_subroutine_name, subroutine_type)

    def compileParameterList(self):
        if self.token != ')':
            type_ = self.token
            self._advance()
            var_name = self.token
            self._advance()
            self.subroutine_table.define(var_name, type_, 'arg')
            while self.token == ',':
                self._advance()
                type_ = self.token
                self._advance()
                var_name = self.token
                self._advance()
                self.subroutine_table.define(var_name, type_, 'arg')

    def compileSubroutineBody(self, full_subroutine_name, subroutine_type):
        self._pass_token('{')
        self.compileVarDec()
        local_count = self.subroutine_table.varCount('var')
        self.vm_writer.writeFunction(full_subroutine_name, local_count)

        if subroutine_type == 'constructor':
            field_count = self.class_table.counts['field']
            self.vm_writer.writePush('constant', field_count)
            self.vm_writer.writeCall('Memory.alloc', 1)
            self.vm_writer.writePop('pointer', 0)
        elif subroutine_type == 'method':
            self.vm_writer.writePush('argument', 0)
            self.vm_writer.writePop('pointer', 0)

        self.compileStatements()
        self._pass_token('}')

    def compileVarDec(self):
        kind = 'var'
        while self.token == 'var':
            self._pass_token('var')
            type_ = self.token
            self._advance()
            name = self.token
            self.subroutine_table.define(name, type_, kind)
            self._advance()
            while self.token == ',':
                self._advance()
                name = self.token
                self.subroutine_table.define(name, type_, kind)
                self._advance()
            self._pass_token(';')

    def compileStatements(self):
        while self._is_statement():
            match self.token:
                case 'let':
                    self.compileLet()
                case 'if':
                    self.compileIf()
                case 'while':
                    self.compileWhile()
                case 'do':
                    self.compileDo()
                case 'return':
                    self.compileReturn()

    def compileLet(self):
        self._pass_token('let')
        var_name = self.token
        self._advance()

        is_array = False
        if self.token == '[':
            is_array = True
            self._pass_token('[')
            self.compileExpression()
            self._pass_token(']')
            kind = self.kind_of(var_name)
            segment = self._segment_of(kind)
            index = self.index_of(var_name)
            self.vm_writer.writePush(segment, index)
            self.vm_writer.writeArithmetic('add')

        self._pass_token('=')
        self.compileExpression()
        self._pass_token(';')

        if is_array:
            self.vm_writer.writePop('temp', 0)
            self.vm_writer.writePop('pointer', 1)
            self.vm_writer.writePush('temp', 0)
            self.vm_writer.writePop('that', 0)
        else:
            kind = self.kind_of(var_name)
            segment = self._segment_of(kind)
            index = self.index_of(var_name)    
            self.vm_writer.writePop(segment, index)
        
    
    def compileIf(self):
        self._pass_token('if')
        self._pass_token('(')

        self.compileExpression()
        self.vm_writer.writeArithmetic('not')
        self._pass_token(')')
        enter_label = f'{self.current_class}_{self.label_count}'
        self.label_count += 1
        exit_label = f'{self.current_class}_{self.label_count}'
        self.label_count += 1
        self.vm_writer.writeIf(exit_label)

        self._pass_token('{')
        
        self.compileStatements()
        
        self.vm_writer.writeGoto(enter_label)
        self._pass_token('}')
        self.vm_writer.writeLabel(exit_label)
        if self.token == 'else':
            self._pass_token('else')
            self._pass_token('{')

            self.compileStatements()

            self._pass_token('}')
        self.vm_writer.writeLabel(enter_label)

    def compileWhile(self):
        self._pass_token('while')
        self._pass_token('(')
        enter_label = f'{self.current_class}_{self.label_count}'
        self.label_count += 1
        self.vm_writer.writeLabel(enter_label)
        exit_label = f'{self.current_class}_{self.label_count}'
        self.label_count += 1
        self.compileExpression()
        self._pass_token(')')
        self._pass_token('{')
        self.vm_writer.writeArithmetic('not')
        self.vm_writer.writeIf(exit_label)

        self.compileStatements()

        self.vm_writer.writeGoto(enter_label)
        self.vm_writer.writeLabel(exit_label)
        self._pass_token('}')

    def compileDo(self):
        self._pass_token('do')
        self.compileExpression()
        self.vm_writer.writePop('temp', 0)
        self._pass_token(';')

    def compileReturn(self):
        if self.return_type == 'void':
            self.vm_writer.writePush('constant', 0)
            self.vm_writer.writeReturn()
            self._advance() #probably exchange to _pass_token('return')
            self._pass_token(';')
        # if self.return_type == 'int':
        else:
            self._pass_token('return')
            self.compileExpression()
            self._pass_token(';')
            self.vm_writer.writeReturn()

    def compileExpression(self):
        operators = {'+', '-', '*', '/', '&', '|', '<', '>', '='}

        self.compileTerm()

        while self.token in operators:
            operator = self.token
            self._advance()
            self.compileTerm()
            match operator:
                case '+':
                    self.vm_writer.writeArithmetic('add')
                case '-':
                    self.vm_writer.writeArithmetic('sub')
                case '*':
                    self.vm_writer.writeCall('Math.multiply', 2)
                case'/':
                    self.vm_writer.writeCall('Math.divide', 2)
                case '&':
                    self.vm_writer.writeArithmetic('and')
                case '|':
                    self.vm_writer.writeArithmetic('or')
                case '<':
                    self.vm_writer.writeArithmetic('lt')
                case '>':
                    self.vm_writer.writeArithmetic('gt')
                case '=':
                    self.vm_writer.writeArithmetic('eq')

    def compileTerm(self):
        unary_operators = {'-', '~'}

        token_type = self.tokenizer.tokenType()

        if self.token in unary_operators:
            match self.token:
                case '-':
                    self._advance()
                    self.compileTerm()
                    self.vm_writer.writeArithmetic('neg')
                case '~':
                    self._advance()
                    self.compileTerm()
                    self.vm_writer.writeArithmetic('not')

        elif self.token == '(':
            self._pass_token('(')
            self.compileExpression()
            self._advance()
        
        if token_type == 'INT_CONST':
            self.vm_writer.writePush('constant', self.tokenizer.intVal())
            self._advance()
        elif token_type == 'STRING_CONST':
            string = self.tokenizer.stringVal()
            string_length = len(string)
            self.vm_writer.writePush('constant', string_length)
            self.vm_writer.writeCall('String.new', 1)
            for char in string:
                self.vm_writer.writePush('constant', ord(char))
                self.vm_writer.writeCall('String.appendChar', 2)
            self._advance()


        elif token_type == 'IDENTIFIER':
            count_args = 0
            name = self.token
            self._advance()
            if self.token == '.':
                self._pass_token('.')
                subroutine_name = self.token
                self._advance()
                if self.kind_of(name):
                    kind = self.kind_of(name)
                    segment = self._segment_of(kind)
                    index = self.index_of(name)
                    self.vm_writer.writePush(segment, index)
                    count_args += 1
                    type_ = self.type_of(name)
                    full_name = f'{type_}.{subroutine_name}'
                else:
                    full_name = f'{name}.{subroutine_name}'

                self._pass_token('(')
                count_args += self.compileExpressionList()
                self._pass_token(')')
                self.vm_writer.writeCall(full_name, count_args)

            elif self.token == '(':
                self.vm_writer.writePush('pointer', 0)
                count_args += 1
                full_name = f'{self.current_class}.{name}'
                self._pass_token('(')
                count_args += self.compileExpressionList()
                self._pass_token(')')
                self.vm_writer.writeCall(full_name, count_args)
            elif self.token == '[':
                self._pass_token('[')
                self.compileExpression()
                self._pass_token(']')
                kind = self.kind_of(name)
                segment = self._segment_of(kind)
                index = self.index_of(name)
                self.vm_writer.writePush(segment, index)
                self.vm_writer.writeArithmetic('add')
                self.vm_writer.writePop('pointer', 1)
                self.vm_writer.writePush('that', 0)
            else:
                kind = self.kind_of(name)
                segment = self._segment_of(kind)
                index = self.index_of(name)
                self.vm_writer.writePush(segment, index)
        elif self.token in {'true', 'false', 'null', 'this'}:
            if self.token == 'true':
                self.vm_writer.writePush('constant', 1)
                self.vm_writer.writeArithmetic('neg')
            elif self.token in {'false', 'null'}:
                self.vm_writer.writePush('constant', 0)
            elif self.token == 'this':
                self.vm_writer.writePush('pointer', 0)
            self._advance()

    def compileExpressionList(self):
        count = 0
        if self.token != ')':
            self.compileExpression()
            count += 1
            while self.token == ',':
                self._advance()
                self.compileExpression()
                count += 1
        return count

    def _pass_token(self, expected_token):
        actual = self.token
        if actual != expected_token:
            raise ValueError(f'Expected {expected_token}, got {actual}')
        self._advance()

    def _is_class_var_dec(self):
        return True if self.token in {'static', 'field'} else False
    
    def _is_subroutine(self):
        subroutines = {'constructor', 'function', 'method'}
        return True if self.token in subroutines else False
    
    def _is_statement(self):
        statements = {'let', 'do', 'return', 'if', 'while'}
        return True if self.token in statements else False
    
    def _advance(self):
        if self.tokenizer.hasMoreTokens():
            self.token = self.tokenizer.advance()

    def _segment_of(self, kind):
        segment_table = {
            'static': 'static',
            'field': 'this',
            'arg': 'argument',
            'var': 'local'
        }
        return segment_table[kind]
    
    def kind_of(self, name):
        result = self.subroutine_table.kindOf(name)
        if result is not None:
            return result
        return self.class_table.kindOf(name)

    def index_of(self, name):
        result = self.subroutine_table.indexOf(name)
        if result is not None:
            return result
        return self.class_table.indexOf(name)
    
    def type_of(self, name):
        result = self.subroutine_table.typeOf(name)
        if result is not None:
            return result
        return self.class_table.typeOf(name)