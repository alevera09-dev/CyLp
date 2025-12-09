from prototype_lexer import Lexer
from system_errors import ErrorReporter

code = [
    "str greet = \"Hola Mundo\\\";\n"
]
error_reporter = ErrorReporter()
lexer = Lexer(code[0], error_reporter)
print(lexer.get_tokens())
error_reporter.display()
    




