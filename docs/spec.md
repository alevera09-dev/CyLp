# CyLp Language Specification  
### **Version: v0.1**

> CyLp es un lenguaje experimental diseñado para ofrecer la familiaridad de C, la flexibilidad y sencillez de Python, y una base sólida para computación de alto rendimiento, machine learning, robótica y programación concurrente moderna.

---

# 📌 1. Filosofía del lenguaje

CyLp se diseña siguiendo estos principios:

- **Familiaridad** para usuarios de C y Python  
- **Compilado y eficiente**, con implementación final en C  
- **Sintaxis clara** basada en C como estándar  
- **Opcionalmente indentada**, estilo Python  
- **Tipado híbrido con inferencia**  
- **Soporte dinámico mediante `dynamic`**  
- **Simplicidad para principiantes**, potencia para expertos  
- **Punteros seguros**, con `unsafe` explícito  
- **Concurrencia moderna**, basada en paso de mensajes  
- **Macros higiénicas estilo Rust**  
- **Foco en ML, GPU y robótica** para futuro uso profesional  

---

# 📌 2. Sintaxis general

CyLp permite **dos estilos sintácticos**:

## ✔ A) Estilo C (estándar)

```c
func main(void) -> int {
    print("Hola mundo");
    return 0;
}
```

## ✔ B) Estilo Python (opcional)

Activado con `:`

```py
func main(void) -> int:
    print("Hola mundo");
    return 0
```

---

## ✔ Reglas clave

- **El ; es opcional**
- **La indentación solo funciona si una línea termina en `:`**
- **No se mezclan estilos dentro de una misma estructura**
- **El archivo puede contener ambos estilos**

---

# 📌 3. Tipos de datos

# Tipos soportados:

- **int: Entero**
- **float: Decimal**
- **bool: Booleano**
- **str: Cadena UTF-8**
- **array: Arreglo homogéneo**
- **dynamic: Tipo dinámico e inferido**
- **dict<K,V>: Diccionario genérico**
- **void: Sin retorno**
- **null: Puntero nulo**
. **none: Valor vacío seguro**

---

# 📌 4. Sistema de Tipos

CyLp usa un sistema híbrido con inferencia:
- **Estático por defecto**
- **Dinámico cuando se usa dynamic**
- **El compilador infiere tipos automáticamente**

# Ejemplos:

```
int numero = 50;
str nombre = "Harvard";
bool casado = false;

dynamic x = 20;
x = "20";         // válido

numero = "50";    // ERROR
```

---

# 📌 5. Declaración de variables

# ✔ Variables estándar

**tipo identificador = valor;**

```
int numero = 50;
str nombre = "Harvard";
bool casado = false;
```

# ✔ Variables dinámicas

```
dynamic x = 50;
x = "Hola";   // válido
```

# ✔ Error típico

```
int edad = "20"; // ERROR
```

---

# 📌 6. Estructuras de datos

## Formato general:

**tipo tipo_de_estructura identificador = valor;**

## ✔ Arrays Homogéneos:
```
int array numeros = [1, 2, 3, 4, 5];
````

## Dinámicos:
```
dynamic array lista = [1, "2", true, 0.4, "Alex", [1, 2, 3]];
```

## ✔ Diccionarios (generics)
```
dict<str, int> phonebook = {
    "Alex": 1932394055,
    "Maria": none
};
```

## Diccionarios dinámicos
```
dict<dynamic, dynamic> person = {
    "nombre": "John",
    "edad": 26,
    "casado": true
};
```

---

# 📌 7. Funciones

## Sintaxis:

```
func nombre(parametros) -> tipo {
    ...
}
```

**func obligatorio**
**-> tipo obligatorio**
**return opcional**

## Ejemplo:

```
func add(int a, int b) -> int {
    return a + b;
}
```

## Indentado:

```
func add(int a, int b) -> int:
    return a + b
```

---

# 📌 8. Entrada y Salida

```
print("Hola");
input("Nombre: ")
```

---

# 📌 9. Control de flujo

## Estilo C/Python con {}
```
if x > 10 {
    ...
} elif x == 10 {
    ...
} else {
    ...
}

while cond { ... }

for i in range(10) { ... }

do {
    ...
} while cond;
```

## Estilo indentado
```
if x > 10:
    print("Mayor")
```

---

## 📌 10. Comentarios
```
// Comentario de una línea
/*
   Comentario de múltiples líneas
*/
```

---

## 📌 11. Punteros y seguridad

# CyLp tiene punteros seguros:

```
unsafe {
    pointer<int> p = &x;
    *p = 20;
}
```
**unsafe obligatorio para desreferenciar**
**pointer<T> es el tipo de puntero moderno**

---

## 📌 12. Concurrencia

# Modelo inspirado en Go: paso de mensajes.
```
spawn worker();
channel<int> ch;

ch.send(42);
```

---

## 📌 13. Macros

# Macros higiénicas (como Rust):
```
macro repeat(n, body) {
    for (int i = 0; i < n; i++) {
        body();
    }
}
```

---

## 📌 14. Módulos y paquetes

# CyLp no usa #include.
```
import math;
import io;
import ml;
```

---

## 📌 15. Machine Learning, GPU y Robótica
# ✔ Integración con Python ML stack:

- **TensorFlow**
- **NumPy**
- **PyTorch**
- **SciPy**
 
**Mediante API C/Python y una capa nativa de alto nivel.**

# ✔ GPU

- **CUDA/OpenCL**
- **Tensores acelerados**
- **Backend optimizado**

# ✔ Robótica

# A definir, pero con base para:

- **Sensores**
- **Actuadores**
- **Tiempo real ligero**
- **Comunicación**

---

## 📌 16. Implementación

# Prototipo actual

- **Python**
- **Lexer**
- **Parser**
- **AST**
- **Intérprete básico**

# Implementación final

- **Compilador en C**
- **VM propia**
- **Backend C**
- **Optimizaciones avanzadas**
- **Sistema de módulos**

  ---

  
