#  A Python-bytecode interpreter implementation

> If you don’t know how compilers work, then you don’t know how computers work. If you’re not 100% sure whether you know how compilers work, then you don’t know how they work.” — Steve Yegge



## Goal
To write an implementation of a python interpreter in a language of choice.  
**Directly execute intermediate bytecode.** Use CPython to generate the intermediary bytecode and use it as input to our interpreter. This allows us to skip semantic and syntactic analysis.

Language choices:
 - **Portabiliy** ( Java/C# - Mono)
 - **Speed** (C, C++, Rust)
 - *Simplicity* (Pypy - JIT)
 


 ## Roadmap
 > You must have a map, no matter how rough. Otherwise you wander all over the place. In The Lord of the Rings I never made anyone go farther than he could on a given day.  
> \- J.R.R. Tolkien

![](https://craftinginterpreters.com/image/a-map-of-the-territory/mountain.png)


## Resources
* https://craftinginterpreters.com/
* https://docs.python.org/3/
* https://en.wikipedia.org/wiki/Compilers:_Principles,_Techniques,_and_Tools
* http://doc.pypy.org/en/latest/interpreter.html
* CPython internals lectures
