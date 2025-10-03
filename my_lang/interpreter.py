from my_lang.parser import Parser, BinOp, Num, UnaryOp, Var, Assign, Block, If, While, Print, NoOp, String, Boolean
from my_lang.lexer import Lexer

GLOBAL_SCOPE = {}

class NodeVisitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'Нет метода visit_{type(node).__name__}')

class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser

    def visit_BinOp(self, node):
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)

        if node.op.type == 'PLUS':
            return left_val + right_val
        elif node.op.type == 'MINUS':
            return left_val - right_val
        elif node.op.type == 'MUL':
            return left_val * right_val
        elif node.op.type == 'DIV':
            return left_val / right_val
        elif node.op.type == 'KEYWORD_IS': # 'is' для сравнения
            return left_val == right_val
        elif node.op.type == 'NOT_EQ': # 'not is'
            return left_val != right_val
        elif node.op.type == 'KEYWORD_LESS': # 'less than'
            return left_val < right_val
        elif node.op.type == 'KEYWORD_GREATER': # 'greater than'
            return left_val > right_val

    def visit_Num(self, node):
        return node.value

    def visit_String(self, node):
        return node.value

    def visit_Boolean(self, node):
        return node.value

    def visit_UnaryOp(self, node):
        if node.op.type == 'PLUS':
            return +self.visit(node.expr)
        elif node.op.type == 'MINUS':
            return -self.visit(node.expr)

    def visit_Block(self, node):
        for statement in node.statements:
            self.visit(statement)

    def visit_Assign(self, node):
        var_name = node.left.value
        GLOBAL_SCOPE[var_name] = self.visit(node.right)

    def visit_Var(self, node):
        var_name = node.value
        val = GLOBAL_SCOPE.get(var_name)
        if val is None:
            raise NameError(f"Переменная '{var_name}' не определена.")
        return val

    def visit_NoOp(self, node):
        pass

    def visit_If(self, node):
        condition_result = self.visit(node.condition)
        if condition_result:
            self.visit(node.if_block)
        elif node.else_block:
            self.visit(node.else_block)

    def visit_While(self, node):
        while self.visit(node.condition):
            self.visit(node.body)

    def visit_Print(self, node):
        print(self.visit(node.expr))

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

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
    flag is true
    if flag is true then
        show "Flag is true"
    end
    z is 10
    if z not is 5 then
        show "z is not 5"
    end
    """
    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpret()
    print("Глобальные переменные:", GLOBAL_SCOPE)