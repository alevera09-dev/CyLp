# lexer_tests.py
# Suite de pruebas para el lexer

# Supongamos que tu lexer se llama `lexer` y está importado
# from my_lexer_module import lexer

# Diccionario de palabras clave (tu versión)

from ..src.frontend.prototype_lexer import lexer

keywords_dict = {
    "if" : "IF",
    "elif" : "ELIF",
    "else" : "ELSE",
    "switch" : "SWITCH",
    "case" : "CASE",
    "for" : "FOR",
    "while" : "WHILE",
    "do" : "DO",
    "dynamic" : "DYNAMIC",
    "int" : "INT",
    "float" : "FLOAT",
    "bool" : "BOOL",
    "str" : "STR",
    "char" : "CHAR",
    "array" : "ARRAY",
    "tuple" : "TUPLE",
    "set" : "SET",
    "dict" : "DICT",
    "func" : "FUNC",
    "lambda" : "LAMBDA",
    "or" : "OR",
    "and" : "AND",
    "not" : "NOT",
}

def test_identifiers_numbers():
    code = "x y variable_name 123 45.67"
    tokens = lexer(code)
    assert tokens[0] == ("IDENTIFIER", "x")
    assert tokens[1] == ("IDENTIFIER", "y")
    assert tokens[2] == ("IDENTIFIER", "variable_name")
    assert tokens[3] == ("NUMBER", 123)
    assert tokens[4] == ("NUMBER", 45.67)

def test_operators():
    code = "+ - * ** / == != < <= > >="
    tokens = lexer(code)
    operator_tokens = [
        ("PLUS", "+"), ("MINUS", "-"), ("STAR", "*"), ("DOUBLE_STAR", "**"),
        ("SLASH", "/"), ("EQUAL_EQUAL", "=="), ("BANG_EQUAL", "!="),
        ("LESS", "<"), ("LESS_EQUAL", "<="), ("GREATER", ">"), ("GREATER_EQUAL", ">=")
    ]
    for op in operator_tokens:
        assert op in tokens, f"Operador {op} no detectado"

def test_punctuation():
    code = "( ) ;"
    tokens = lexer(code)
    assert ("LPAREN", "(") in tokens
    assert ("RPAREN", ")") in tokens
    assert ("SEMICOLON", ";") in tokens

def test_keywords():
    code = " ".join(keywords_dict.keys())
    tokens = lexer(code)
    for word in keywords_dict.keys():
        token_type = keywords_dict[word]
        found = any(t[0] == token_type and t[1] == word for t in tokens)
        assert found, f"Palabra clave {word} no detectada correctamente"

def test_strings():
    code = '"hello" "world"'
    tokens = lexer(code)
    assert tokens[0] == ("STRING", "hello")
    assert tokens[1] == ("STRING", "world")

def test_full_expression():
    code = 'x = 5 + 3 * (2 - 1); if x >= 10: print("done")'
    tokens = lexer(code)
    expected = [
        ("IDENTIFIER", "x"), ("ASSIGN", "="), ("NUMBER", 5), ("PLUS", "+"),
        ("NUMBER", 3), ("STAR", "*"), ("LPAREN", "("), ("NUMBER", 2),
        ("MINUS", "-"), ("NUMBER", 1), ("RPAREN", ")"), ("SEMICOLON", ";"),
        ("IF", "if"), ("IDENTIFIER", "x"), ("GREATER_EQUAL", ">="),
        ("NUMBER", 10), ("COLON", ":"), ("IDENTIFIER", "print"), ("LPAREN", "("),
        ("STRING", "done"), ("RPAREN", ")")
    ]
    assert tokens == expected, f"Tokens no coinciden: {tokens}"

# Función que ejecuta todos los tests
def run_all_tests():
    test_identifiers_numbers()
    test_operators()
    test_punctuation()
    test_keywords()
    test_strings()
    test_full_expression()
    print("¡Todos los tests pasaron!")

if __name__ == "__main__":
    run_all_tests()
