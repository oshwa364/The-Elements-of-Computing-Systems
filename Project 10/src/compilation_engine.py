class CompilationEngine():

    SPACES = '  '

    def __init__(self, out_file, tokenizer):
        self._out_file = out_file
        self._tokenizer = tokenizer
        self._depth = 0
        self.compileClass()
        
    def compileClass(self):
        self._write_open_token('class')
        self._depth += 1
        while self._tokenizer.hasMoreTokens():
            self._advance()
            while self._is_class_var_dec():
                self.compileClassVarDec()
            while self._is_subroutine():
                self.compileSubroutine()
            self._write_token()
        self._depth -= 1
        self._write_close_token('class')

    def _is_class_var_dec(self):
        return True if self.token == 'static' or self.token == 'field' else False
    
    def _is_subroutine(self):
        subroutines = {'constructor', 'function', 'method'}
        return True if self.token in subroutines else False

    def _is_var_dec(self):
        return True if self.token == 'var' else False

    def _is_statement(self):
        statements = {'let', 'do', 'return', 'if', 'while'}
        return True if self.token in statements else False

    def _advance(self):
        if self._tokenizer.hasMoreTokens():
            self.token = self._tokenizer.advance()
            self.token_type = self._tokenizer.tokenType()

    def compileClassVarDec(self):
        self._write_open_token('classVarDec')
        self._depth += 1
        while self.token != ';':
            self._write_token()
            self._advance()
        self._write_token()
        self._advance()
        self._depth -= 1
        self._write_close_token('classVarDec')

    def compileSubroutine(self):
        self._write_open_token('subroutineDec')
        self._depth += 1
        
        self._write_token()
        self._advance()
        self._write_token()
        self._advance()
        self._write_token()
        self._advance()
        self._write_token()
        self._advance()

        self.compileParameterList()
        
        self._write_token()
        self._advance()

        self.compileSubroutineBody()

        self._depth -= 1
        self._write_close_token('subroutineDec')

    def compileParameterList(self):
        self._write_open_token('parameterList')
        self._depth += 1

        while self.token != ')':
            self._write_token()
            self._advance()

        self._depth -= 1
        self._write_close_token('parameterList')

    def compileSubroutineBody(self):
        self._write_open_token('subroutineBody')
        self._depth += 1
        self._write_token()
        self._advance()

        while self._is_var_dec():
            self.compileVarDec()

        self.compileStatements()

        self._write_token()
        self._advance()

        self._depth -= 1
        self._write_close_token('subroutineBody')

    def compileVarDec(self):
        self._write_open_token('varDec')
        self._depth += 1

        while self.token != ';':
            self._write_token()
            self._advance()
        self._write_token()
        self._advance()
        self._depth -= 1
        self._write_close_token('varDec')

    def compileStatements(self):
        self._write_open_token('statements')
        self._depth += 1

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
        
        self._depth -= 1
        self._write_close_token('statements')

    def compileLet(self):
        self._write_open_token('letStatement')
        self._depth += 1
        
        while self.token != ';':
            self._write_token()
            self._advance()
            if self.token == '[':
                self._write_token()
                self._advance()
                self.compileExpression()
            if self.token == '=':
                self._write_token()
                self._advance()
                self.compileExpression()
        
        self._write_token()
        self._advance()  # ВЕРНУТЬ КОГДА ЗАКОНЧИШЬ ВСЕ СТАЙТМЕНТЫ

        self._depth -= 1
        self._write_close_token('letStatement')

    def compileIf(self):
        self._write_open_token('ifStatement')
        self._depth += 1

        self._write_token()
        self._advance()

        self._write_token()
        self._advance()

        self.compileExpression()

        self._write_token()
        self._advance()

        self._write_token()
        self._advance()

        self.compileStatements()

        self._write_token()
        self._advance()

        if self.token == 'else':
            self._write_token()
            self._advance()

            self._write_token()
            self._advance()

            self.compileStatements()

            self._write_token()
            self._advance()

        self._depth -= 1
        self._write_close_token('ifStatement')

    def compileWhile(self):
        self._write_open_token('whileStatement')
        self._depth += 1

        self._write_token()
        self._advance()
        self._write_token()
        self._advance()

        self.compileExpression()

        self._write_token()
        self._advance()
        self._write_token()
        self._advance()

        self.compileStatements()

        self._write_token()
        self._advance()

        self._depth -= 1
        self._write_close_token('whileStatement')

    def compileDo(self):
        self._write_open_token('doStatement')
        self._depth += 1
        
        self._write_token()
        self._advance()
        self._write_token()
        self._advance()
        if self.token == '.':
            self._write_token()
            self._advance()
            self._write_token()
            self._advance()
            self._write_token()
            self._advance()
            self.compileExpressionList()
            self._write_token()
            self._advance()
        else:
            self._write_token()
            self._advance()
            self.compileExpressionList()
            self._write_token()
            self._advance()

        self._write_token()
        self._advance()  # ALL STATEMTNS
        self._depth -= 1
        self._write_close_token('doStatement')

    def compileReturn(self):
        self._write_open_token('returnStatement')
        self._depth += 1

        self._write_token()
        self._advance()

        while self.token != ';':
            self.compileExpression()

        self._write_token()
        self._advance()  # ALL STATEMENTS

        self._depth -= 1
        self._write_close_token('returnStatement')

    def compileExpression(self):
        operators = {'+', '-', '*', '/', '&', '|', '<', '>', '='}

        self._write_open_token('expression')
        self._depth += 1

        self.compileTerm()

        while self.token in operators:
            self._write_token()
            self._advance()
            self.compileTerm()

        self._depth -= 1
        self._write_close_token('expression')

    def compileTerm(self):
        unary_operators = {'-', '~'}
        self._write_open_token('term')
        self._depth += 1

        if self.token == '(':
            self._write_token()
            self._advance()
            self.compileExpression()
            self._write_token()
            self._advance()
        elif self.token in unary_operators:
            self._write_token()
            self._advance()
            self.compileTerm()
        else:
            self._write_token()
            self._advance()

            if self.token == '[':
                self._write_token()
                self._advance()
                self.compileExpression()
                self._write_token()
                self._advance()
            elif self.token == '.':
                self._write_token()
                self._advance()
                self._write_token()
                self._advance()
                self._write_token()
                self._advance()
                self.compileExpressionList()
                self._write_token()
                self._advance()
        
        self._depth -= 1
        self._write_close_token('term')

    def compileExpressionList(self) -> int:
        self._write_open_token('expressionList')
        self._depth += 1

        if self.token != ')':
            self.compileExpression()
            while self.token == ',':
                self._write_token()
                self._advance()
                self.compileExpression()
            

        self._depth -= 1
        self._write_close_token('expressionList')

    def _write_token(self):
        indent = self.SPACES * self._depth
        match self.token_type:
            case 'KEYWORD':
                self._out_file.write(f'{indent}<keyword> {self.token} </keyword>\n')
            case 'SYMBOL':
                if self.token == '<':
                    self._out_file.write(f'{indent}<symbol> &lt; </symbol>\n')
                elif self.token== '>':
                    self._out_file.write(f'{indent}<symbol> &gt; </symbol>\n')
                elif self.token == '"':
                    self._out_file.write(f'{indent}<symbol> &quot; </symbol>\n')
                elif self.token == '&':
                    self._out_file.write(f'{indent}<symbol> &amp; </symbol>\n')
                else:
                    self._out_file.write(f'{indent}<symbol> {self.token} </symbol>\n')
            case 'STRING_CONST':
                self._out_file.write(f'{indent}<stringConstant> {self.token[1:-1]} </stringConstant>\n')
            case 'INT_CONST':
                self._out_file.write(f'{indent}<integerConstant> {self.token} </integerConstant>\n')
            case 'IDENTIFIER':
                self._out_file.write(f'{indent}<identifier> {self.token} </identifier>\n')

    def _write_open_token(self, token):
        indent = self.SPACES * self._depth
        self._out_file.write(f'{indent}<{token}>\n')

    def _write_close_token(self, token):
        indent = self.SPACES * self._depth
        self._out_file.write(f'{indent}</{token}>\n')
