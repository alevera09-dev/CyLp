from enum import Enum, auto
from system_errors import ErrorReporter, LexerError

class TokenType(Enum):
    IF = auto()
    ELIF = auto()
    ELSE = auto()
    SWITCH = auto()
    CASE = auto()
    FOR = auto()
    WHILE = auto()
    FUNC = auto()
    DYNAMIC = auto()
    INT = auto()
    FLOAT = auto()
    BOOL = auto()
    STR = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    DOUBLE_STAR = auto()
    SLASH = auto()
    SEMICOLON = auto()
    COLON = auto()
    COMMENT = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    LBRACE = auto()
    RBRACE = auto()
    ASSIGN = auto()
    EQUAL_EQUAL = auto()
    MOD = auto()
    LESS = auto()
    GREATER = auto()
    LESS_EQUAL = auto()
    GREATER_EQUAL = auto()
    BANG_EQUAL = auto()
    IDENT = auto()
    NUMBER = auto()
    STRING = auto()
    NULL = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    NEWLINE = auto()
    EOF = auto()
    
class Token:
    def __init__(self, type:TokenType, value, column, line):
        self.type = type
        self.value = value
        self.column = str(column)
        self.line = str(line)
        
    def __repr__(self):
        return f"{self.type}({self.value})"
    
    def __str__(self):
        return f"Token de tipo {self.type} con un valor de {self.value} en la posision {self.col} col, {self.line} line"

