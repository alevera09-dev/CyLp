🌀 CyLp — Proyecto Personal de Aprendizaje

Bienvenido a CyLp, un proyecto que estoy construyendo por pasión, por práctica y porque quiero aprender cómo funciona un lenguaje por dentro.

Este repositorio contiene el lexer, parser, AST, y próximamente el intérprete/VM.
Todavía es un trabajo en progreso, pero cualquier persona es bienvenida a verlo, aprender conmigo o dar ideas.

Cuidado! -> El nombre actual es un nombre clave por ahora, pero cuando tenga un nivel decente lo cambiare a uno que piense mejor o lo piense
con la comunidad si es que llego a tener.

Cual es un nivel decente?: Que haga lo mas basico que puede hacer un lenguaje, tener variables, hacer operaciones aritmeticas, logicas, de comparacion,
condicionales y bucles, luego de eso espero ponerle funciones entre otras cosas para pulirlo

¿Qué es este lenguaje?

Es un lenguaje híbrido entre C y Python, combinando:

Sintaxis con { } y ; inspirada en C

Funciones simples estilo Python como print()

Tipado estático con opción dynamic para más flexibilidad

Ideas modernas como inferencia de tipo y un modo prototipo

Mi objetivo no es reemplazar a ningún lenguaje:

👉 Solo quiero aprender, mejorar y divertirme construyendo algo real.

Características planeadas

Lexer básico - Listo pero siempre dispuesto a actualizarlo si se puede mejorar

Parser con nodos AST - en desarrollo

Tipos básicos (int, float, string, bool) - futuro

Tipo dynamic - futuro

Funciones y bloques {} - futuro

Librería estándar mínima (print, input, range) - futuro

Control de flujo (if, while, for) - futuro

Intérprete o máquina virtual - futuro

Y mucho mas!!!

Ejemplo de cómo se verá(O espero que se vea):
from stdmath import fact

int main() 
{
    int num = input("Digita un numero: "); #Planeo que el parser convierta el tipo de dato entrante con el que se espera como en este caso int
    print("Factorial:", fact(num));
    return 0;
}

No se si soy un viejo dentro de un cuerpo joven pero me encanta algunas cosas de la sintaxis de c como {} para bloques, semicolons, me parece mas legible a mis ojos aunque python no esta mal
y de hecho es mi lenguaje principal por asi decirlo ya que empece a aprender con el.

Otra cosa que debo decir es que por el momento estoy haciendo el prototipo del lenguaje en mi querido python pero luego lo rehare en mi nuevo amor C, si quieres ver el progreso mira la carpeta /src

🙌 Contribuciones

Soy novato y estoy aprendiendo, así que:

👉 Cualquier aporte es bienvenido
👉 Si ves un error, por favor abre un issue
👉 Si tienes una idea, déjala en Discussions o Issues

No necesitas experiencia para contribuir:
si quieres aprender sobre compiladores, este repo es un buen lugar para jugar

⭐ Por qué hago esto

Para aprender C y Python más profundamente

Para practicar estructuras como AST, parsing y tipos

Para entender cómo funciona un lenguaje detrás de escena

Porque me apasiona la programación
