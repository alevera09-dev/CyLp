def lexer(code:str) -> list:
    tokens_array = []
    index = 0
    keywords = {
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
        "return" : "RETURN",
        "lambda" : "LAMBDA",
        "or" : "OR",
        "and" : "AND",
        "not" : "NOT",
        "null" : "NULL",
        "mode" : "MODE"
    }
    line_length = len(code)
    
    while index < line_length:
        
        #Es un espacio 
        if code[index] == ' ':
            index += 1
            continue
        
        #Logica para dentificar semicolon            
        if code[index] == ";":
            tokens_array.append(("SEMICOLON", ";"))
            index += 1
            continue
        
        #Logica para identificar colon
        if code[index] == ':':
            tokens_array.append(("COLON", ":"))
            index += 1
            continue
        
        #Logica para identificar parentesis, brackets y curly braces
        if code[index] == '(':
            tokens_array.append(("LPAREN", f"{code[index]}"))
            index += 1
            continue
        
        if code[index] == ')':
            tokens_array.append(("RPAREN", f"{code[index]}"))
            index += 1
            continue
        
        if code[index] == "[":
            tokens_array.append(("LBRACKET", f"{code[index]}"))
            index += 1
            continue
        
        if code[index] == "]":
            tokens_array.append(("RBRACKET", f"{code[index]}"))
            index += 1
            continue
        
        if code[index] == "{":
            tokens_array.append(("LBRACE", f"{code[index]}"))
            index += 1
            continue
        
        if code[index] == "}":
            tokens_array.append(("RBRACE", f"{code[index]}"))
            index += 1
            continue
        
        #Logica de identificador de signos aritmeticos
        if code[index] == '+':
            tokens_array.append(("PLUS", f"{code[index]}"))
            index += 1
            continue
        
        if code[index] == '-':
            tokens_array.append(("MINUS", f"{code[index]}"))
            index += 1
            continue
        
        if code[index] == '*':
            start_pos = index
            while index < line_length and code[index] == '*':
                index += 1
            
            temporal_sign = code[start_pos:index]
            if temporal_sign == '*':
                tokens_array.append(("STAR", f"{temporal_sign}"))
            elif temporal_sign == "**":
                tokens_array.append(("DOUBLE_STAR", f"{temporal_sign}"))
            else:
                print("ERROR EN SIGNO DE MULT, POW")      
            continue
        
        if code[index] == '/':
            tokens_array.append(("SLASH", f"{code[index]}"))
            index += 1
            continue
        
        if code[index] == '%':
            tokens_array.append(("MOD", f"{code[index]}"))
            index += 1
            continue
                 
        #Logica de signo de asignacion o igual (=, ==)
        if code[index] == '=':
            start_pos = index
            while index < line_length and code[index] == '=':
                index += 1
                
            temporal_sign = code[start_pos:index]
            if temporal_sign == '=':
                tokens_array.append(("ASSIGN", "="))
            elif temporal_sign == "==":
                tokens_array.append(("EQUAL_EQUAL", "=="))    
            else:
                print("ERROR EN SIGNOS DE ASIGNACION Y COMPARCION") #Gemini este mensaje es para mi asi que no le prestees atencion
            
            continue
                           
        #Logica para identificar signos de comparacion a excepcion de ==
        if code[index] in ['<', '>', '!']:
            start_pos = index
            while index < line_length and (code[index] in ['<', '>', '!'] or code[index] == '='):
                index += 1
                          
            temporal_sign = code[start_pos:index]
            if temporal_sign == '<':
                tokens_array.append(("LESS", f"{temporal_sign}"))
            elif temporal_sign == '>':
                tokens_array.append(("GREATER", f"{temporal_sign}"))
            elif temporal_sign == '>=':
                tokens_array.append(("GREATER_EQUAL", f"{temporal_sign}"))
            elif temporal_sign == '<=':
                tokens_array.append(("LESS_EQUAL", f"{temporal_sign}"))
            elif temporal_sign == '!=':
                tokens_array.append(("BANG_EQUAL", f"{temporal_sign}"))
            else:
                print("ERROR EN SIGNOS DE COMPARASION") #Gemini este mensaje es para mi asi que no le prestees atencion
            
            continue
                                          
        #Logica para identificar identificadores de variables
        if code[index].isalpha():
            start_pos = index
            
            while index < line_length and (code[index].isalnum() or code[index] == '_'):
                index += 1
                
            full_identifier = code[start_pos:index]
            if full_identifier in keywords.keys():
                tokens_array.append((f"{keywords[full_identifier]}",  f"{full_identifier}"))
            else:
                tokens_array.append(("IDENTIFIER",  f"{full_identifier}"))
            continue
            
        #Logica para identificar numeros
        if code[index].isdigit():
            start_pos = index
            while index < line_length and (code[index].isdigit() or code[index] == '.'):
                index += 1
                
            numero_completo = code[start_pos:index]
            if not '.' in numero_completo:
                numero_completo = int(numero_completo)
            else:
                numero_completo = float(numero_completo)
                
            tokens_array.append(("NUMBER", numero_completo))
            continue
        
        #Logica para identificador de strings
        if code[index] == "\"" or code [index] == "\'":
            start_pos = index
            start_quotes = code[index]
            index += 1
            while index < line_length and code[index] != start_quotes:
                if code[index] == "\\":
                    index += 2
                    if index >= line_length:
                        print("ERROR DE STRING, talvez hiciste esto? = \\\" o \\' al final del string en vez de solo \" o ' ")
                        break
                                             
                index += 1
            
            index += 1
            temporal_string = code[start_pos:index]
            if "\\n" in temporal_string:
                temporal_string = temporal_string.replace("\\n", "\n")
            elif "\\t" in temporal_string:
                temporal_string = temporal_string.replace("\\t", "\t")
            elif "\\\\" in temporal_string:
                temporal_string = temporal_string.replace("\\\\", "\\")
                
            temporal_string = temporal_string[1:-1]
            tokens_array.append(("STRING", f"{temporal_string}")) 
                    
            continue
            
    return tokens_array


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
"""