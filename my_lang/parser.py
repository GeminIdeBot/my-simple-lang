from my_lang.lexer import Token, Lexer

class AST:
    pass

class Num(AST):
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
        elif self.current_token.type == 'KEYWORD' and self.current_token.value == 'if':
            node = self.if_statement()
        elif self.current_token.type == 'KEYWORD' and self.current_token.value == 'while':
            node = self.while_statement()
        elif self.current_token.type == 'KEYWORD' and self.current_token.value == 'print':
            node = self.print_statement()
        elif self.current_token.type == 'LBRACE':
            node = self.block_statement()
        else:
            node = self.empty_statement()
        
        if self.current_token.type == 'SEMI':
            self.eat('SEMI')
        return node

    def assignment_statement(self):
        left = self.variable()
        token = self.current_token
        self.eat('ASSIGN')
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def if_statement(self):
        self.eat('KEYWORD') # if
        self.eat('LPAREN')
        condition = self.expr()
        self.eat('RPAREN')
        if_block = self.block_statement()
        else_block = None
        if self.current_token.type == 'KEYWORD' and self.current_token.value == 'else':
            self.eat('KEYWORD') # else
            else_block = self.block_statement()
        node = If(condition, if_block, else_block)
        return node

    def while_statement(self):
        self.eat('KEYWORD') # while
        self.eat('LPAREN')
        condition = self.expr()
        self.eat('RPAREN')
        body = self.block_statement()
        node = While(condition, body)
        return node

    def print_statement(self):
        self.eat('KEYWORD') # print
        expr = self.expr()
        node = Print(expr)
        return node

    def block_statement(self):
        self.eat('LBRACE')
        statements = []
        while self.current_token.type != 'RBRACE':
            statements.append(self.statement())
        self.eat('RBRACE')
        node = Block(statements)
        return node

    def empty_statement(self):
        return NoOp()

    def expr(self):
        node = self.term()

        while self.current_token.type in ('PLUS', 'MINUS', 'EQ', 'LT', 'GT'):
            token = self.current_token
            if token.type == 'PLUS':
                self.eat('PLUS')
            elif token.type == 'MINUS':
                self.eat('MINUS')
            elif token.type == 'EQ':
                self.eat('EQ')
            elif token.type == 'LT':
                self.eat('LT')
            elif token.type == 'GT':
                self.eat('GT')
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
    x = 10 + 5;
    if (x > 10) {
        print x;
    } else {
        print 0;
    }
    while (x > 0) {
        x = x - 1;
        print x;
    }
    """
    lexer = Lexer(text)
    parser = Parser(lexer)
    ast = parser.parse()
    # Для демонстрации можно вывести структуру AST, но это требует рекурсивного обхода
    # Пока просто убедимся, что парсинг не вызывает ошибок
    print("Парсинг успешно завершен.")