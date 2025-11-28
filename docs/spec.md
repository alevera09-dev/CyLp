# Especificación del Núcleo (spec.md)

## 1. Introducción

**Propósito:** Definir el diseño del núcleo del lenguaje: sintaxis esencial, semántica, modelo de tipos, memoria y runtime mínimo necesario para ejecutar programas simples.
**Alcance v1:** variables, expresiones, condiciones, loops, funciones, estructuras de datos (arrays, tuples, diccionarios, strings), módulos, ejecución interpretada/bytecode simple. Objetos y OOP quedan para ramificaciones.
**Nombre clave** es CyLp un nombre temporal mientras desarrollo el lenguaje y cuando lo termine pondre nombre oficial y extension(talvez icono)


## 2. Filosofía y objetivos

* Paradigma principal: **imperativo estructurado** (estilo Python/C).
* Multi-paradigma suave: funciones de primera clase; soporte futuro para prototipos/objetos.
* Modos: **modo estricto** (tipado y reglas más rígidas) y **modo prototipo** (más flexible).
* Enfoque: facilidad para aprender, rendimiento razonable y extensibilidad.

## 3. Características clave

* Tipado: **estático por defecto**, con palabra clave para tipado dinámico (`dynamic`).
* Valores primitivos: `int`, `float`, `bool`, `string`, `null`.
* Estructuras: `array`, `dict` (map), `tuple`.
* Funciones como valores (closures simples).
* Variables globales y locales.
* Módulos / import básico.

## 4. Modo de uso (ejemplo conceptual)

* Archivo de código inicia con opcional `mode strict` o `mode prototype`.
* Declaración de variables:

  * Estático: `int x = 10;`
  * Dinámico: `dynamic y = "hola";`

## 5. Diseño del Lexer

* Tokens principales:

  * `IDENTIFIER` : `[A-Za-z0-9_]`
  * `NUMBER` : enteros y flotantes
  * `STRING` : delimitadores `"..."` (escapes básicos)
  * `KEYWORDS` : `[if, elif, else, switch, case, while, for, lambda, func, do, return,` 
                  `mode, dynamic, str, int, float, bool, array, dict,`
                  `tuple, true, false, null, and, or, not]`

  * Operadores: `+ - * ** / % == != < <= > >= and or not =`
  * Delimitadores: `; , ( ) { } [ ] .`
* Comentarios:

  * Línea: `// ...`
  * Bloque: `/* ... */`


















* Reglas: ignorar whitespace salvo en tokenización; reportar errores léxicos con línea/columna.

## 6. Diseño del Parser

* Enfoque recomendado: **recursive-descent** (o Pratt para expresiones) por claridad y control.
* Producciones básicas:

  * `program -> statement*`
  * `statement -> var_decl | func_decl | expr_stmt | if_stmt | while_stmt | for_stmt | return_stmt | import_stmt`
  * `expr -> assignment | logic_or`
  * `assignment -> Identifier '=' expr`
  * `logic_or -> logic_and ( '||' logic_and )*`
  * `...` (definir precedencia para operadores aritméticos y lógicos)
* Manejo de errores: recuperación simple por `;` y llaves; mensajes con contexto.

## 7. AST (Nodos y estructura)

* Nodos sugeridos:

  * `Program` (lista de statements)
  * `FunctionDecl(name, params, body)`
  * `VarDecl(name, typeOpt, initializer)`
  * `If(cond, thenBlock, elseBlockOpt)`
  * `While(cond, body)`
  * `For(init, cond, post, body)` (opcional)
  * `Return(exprOpt)`
  * `ExprStmt(expr)`
  * `BinaryExpr(left, op, right)`
  * `UnaryExpr(op, operand)`
  * `CallExpr(callee, args)`
  * `Identifier(name)`
  * `Literal(value)`
  * `ListExpr(elements)`
  * `DictExpr(pairs)`
* Cada nodo incluye posición (line/col) para errores y tooling.

## 8. Semántica

* Alcance (scope): soportar scopes anidados (funciones crean scope). Variables globales en módulo global.
* Resolución de nombres: dos fases — resolución de símbolos (build symbol table) y chequeo semántico.
* Evaluación de expresiones: left-to-right, short-circuit para `&&`/`||`.
* Conversiones/coerciones: explícitas preferibles; definir reglas simples (ej. `int + float -> float`).

## 9. Sistema de Tipos

* Tipos básicos y combinaciones simples.
* Estático por defecto: variables declaradas con tipo requerido en `mode strict`.
* `dynamic` (o `auto`) permite tipado dinámico en `mode prototype` o localmente.
* Inferencia mínima para `auto` si implementas.
* Errores de tipo en tiempo de compilación en modo estricto; advertencias o checks en modo prototipo.

## 10. Modelo de memoria y GC

* **v1: Reference Counting (conteo de referencias)**

  * Cada objeto heap (listas, dicts, strings heap, closures) mantiene contador.
  * Al asignar/reasignar se incrementa/decrementa.
  * Liberación inmediata en contador 0.
  * Documentar riesgos: ciclos de referencia.
* **v2: Detector de ciclos**

  * Implementar un recolector de ciclos periódico para detectar y limpiar objetos en ciclos.
* **v3 opcional: Mark-and-sweep GC** para mayor rendimiento en cargas grandes.
* Nota: manejar correctamente objetos nativos y finalizadores (si los hay).

## 11. Runtime básico

* Representación `Value` unificada (tagged union) para tipos primitivos y referencias.
* Tabla de símbolos por scope.
* Stack para llamadas (frames) con referencias a variables locales y parámetros.
* Módulos como namespaces con carga perezosa (lazy import) opcional.

## 12. Librería estándar mínima (v1)

* `io` (print, read)
* `math` (abs, floor, ceil, sin, cos...)
* `string` (split, join, substr, format)
* `list` (append, remove, length, iterate)
* `dict` (get, set, keys, values)
* `time` (sleep)
* `sys` (args, exit)

## 13. Errores y mensajes

* Mensajes legibles con archivo:line:col y fragmento de línea.
* Tipos de errores: léxicos, sintácticos, semánticos, runtime (excepciones).
* Modo estricto → tratar ciertas advertencias como errores.

## 14. Modo estricto vs modo prototipo

* `mode strict` (por archivo o flag del intérprete):

  * Tipado estático obligatorio.
  * No permitir variables no declaradas.
  * Más chequeos en tiempo de parseo/semantic.
* `mode prototype`:

  * Tipado dinámico permitido.
  * Flexibilidad en coerciones.
  * Mensajes menos estrictos.

## 15. Testing

* Suite de tests unitarios del parser, lexer y runtime.
* Tests de conformance: pequeños programas con salida esperada.
* Tests de memoria: leaks y manejo de ciclos (cuando implementes detector).

## 16. Roadmap (v1 → vN)

* v1: Lexer, Parser, AST, intérprete, stdlib mínima, RC.
* v2: LSP básico, formateador, linter.
* v3: Detector de ciclos, optimizaciones, bytecode VM (opcional).
* v4: Objetos / prototipos, clases “sugar”, módulos avanzados.
* v5: IDE propio + variantes especializadas.

## 17. Documentación y ejemplos

* Incluir ejemplos por característica (variables, funciones, módulos, listas, dicts, modo strict/prototype).
* Mantener spec en Markdown en `/docs/spec.md`.

## 18. Notas de implementación (para futura conversión a C)

* Diseñar `Value` como tagged union compacto.
* Exponer API C para creación y manejo de objetos GC/RC.
* Separar capas: front-end (lexer/parser), middle (AST/semantics), back-end (runtime/VM).

---

**Fin del spec v1.**
