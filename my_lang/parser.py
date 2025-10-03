from my_lang.lexer import Token, Lexer

class AST:
    pass

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class String(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class NoOp(AST):
    pass

class Block(AST):
    def __init__(self, statements):
        self.statements = statements

class If(AST):
    def __init__(self, condition, if_block, else_block=None):
        self.condition = condition
        self.if_block = if_block
        self.else_block = else_block

class While(AST):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class Print(AST):
    def __init__(self, expr):
        self.expr = expr

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Неверный синтаксис')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def program(self):
        statements = []
        while self.current_token.type != 'EOF':
            statements.append(self.statement())
        return Block(statements)

    def statement(self):
        if self.current_token.type == 'ID':
            node = self.assignment_statement()
        elif self.current_token.type == 'KEYWORD_IF':
            node = self.if_statement()
        elif self.current_token.type == 'KEYWORD_LOOP':
            node = self.while_statement()
        elif self.current_token.type == 'KEYWORD_SHOW':
            node = self.print_statement()
        else:
            node = self.empty_statement()
        return node

    def assignment_statement(self):
        left = self.variable()
        token = self.current_token
        self.eat('ASSIGN_OR_EQ') # 'is'
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def if_statement(self):
        self.eat('KEYWORD_IF') # if
        condition = self.expr()
        self.eat('KEYWORD_THEN') # then
        if_block = self.block_statement()
        else_block = None
        if self.current_token.type == 'KEYWORD_ELSE':
            self.eat('KEYWORD_ELSE') # else
            else_block = self.block_statement()
        self.eat('KEYWORD_END') # end
        node = If(condition, if_block, else_block)
        return node

    def while_statement(self):
        self.eat('KEYWORD_LOOP') # loop
        self.eat('KEYWORD_WHILE') # while
        condition = self.expr()
        self.eat('KEYWORD_DO') # do
        body = self.block_statement()
        self.eat('KEYWORD_END') # end
        node = While(condition, body)
        return node

    def print_statement(self):
        self.eat('KEYWORD_SHOW') # show
        expr = self.expr()
        node = Print(expr)
        return node

    def block_statement(self):
        statements = []
        while self.current_token.type != 'KEYWORD_ELSE' and \
              self.current_token.type != 'KEYWORD_END' and \
              self.current_token.type != 'EOF':
            statements.append(self.statement())
        node = Block(statements)
        return node

    def empty_statement(self):
        return NoOp()

    def expr(self):
        node = self.term()

        while self.current_token.type in ('PLUS', 'MINUS', 'ASSIGN_OR_EQ', 'KEYWORD_LESS', 'KEYWORD_GREATER'):
            token = self.current_token
            if token.type == 'PLUS':
                self.eat('PLUS')
            elif token.type == 'MINUS':
                self.eat('MINUS')
            elif token.type == 'ASSIGN_OR_EQ': # 'is' для сравнения
                self.eat('ASSIGN_OR_EQ')
            elif token.type == 'KEYWORD_LESS': # 'less than'
                self.eat('KEYWORD_LESS')
                self.eat('KEYWORD_THAN')
            elif token.type == 'KEYWORD_GREATER': # 'greater than'
                self.eat('KEYWORD_GREATER')
                self.eat('KEYWORD_THAN')
            node = BinOp(left=node, op=token, right=self.term())
        return node

    def term(self):
        node = self.factor()

        while self.current_token.type in ('MUL', 'DIV'):
            token = self.current_token
            if token.type == 'MUL':
                self.eat('MUL')
            elif token.type == 'DIV':
                self.eat('DIV')
            node = BinOp(left=node, op=token, right=self.factor())
        return node

    def factor(self):
        token = self.current_token
        if token.type == 'PLUS':
            self.eat('PLUS')
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == 'MINUS':
            self.eat('MINUS')
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == 'INTEGER':
            self.eat('INTEGER')
            return Num(token)
        elif token.type == 'STRING':
            self.eat('STRING')
            return String(token)
        elif token.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.expr()
            self.eat('RPAREN')
            return node
        else:
            node = self.variable()
            return node

    def variable(self):
        node = Var(self.current_token)
        self.eat('ID')
        return node

    def parse(self):
        node = self.program()
        if self.current_token.type != 'EOF':
            self.error()
        return node

if __name__ == '__main__':
    text = """
    x is 10 + 5
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
    parser = Parser(lexer)
    ast = parser.parse()
    print("Парсинг успешно завершен.")