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
        self.advance() 

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def string(self):
        self.advance() 
        result = ''
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        self.advance() 
        return Token('STRING', result)

    def identifier(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        keywords = {
            'if': Token('KEYWORD_IF', 'if'),
            'then': Token('KEYWORD_THEN', 'then'),
            'else': Token('KEYWORD_ELSE', 'else'),
            'end': Token('KEYWORD_END', 'end'),
            'loop': Token('KEYWORD_LOOP', 'loop'),
            'while': Token('KEYWORD_WHILE', 'while'),
            'do': Token('KEYWORD_DO', 'do'),
            'show': Token('KEYWORD_SHOW', 'show'),
            'is': Token('ASSIGN_OR_EQ', 'is'), # 'is' может быть присваиванием или сравнением
            'less': Token('KEYWORD_LESS', 'less'),
            'than': Token('KEYWORD_THAN', 'than'),
            'greater': Token('KEYWORD_GREATER', 'greater'),
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

            if self.current_char == '"':
                return self.string()

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

            raise Exception(f"Неизвестный символ: {self.current_char}")

        return Token('EOF', None)

if __name__ == '__main__':
    text = """
    x is 10 + 5
    # Это комментарий
    if x greater than 10 then
        show x
    else
        show "x is not greater than 10"
    end
    loop while x greater than 0 do
        x is x - 1
        show x
    end
    y is "Hello, World!"
    show y
    """
    lexer = Lexer(text)
    token = lexer.get_next_token()
    while token.type != 'EOF':
        print(token)
        token = lexer.get_next_token()