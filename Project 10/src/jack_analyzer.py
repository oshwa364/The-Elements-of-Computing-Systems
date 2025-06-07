import os.path

from src.compilation_engine import CompilationEngine
from src.jack_tokenizer import JackTokenizer


class JackAnalyzer():

    def __init__(self):
        pass

    def analyze_all(self, files: list):
        for jack_file in files:
            current_filename = os.path.splitext(os.path.basename(jack_file))[0]
            filename_out = current_filename + '.xml'
            self.tokenizer = JackTokenizer(jack_file)
            # self._out_file = open(filename_out, 'w')
            with open(filename_out, 'w') as f:
                self.compiler = CompilationEngine(f, self.tokenizer)
            # self._write_first_token()
            # self._write_tokens()
            # self._write_last_token()
            # self._out_file.close()
    
    def _write_tokens(self):
        while self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            token_type = self.tokenizer.tokenType()
            match token_type:
                case 'KEYWORD':
                    self._out_file.write(f'<keyword> {self.tokenizer.keyword()} </keyword>\n')
                case 'SYMBOL':
                    if self.tokenizer.symbol() == '<':
                        self._out_file.write(f'<symbol> &lt; </symbol>\n')
                    elif self.tokenizer.symbol()== '>':
                        self._out_file.write(f'<symbol> &gt; </symbol>\n')
                    elif self.tokenizer.symbol() == '"':
                        self._out_file.write(f'<symbol> &quot; </symbol>\n')
                    elif self.tokenizer.symbol() == '&':
                        self._out_file.write(f'<symbol> &amp; </symbol>\n')
                    else:
                        self._out_file.write(f'<symbol> {self.tokenizer.symbol()} </symbol>\n')
                case 'STRING_CONST':
                    self._out_file.write(f'<stringConstant> {self.tokenizer.stringVal()} </stringConstant>\n')
                case 'INT_CONST':
                    self._out_file.write(f'<integerConstant> {self.tokenizer.intVal()} </integerConstant>\n')
                case 'IDENTIFIER':
                    self._out_file.write(f'<identifier> {self.tokenizer.identifier()} </identifier>\n')

    def _write_first_token(self):
        self._out_file.write('<tokens>\n')

    def _write_last_token(self):
        self._out_file.write('</tokens>\n')
