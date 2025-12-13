# main.py
from logger import Logger
from system_errors import ErrorReporter
from prototype_lexer import Lexer, Token, TokenType
from prototype_parser import Parser

logger = Logger()
reporter = ErrorReporter(logger)

code  = [
    Token(TokenType.MINUS, '-', 1, 1),
    Token(TokenType.NUMBER, 4, 3, 1),
    Token(TokenType.PLUS, '+', 5, 1),
    Token(TokenType.NUMBER, 2, 7, 1),
    ]

parser = Parser(code, reporter)

print(parser.expr().evaluate())