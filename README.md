# **C-imple to RISC-V Compiler (Python)**

## A complete compiler, written in Python, designed to translate programs from the educational programming language C-imple into low-level RISC-V assembly code. C-imple is a simplified language, similar in structure to C , which features integer-only variables and custom control structures like switchcase, forcase, and the re-executing incase loop. It also supports parameters passed by value (in) and by reference (inout).

### **Compiler Architecture**

The compiler is implemented as a traditional multi-pass system:

•	Lexical Analyzer: Reads the C-imple source file and converts the input into meaningful tokens.

•	Syntax Analyzer: Validates the sequence of tokens against C-imple's grammatical rules.

•	Symbol Table: Manages variable, function, and parameter data using a stack-based scope structure to handle variable access in nested functions.

•	Intermediate Code Generator: Translates the parsed code into an intermediate language consisting of quads (four-part instructions similar to assembly).

•	Final Code Generator: Produces the final executable output in RISC-V assembly code (or C file) by processing the generated quads with assistance from the symbol table.
