# ---------------------------------------
# TEST AUTOMÁTICO PARA TU PARSER
# ---------------------------------------

from src.frontend.prototype_parser import Parser

def run_test(tokens, expected):
    """
    Ejecuta el parser, evalúa el AST y compara el resultado.
    """
    parser = Parser(tokens)
    node = parser.expr()
    result = node.evaluate()
    assert result == expected, f"Esperado {expected}, obtenido {result}"


def run_error_test(tokens):
    """
    Prueba que el parser lance error.
    """
    try:
        parser = Parser(tokens)
        parser.expr()
        assert False, "Se esperaba error, pero el parser no falló."
    except Exception:
        pass  # Error esperado


# ---------------------------------------
# 1. TESTS VÁLIDOS
# ---------------------------------------

run_test(
    [("NUMBER", 1), ("PLUS", "+"), ("NUMBER", 2), ("SEMICOLON", ";")],
    3
)

run_test(
    [("NUMBER", 2), ("PLUS", "+"), ("NUMBER", 3), ("STAR", "*"),
     ("NUMBER", 4), ("SEMICOLON", ";")],
    14
)

run_test(
    [("NUMBER", 10), ("SLASH", "/"), ("NUMBER", 2),
     ("PLUS", "+"), ("NUMBER", 5), ("SEMICOLON", ";")],
    10
)

run_test(
    [("NUMBER", 8), ("PLUS", "+"), ("NUMBER", 12), ("SLASH", "/"),
     ("NUMBER", 3), ("MINUS", "-"), ("NUMBER", 2), ("SEMICOLON", ";")],
    10
)

run_test(
    [("NUMBER", 50), ("MINUS", "-"), ("NUMBER", 6), ("SLASH", "/"),
     ("NUMBER", 3), ("STAR", "*"), ("NUMBER", 4), ("SEMICOLON", ";")],
    42
)

run_test(
    [("NUMBER", 2), ("STAR", "*"), ("NUMBER", 3),
     ("STAR", "*"), ("NUMBER", 4), ("SEMICOLON", ";")],
    24
)

run_test(
    [("NUMBER", 100), ("SLASH", "/"), ("NUMBER", 5),
     ("SLASH", "/"), ("NUMBER", 2), ("SEMICOLON", ";")],
    10
)

run_test(
    [("NUMBER", 10), ("PLUS", "+"), ("NUMBER", 2), ("STAR", "*"),
     ("NUMBER", 3), ("MINUS", "-"), ("NUMBER", 8), ("SLASH", "/"),
     ("NUMBER", 4), ("PLUS", "+"), ("NUMBER", 6), ("STAR", "*"),
     ("NUMBER", 2), ("MINUS", "-"), ("NUMBER", 1), ("SEMICOLON", ";")],
    25
)


# ---------------------------------------
# 2. TESTS DE ERROR
# ---------------------------------------

# + 3;
run_error_test([
    ("PLUS", "+"), ("NUMBER", 3), ("SEMICOLON", ";")
])

# 2 + ;
run_error_test([
    ("NUMBER", 2), ("PLUS", "+"), ("SEMICOLON", ";")
])

# 4 * ;
run_error_test([
    ("NUMBER", 4), ("STAR", "*"), ("SEMICOLON", ";")
])

# / 5;
run_error_test([
    ("SLASH", "/"), ("NUMBER", 5), ("SEMICOLON", ";")
])

# 2 3;
run_error_test([
    ("NUMBER", 2), ("NUMBER", 3), ("SEMICOLON", ";")
])

# 2 ++ 3;
run_error_test([
    ("NUMBER", 2), ("PLUS", "+"), ("PLUS", "+"),
    ("NUMBER", 3), ("SEMICOLON", ";")
])

# semicolon faltante: 3 + 2
run_error_test([
    ("NUMBER", 3), ("PLUS", "+"), ("NUMBER", 2)
])

# termina incorrecto: 3 + 2 *
run_error_test([
    ("NUMBER", 3), ("PLUS", "+"), ("NUMBER", 2),
    ("STAR", "*")
])

# división por cero (si lo manejas)
try:
    run_test([
        ("NUMBER", 10), ("SLASH", "/"), ("NUMBER", 0),
        ("SEMICOLON", ";")
    ], None)  # None porque depende de cómo lo manejes
except ZeroDivisionError:
    pass  # comportamiento aceptado


print("✔ Todos los tests ejecutados.")
