from prototype_lexer import Token, TokenType
from system_errors import ParserError, ErrorReporter

class Node:
    def __repr__():
        return f"<{__class__.__name__}>"
    
    def evaluate(self):
        raise NotImplementedError

    def pretty_print(self):
        return str(self.evaluate())
    
class ProgramNode(Node):
    pass

class AssigmentNone(Node):
    pass

class NumberNode(Node):
    def __init__(self, value:int | float):
        self.value = value
        
    def __repr__(self):
        return f"<{__class__.__name__} value={self.value}>"
    
    def evaluate(self) -> int|float:
        if self.value is None:
            raise ValueError("ValueError: Se esperaba un valor valido")
        return self.value

    def pretty_print(self):
        return str(self.value)  
    
     
class BinaryOpNode(Node):
    #Atributos
    def __init__(self, left:Node, operator:str, right:Node):
        self.left = left
        self.operator = operator
        self.right = right
        
    def __repr__(self):
        return f"<{__class__.__name__} left={self.left} operator={self.operator} right={self.right}>"
        
    def evaluate(self) -> int|float:
        left = self.left.evaluate()
        right = self.right.evaluate()
        operator = self.operator
        
        if operator == '+':
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            return left * right
        elif operator == '/':
            if right == 0:
                raise ZeroDivisionError("No se puede dividir por cero")
            return left / right
        elif operator == "**":
            return left ** right
        elif operator == '%':
            return left % right
        else:
            raise ValueError("Se esperaba operador valido(+, -, * o /)")
        
    def pretty_print(self):
        left_str = self.left.pretty_print()
        right_str = self.right.pretty_print()
        
        if isinstance(self.left, BinaryOpNode) and self.operator in ['*', '/'] and self.left.operator in ['+', '-']:
             left_str = f"({left_str})"
             
        if isinstance(self.right, BinaryOpNode) and self.operator in ['*', '/'] and self.right.operator in ['+', '-']:
             right_str = f"({right_str})"

        return f"{left_str} {self.operator} {right_str}"
    

class UnaryNode(Node):
    def __init__(self, operator:str, node: Node):
        self.operator = operator
        self.node = node
        
    def __repr__(self):
        return f"<{__class__.__name__} operator={self.operator} value={self.node}>"

    def evaluate(self) -> int|float:
        if self.operator == '-':
            return -self.node.evaluate()
        elif self.operator == '+':
            return +self.node.evaluate()
    
    def pretty_print(self):
        child_str = self.node.pretty_print()
        if isinstance(self.node, (BinaryOpNode, UnaryNode)):
            child_str = f"({child_str})"
        return f"{self.operator}{child_str}"


class Parser:
    def __init__(self, tokens:list[Token], reporter:ErrorReporter) -> None:
        self.tokens: list[Token] = tokens
        self.position = 0
        self.current_token: Token = self.tokens[self.position] if tokens else Token(TokenType.EOF, None, 0, 0)
        self.length_list = len(self.tokens)
        self.error_reporter: ErrorReporter = reporter
    
    
    def eat(self, expected_token:TokenType) -> None:
        if self.current_token.type == expected_token:
            self.position += 1
            if self.position < self.length_list:
                self.current_token = self.tokens[self.position]
        else:
            position = {"line":self.current_token.line, "column":self.current_token.column}
            self.error_reporter.add_error(
                ParserError(
                    "Parser encontro algo inesperado",
                    position["line"],
                    position["column"],
                    expected = expected_token.value,
                    get = self.current_token.value
                    )
                )
    
    
    def at_end(self):
        return self.current_token.type == TokenType.EOF
        
    
    def factor(self):
        # Is Unary Minus?
        if self.current_token.type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            node = self.factor()
            return UnaryNode('-', node)
        
        #Is Unary Plus
        elif self.current_token.type == TokenType.PLUS:
            self.eat(TokenType.PLUS)
            node = self.factor()
            return UnaryNode('+', node)
        
        # Is a NUMBER?
        elif self.current_token.type == TokenType.NUMBER:
            node = NumberNode(self.current_token.value)
            self.eat(TokenType.NUMBER)
            return node
        
        # Is a LPAREN?
        elif self.current_token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        
        else:
            self.error_reporter.add_error(
                ParserError(
                    "Factor inesperado",
                    self.current_token.line,
                    self.current_token.column,
                    expected = "-, +, (",
                    get = self.current_token.value
                )
            )
    
    def term(self):
        node = self.power()
        
        while self.current_token.type in [TokenType.STAR, TokenType.SLASH, TokenType.MOD]:
            op = self.current_token.value
            self.eat(self.current_token.type)
            right = self.factor()
            node = BinaryOpNode(node, op, right)
            
        return node
    
    def expr(self):
        node = self.term()
        
        while self.current_token.type in [TokenType.PLUS, TokenType.MINUS]:
            op = self.current_token.value
            self.eat(self.current_token.type)
            right = self.term()            
            node = BinaryOpNode(node, op, right)
            
        return node
    
    def power(self):
        node = self.factor()
        
        while self.current_token.type == TokenType.DOUBLE_STAR:
            op = "**"
            self.eat(TokenType.DOUBLE_STAR)
            right = self.power()
            node = BinaryOpNode(node, op, right)
            
        return node


"""
Prototipo 1.

cosas a arreglar:
    
    1. la logica de eat en number, hacerlo casi igual que en el lexer(talvez),
    que cada iteracion y condicion se compare con token actual en vez de uno mayor
    talvez comparar uno por uno y guardar un 'historial' cada iteracion
    
    2. modifique todo esto que me dio dolor de cabeza !!!, dure horas para entenderlo, aunque
    este primer vistaso es mas lineal de lo que me gustaria el lexer no lo hice a la primera asi
    que espero que para al menos el prototipo 5 sea un parser decente
    
Prototipo 2.

cosas que agregue:

    1.cambie toda la logica de el parser, y agruege nodos genericos.
    
Prototipo 3:

    1. migracion de tokens, tokens string -> objects token.
"""