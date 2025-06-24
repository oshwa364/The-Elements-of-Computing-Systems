import re


class JackTokenizer():

    KEYWORDS = {
        'class', 'constructor', 'function', 'method', 'field', 'static',
        'var', 'int', 'char', 'boolean', 'void', 'true', 'false',
        'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return',
    }

    SYMBOLS = '{}()[],.;+-*/&|<>=~'

    def __init__(self, file):
        with open(file, 'r') as f:
            self.input = f.read()
        self.cleaned_input = self._remove_comments(self.input)
        self.tokens = self._tokenize(self.cleaned_input)
        self.current_index = 0

    def _remove_comments(self, text):
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
        text = re.sub(r'//.*', '', text)
        return text

    def _tokenize(self, text):
        string_regex = r'"[^"\n]*"'
        token_regex = r'(' + string_regex + r'|\w+|[' + re.escape(self.SYMBOLS) + r'])'
        tokens = re.findall(token_regex, text)
        return [*tokens]
        # return [token.strip() for token in tokens if token.strip()]

    def hasMoreTokens(self) -> bool:
        return self.current_index < len(self.tokens)

    def advance(self):
        self.current_token = self.tokens[self.current_index]
        self.current_index += 1
        return self.current_token

    def tokenType(self):
        if self.current_token in self.KEYWORDS:
            return 'KEYWORD'
        elif self.current_token in self.SYMBOLS:
            return 'SYMBOL'
        elif self.current_token[0] == '"':
            return 'STRING_CONST'
        elif self.current_token.isdigit():
            return 'INT_CONST'
        else:
            return 'IDENTIFIER'

    def keyword(self) -> str:
        return self.current_token
    
    def symbol(self) -> str:
        return self.current_token
    
    def identifier(self) -> str:
        return self.current_token
    
    def intVal(self) -> int:
        return self.current_token
    
    def stringVal(self) -> str:
        return self.current_token[1:-1]
