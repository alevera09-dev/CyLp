🌀 CyLp — Personal Learning Project

Welcome to CyLp, a project I'm building out of passion, practice, and a desire to understand how a programming language works on the inside.

This repository contains the lexer, parser, AST, and soon the interpreter/VM. It’s still a work in progress, but anyone is welcome to take a look, learn with me, or share ideas.

Warning! → The current name is just a codename. Once the project reaches a decent level, I’ll rename it to something better — either something I come up with or something chosen together with the community (if I ever get one!).

What’s a “decent level”?
When the language can do the basic essentials: variables, arithmetic operations, logic, comparisons, conditionals, and loops. After that, I want to add functions and other features to polish it.

❓ What is this language?

It’s a hybrid between C and Python, combining:

C-style { } and ; syntax

Simple Python-like functions such as print()

Static typing with a dynamic type for flexibility

Modern ideas like type inference and a prototype mode

My goal is not to replace any language:

👉 I just want to learn, improve, and have fun building something real.

🚧 Planned Features

Basic lexer — Done, but always open to improvements

Parser with AST nodes — In progress

Basic types (int, float, string, bool) — Coming soon

dynamic type — Future

Functions and {} blocks — Future

Minimal standard library (print, input, range) — Future

Control flow (if, while, for) — Future

Interpreter or virtual machine — Future

And much more!!!

✨ Example of how it might look (or how I hope it will):
 from stdmath import fact

int main() {
    int num = input("Enter a number: ");
    // I plan for the parser to automatically convert the input to the expected type (int in this case)
    print("Factorial:", fact(num));
    return 0;
}


I don’t know if I’m an old man in a young body, but I really love some parts of C’s syntax: {} for blocks, semicolons… it just feels more readable to me.
Python isn’t bad at all—in fact it’s my main language since it’s the one I started with—but C’s style has a special charm.

Another thing worth mentioning: for now I’m building the prototype of the language in my beloved Python, but later I will rebuild it in my new love, C.
If you want to follow the progress, check the /src folder.

🙌 Contributions

I’m a beginner and I’m learning, so:

👉 Any contribution is welcome
👉 If you see a bug, please open an issue
👉 If you have an idea, share it in Discussions or Issues

You don’t need experience to contribute:
if you want to learn about compilers, this repo is a fun place to experiment.

⭐ Why I'm doing this

To learn C and Python more deeply

To practice structures like ASTs, parsing, and type systems

To understand how a language works behind the scenes

Because I’m passionate about programming
