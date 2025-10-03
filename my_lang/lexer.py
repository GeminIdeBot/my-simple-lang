import re

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if len(self.text) > 0 else None

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
        self.advance() # Пропустить символ новой строки

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def identifier(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        keywords = {
            'if': Token('KEYWORD', 'if'),
            'else': Token('KEYWORD', 'else'),
            'while': Token('KEYWORD', 'while'),
            'print': Token('KEYWORD', 'print'),
        }
        
        token = keywords.get(result, Token('ID', result))
        return token

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char == '#':
                self.skip_comment()
                continue

            if self.current_char.isdigit():
                return Token('INTEGER', self.integer())

            if self.current_char.isalpha() or self.current_char == '_':
                return self.identifier()

            if self.current_char == '+':
                self.advance()
                return Token('PLUS', '+')
            if self.current_char == '-':
                self.advance()
                return Token('MINUS', '-')
            if self.current_char == '*':
                self.advance()
                return Token('MUL', '*')
            if self.current_char == '/':
                self.advance()
                return Token('DIV', '/')
            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token('EQ', '==')
                return Token('ASSIGN', '=')
            if self.current_char == '<':
                self.advance()
                return Token('LT', '<')
            if self.current_char == '>':
                self.advance()
                return Token('GT', '>')
            if self.current_char == '(':
                self.advance()
                return Token('LPAREN', '(')
            if self.current_char == ')':
                self.advance()
                return Token('RPAREN', ')')
            if self.current_char == '{':
                self.advance()
                return Token('LBRACE', '{')
            if self.current_char == '}':
                self.advance()
                return Token('RBRACE', '}')
            if self.current_char == ';':
                self.advance()
                return Token('SEMI', ';')

            raise Exception(f"Неизвестный символ: {self.current_char}")

        return Token('EOF', None)

if __name__ == '__main__':
    text = """
    x = 10 + 5;
    if x > 10 {
        print x;
    } else {
        print 0;
    }
    """
    lexer = Lexer(text)
    token = lexer.get_next_token()
    while token.type != 'EOF':
        print(token)
        token = lexer.get_next_token()