class NumberNode:
    #Atributos
    def __init__(self, value:int | float):
        self.value = value
        
    def __str__(self):
        return f"{self.value}"
        
class BinaryOpNode:
    #Atributos
    def __init__(self,  left:int|float, operator:str, right:int|float):
        self.left = left
        self.operator = operator
        self.right = right

class Parser:
    #Atributos
    def __init__(self, tokens_array: list):
        self.tokens_array = tokens_array
        self.index = 0
        self.length_array_tokens = len(tokens_array)
    
    #Metodos
    def eat(self, expected_token:str | None):
        if expected_token == self.tokens_array[self.index][0]:
            self.index += 1
        else:
            print(f"ERROR: SE ESPERABA UN {self.tokens_array[self.index][1]}")
            
    def factor(self, value:int | float):
        return NumberNode(value)

    def term(self):
        if self.tokens_array[self.index][0] == "NUMBER":
            left = self.factor(self.tokens_array[self.index][1])
            self.eat(self.tokens_array[self.index][0])
            
            if self.tokens_array[self.index][0] in ["STAR", "SLASH"]:
                operador = self.tokens_array[self.index][1]
                self.eat(self.tokens_array[self.index][0])
                right = self.factor(self.tokens_array[self.index][1])
                
                binary_op_node = BinaryOpNode(left, operador, right)

                return binary_op_node
    
    def expr(self):
        while self.index < self.length_array_tokens:
            if self.tokens_array[self.index][0] == "NUMBER":
                left = self.factor(self.tokens_array[self.index][1])
                self.eat("NUMBER")
                
            if self.tokens_array[self.index][0] in ['PLUS', 'MINUS']:
                operator = self.tokens_array[self.index][1]
                self.eat(self.tokens_array[self.index][0])
                right = self.term()

                root_node = BinaryOpNode(left, operator, right)

                return root_node

    def print_ast(self, root_node: BinaryOpNode):
        print("\t\t", root_node.operator)
        print("\n\t", root_node.left, end = "")
        print("\t\t", root_node.right.operator)
        print("\n\t\t  ", root_node.right.left, end = "")
        print("\t\t", root_node.right.right)
    
    
parser = Parser([("NUMBER", 5), ("PLUS", '+'), ("NUMBER", 3), ("STAR", '*'), ("NUMBER", 2)])
root_node = parser.expr()
print(parser.print_ast(root_node))


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