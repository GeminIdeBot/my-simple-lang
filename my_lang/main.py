from my_lang.lexer import Lexer
from my_lang.parser import Parser
from my_lang.interpreter import Interpreter
import sys

def run_interpreter(file_path):
    with open(file_path, 'r') as f:
        text = f.read()

    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpret()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Использование: python main.py <файл.mylang>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    run_interpreter(file_path)