class Lexer:
    keywords = {
        "if":TokenType.IF,
        "elif":TokenType.ELIF,
        "else":TokenType.ELSE,
        "switch":TokenType.SWITCH,
        "case":TokenType.CASE,
        "while":TokenType.WHILE,
        "for":TokenType.FOR,
        "func":TokenType.FUNC,
        "dynamic":TokenType.DYNAMIC,
        "int":TokenType.INT,
        "float":TokenType.FLOAT,
        "str":TokenType.STR,
        "bool":TokenType.BOOL,
        "null":TokenType.NULL,
        "and":TokenType.AND,
        "or":TokenType.OR,
        "not":TokenType.NOT,
    }
    
    def __init__(self, code:str, error_reporter:ErrorReporter):
        self.code: str = code
        self.error_reporter : ErrorReporter = error_reporter
        self.position: int = 0
        self.column: int = 0
        self.line: int = 1
        self.current_char: str = self.code[self.position] if code else None
        self.tokens_array: list = [] 
        self.code_length: int = len(self.code)
      
    def advance(self):
        self.position += 1
        self.column += 1
        
        if self.current_char == '\n':
            self.column = 0
            self.line += 1
            
        if self.position < self.code_length:
            self.current_char = self.code[self.position]
        else:
            self.current_char = None
    
    def _read_comments(self):  
        if self.current_char == "/":
            while self.position < self.code_length and self.current_char != '\n':
                self.advance()
        elif self.current_char == '*':
            start_comment = [self.line, self.column]
            while self.position < self.code_length:
                self.advance()
                if self.current_char == '*':
                    self.advance()
                    if self.current_char == "/":
                        self.advance()
                        return
            self.error_reporter.add_error(LexerError("Multi-line comment not closed; this closure was expected.", start_comment[0], start_comment[1], bad_char="*/"))
            return None
                         
            
    def _read_number(self):
        #Logica para identificar numeros
        start_pos = self.position
        
        while self.position < self.code_length and (self.current_char.isdigit() or self.current_char == '.'):
            self.advance()
         
        numero_completo = self.code[start_pos:self.position]
        if not '.' in numero_completo:
            numero_completo = int(numero_completo)
        else:
            numero_completo = float(numero_completo)
                
        return Token(TokenType.NUMBER, numero_completo, self.column, self.line)   #Digamos que es line 1 mientras tanto ya despues vere como calcular las lineas
        
    def _read_ident(self):
        start_pos = self.position
            
        while self.position < self.code_length and (self.current_char.isalnum() or self.current_char == '_'):
            self.advance()
                
        full_identifier = self.code[start_pos:self.position]
        if full_identifier in self.keywords.keys():
            return Token(self.keywords[full_identifier], full_identifier, self.position, 1)
        else:
            return Token(TokenType.IDENT, full_identifier, self.column, self.line)
    
    def _read_string(self):
        start_pos = self.position
        start_quotes = self.current_char
        self.advance()
        while self.position < self.code_length and self.current_char != start_quotes:
            if self.current_char == "\\":
                self.advance()
                self.advance()
                if self.position >= self.code_length or self.current_char == ';':
                    self.error_reporter.add_error(LexerError("Strange character", self.line, self.column, bad_char=f"\\{start_quotes}"))
                    return None                        
            self.advance()
            
        self.advance()
        temporal_string = self.code[start_pos:self.position]
        if temporal_string[0] != start_quotes or temporal_string[-1] != start_quotes:
            self.error_reporter.add_error(LexerError("A closing quotation mark is missing:", self.line, self.column, bad_char=f"{start_quotes}"))
            return
        if "\\n" in temporal_string:
            temporal_string = temporal_string.replace("\\n", "\n")
        if "\\t" in temporal_string:
            temporal_string = temporal_string.replace("\\t", "\t")
        if "\\\\" in temporal_string:
            temporal_string = temporal_string.replace("\\\\", "\\")
                
        temporal_string = temporal_string[1:-1]
        
        return Token(TokenType.STRING, temporal_string, self.column, self.line)

    def _read_star(self):
        start_pos = self.position
        while self.position < self.code_length and self.current_char== '*':
            self.advance()
            
        temporal_sign = self.code[start_pos:self.position]
        if temporal_sign == '*':
            token = Token(TokenType.MULT, '*', self.column, self.line)
        elif temporal_sign == "**":
            token = Token(TokenType.POW, '**', self.column, self.line)
        else:
            self.error_reporter.add_error(LexerError("Strange character", self.line, self.column, bad_char=temporal_sign))
            return None   
        return token

    def _read_equal(self):
        start_pos = self.position
        while self.position < self.code_length and self.current_char == "=":
            self.advance()
                
        temporal_sign = self.code[start_pos:self.position]
        if temporal_sign == '=':
            token = Token(TokenType.ASSIGN, '=', self.column, self.line)
        elif temporal_sign == "==":
            token = Token(TokenType.EQUAL_EQUAL, "==", self.column, self.line)  
        else:
            self.error_reporter.add_error(LexerError("Strange character", self.line, self.column, bad_char=temporal_sign))
            return None
        return token        
    
    def _read_comparison(self):
        start_pos = self.position
        while self.position < self.code_length and (self.current_char in ['<', '>', '!'] or self.current_char == '='):
            self.advance()
                          
        temporal_sign = self.code[start_pos:self.position]
        if temporal_sign == '<':
            token = Token(TokenType.LESS, '<', self.column, self.line)
        elif temporal_sign == '>':
            token = Token(TokenType.GREATER, '>', self.column, self.line)
        elif temporal_sign == '>=':
            token = Token(TokenType.GREATER_EQUAL, ">=", self.column, self.line)
        elif temporal_sign == '<=':
            token = Token(TokenType.LESS_EQUAL, "<=", self.column, self.line)
        elif temporal_sign == '!=':
            token = Token(TokenType.BANG_EQUAL, "!=", self.column, self.line)
        else:
            self.error_reporter.add_error(LexerError("Strange character", self.line, self.column, bad_char=temporal_sign))
            return None
        return token
            
    def get_tokens(self):
        while self.position < self.code_length:
            
            #Comments
            if self.current_char == '/':
                self.advance()
                if self._read_comments() == None:
                    break
                
            #Whitespaces and newlines
            if self.current_char.isspace():
                if self.current_char == '\n':
                    token = Token(TokenType.NEWLINE, '\\n', self.column, self.line)
                    self.tokens_array.append(token)
                self.advance()
                    
            #Semicolon and Colon
            elif self.current_char == ";":
                token = Token(TokenType.SEMICOLON, ';', self.column, self.line)
                self.tokens_array.append(token)
                self.advance()
            elif self.current_char == ':':
                token = Token(TokenType.COLON, ':', self.column, self.line)
                self.tokens_array.append(token)
                self.advance()
                
            #Parenthesis, Brackets and Braces
            elif self.current_char == '(':
                token = Token(TokenType.LPAREN, '(', self.column, self.line)
                self.tokens_array.append(token)
                self.advance()
            elif self.current_char == ')':
                token = Token(TokenType.RPAREN, ')', self.column, self.line)
                self.tokens_array.append(token)
                self.advance()
            elif self.current_char == "[":
                token = Token(TokenType.LBRACKET, '[', self.column, self.line)
                self.tokens_array.append(token)
                self.advance()
            elif self.current_char == "]":
                token = Token(TokenType.RBRACKET, ']', self.column, self.line)
                self.tokens_array.append(token)
                self.advance()
            elif self.current_char == "{":
                token = Token(TokenType.LBRACE, '{', self.column, self.line)
                self.tokens_array.append(token)
                self.advance()
            elif self.current_char == "}":
                token = Token(TokenType.RBRACE, '}', self.column, self.line)
                self.tokens_array.append(token)
                self.advance()
                
            #Aritmethic Operators
            elif self.current_char == '+':
                token = Token(TokenType.PLUS, '+', self.column, self.line)
                self.tokens_array.append(token)
                self.advance()
            elif self.current_char == '-':
                token = Token(TokenType.MINUS, '-', self.column, self.line)
                self.tokens_array.append(token)
                self.advance()
            elif self.current_char == '*':
                token = self._read_star()
                if token != None:
                    self.tokens_array.append(token)
            elif self.current_char == '/':
                token = Token(TokenType.SLASH, '/', self.column, self.line)
                self.tokens_array.append(token)
                self.advance()
            elif self.current_char == '%':
                token = Token(TokenType.MOD, '%', self.column, self.line)
                self.tokens_array.append(token)
            
            #Assign sign and Equal sign
            elif self.current_char == '=':
                token = self._read_equal()
                if token != None:
                    self.tokens_array.append(token)
            
            #Comparison signs, except equal
            elif self.current_char in ['<', '>', '!']:
                token = self._read_comparison()
                if token != None:
                    self.tokens_array.append(token)
            
            #Strings
            elif self.current_char.isdigit():
                token = self._read_number()
                if token != None:
                    self.tokens_array.append(token)
            
            #Identifiers and Keywords
            elif self.current_char.isalpha():
                token = self._read_ident()
                if token != None:
                    self.tokens_array.append(token)
                
            #Numbers
            elif self.current_char == "\"" or self.current_char == "\'":
                token = self._read_string()
                if token != None:
                    self.tokens_array.append(token)
            
            else:
                self.error_reporter.add_error(LexerError("Stange character", self.line, self.column, bad_char=self.current_char))
                self.advance()
              
        self.tokens_array.append(Token(TokenType.EOF, None, 0, 0))
        return self.tokens_array
            


