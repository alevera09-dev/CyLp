class Node:
    def __repr__():
        return f"<{__class__.__name__}>"
    
    def evaluate(self):
        raise NotImplementedError

    def pretty_print(self):
        return str(self.evaluate())
    

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
        if self.operator != '-':
            raise ValueError("UnaryError: Se esperaba un operador valido.")
        return -self.node.evaluate()
    
    def pretty_print(self):
        child_str = self.node.pretty_print()
        if isinstance(self.node, (BinaryOpNode, UnaryNode)):
            child_str = f"({child_str})"
        return f"{self.operator}{child_str}"


class Parser:
    EXPR = ['PLUS',
            'MINUS']
    
    TERM = ['STAR',
            'SLASH']
    
    def __init__(self, tokens:list):
        self.tokens = tokens
        self.index = 0
        self.current_token = self.tokens[self.index]
    
    
    def eat(self):
        self.index += 1
        self.current_token = self.tokens[self.index]
    
    
    def factor(self):
        node = NumberNode(self.current_token[1])
        self.eat()
        return node
    
    def term(self):
        node = self.factor()
        
        while self.current_token[0] in self.TERM:
            op = self.current_token[1]
            self.eat()
            right = self.factor()
            node = BinaryOpNode(node, op, right)
            
        return node
    
    def expr(self):
        node = self.term()
        
        while self.current_token[0] in self.EXPR:
            op = self.current_token[1]
            self.eat()
            right = self.term()            
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
"""