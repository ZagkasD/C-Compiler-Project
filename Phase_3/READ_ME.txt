MUST BE RUN WITH PYTHON 3!
(ex. python3 test.py test.ci)

Known bugs:
1) The opened files (test.int, test.symb) can not be closed in the case of an error. That is because the error method is implemented in the Lex class. In order to close the files, we would need access to them from the Parser class but that is not possible, because those files are defined in the Parser class, which inherents the Lex class.

Possible solution: Create global files. In our implementation, we tried to avoid creating global fields and classes.

2) The ci_var_list is being used to store the variables and later generate the intermediate code file. The problem is that a variable is being stored in the list, each time it is used (even as a parameter). That does not effect the intermediate code in c, it just creates the same declaration many times.

Possible solution: Add if statement before the var_list.append to check if the variable has already been appended.

3) In the assembly file, the commands what should be in the main label end up in their own label, following the main. That causes no issues in the functionality