"""
prototipo 4 mañana parche de errores de indice, cambio de logica.

Que hay de nuevo en el prototipo 4?:

    1. logica cambiada para no repetir tanto codigo
    
    2. ya no hay comprobadores de espacios en blanco dentro de los bucles internos,
       y dejo que el coprobador de espacion en el bucle externo haga el trabajo
    
    3. pongo continue en cada condicional al terminar para que suba a la siguiente iteracion de bucle while externo
       y asi no tenga que probar todos los condicionaes de abajo, esto es para mayor velocidad(creo porque solo llevo haciendo codigo desde hace 2 meses)
       pero creo que con los codigos de mas arriba se notara mas que los de abajo ya que estan mas cerca del final pero los puse hay tambien de todos modos
    
    4. trate de en los condicionales de cada comprobacion hacer condicionales que encuentre errores primero y luego con menos posibilidades de error ahora si
        haga el token, puedes verlo en la linea 33 a 41 o la linea 53 a 59
    
    5. puse las condicionales mas cortas todo arriba y las mas largas(no en codigo sino en operaciones) abajo, no se si esto ayude a la eficiencia solo
        creo que se ve mejor =)
    
    6. por ultimo cambie el nombre de el code_array a tokens_array, ademas de que cambie el formato de donde se guardan los tokens,
        pasando de una tupla de tokens, a una lista de tuplas con los tokens(idea que me dio otra ia, de hecho fue el modo ia de google)
        ejemplo = [(IDENTIFIER, a)], no se si esta es buena o es mejor la lista de tokens
    
    
    Nota para IA gemini: Estos comentarips son solo para mi y para gemini, asi que cuando veas este comentario gemini, debo decir que me siento como profesional =)
    
    Otra nota para IA gemini: en el prototipo 5 pienso poner para strings por ejemplo: si empieza con " leo todo hasta que termine con otro ", no se si esto es bueno
    o es mejor hacer los strings arrays de char, o dame un consejo de como hacerlo porfis =)
 
"""
"""
Prototipo 5, Ventisei di novembre di 2025(estoy progresando poco a poco con mi italiano =)

Cosas que han cambiado:

    1. Borre la variable contenedor_de_caracteres completamente del sistema, tambien cambie el nombre de algunas variables poniendolas en ingles.
    
    2. cambie la logica a una de slicing para intentar que no haya errores de indice.
    
    3. tambien elimine completamente char porque con la nueva tecnica de slicing no me convencia dejar la variable
    explicacion de esto: en las condiciiones de los whiles internos no podia usarlas ya que char no cambiaba con cada iteracon solo e index
    por eso ahora en los while uso code[index] asi que decidi hacerlo asi en todo a pesar de repetir codigo, es intencional.
    
    4. agregue de una vez el detector de strings, con soporte para escapes.
    
    5. CAmbie ahora si el guardado de tokens ya que aunque el prototipo pasado lo plantee se me olviso ponerlo!!!.
    
    6. Cambie la mayoria de nombres de token para que cada una cosa tenga un token diferente,
    ejemplo donde antes todos los signos de comparacion su token era COMPARISION ahora cada uno y los aritmeticos tienen su token =)
    
    7. agregue identificador para parentesis. 
"""
"""
Prototipo 6

Cambios:

    1. Cambie la logica del while interno de el identificador de signos de comparacion a uno mas sencillo y logico, con eso borre
    la lista se comparision_signs ya que ya no era necesaria.
    
    2. Cambie la logica de el detector de strings, tambien la de los escapes, segui usando replace porque no encontre(pense) otra forma de hacerlo
    no se si esto me trarea problemas cuando reescriba el lexer en C pero si no existe alguna funcuion replace la creare en su momento en C =)
    
    3. Ahora el projecto tiene un nombre clave y temporal, no sera el nombre real(oficial) ya que por el momento solo tengo cabeza para el desarrollo
    el nombre es CyLp(C de C, y de py, L de language y la p de programacion) este nombre no me gusta mucho y cuando termine el lenguaje en c y decida si
    sigo actualizandolo para algo especifico ahi si le pondre nombre dependiente a eso.
"""
"""
Prototipo 6.5(porque solo hice pequeños cambios)

    1. Arregle el error de identacion
    2. Modifica la logica de el identificador de strings
    3. agruege unas palabras claves coo mode, null, etc.
    
    #Prototipo de lexer terminado!!!
"""
"""
Prototipo 7 Totalmente actualizado y cambiado

    1.Logica pasada de una gran funcion a clases
    2. Clase TokenType para los tipos de token con libreria enum
    3. clase Token con atributos esenciales como Literal Value, TokenType, col y line(para ubicacion)
    4. clase lexer que es donde se hace magia, con la logica de def lexer pero con cosas cambiadas,
        como aumento de indice y current_char en metodo a parte, lectura de diferentes char refactorizado en diferentes metodos
        nuevos errores de sintaxis agregados con raise
         
"""
