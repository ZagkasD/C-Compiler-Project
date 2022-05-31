# Zagkas  Dimosthenis 4359 cse84359
# Andreou Aggelos     4628 cse84628

# Must be run in python3 

import sys

# Tokens = words (or characters) from the input file 
class Token:
    def __init__(self,family=None,recognized_string=None,line_number=None):
        self._family = family
        self._recognized_string = recognized_string
        self._line_number = line_number
    
    def __str__(self):
        return (self._recognized_string+' \tfamily:"'+str(self._family)+'", line:'+str(self._line_number))

# Each token (word/character) fits into one of these categories
class Family: 

	number      = 'number'	
	keyword     = 'keyword'	   	# if,while...
	id          = 'id'			# identifiers
	addOperator = 'addOperator'	# +,-
	mulOperator = 'mulOperator'	# *,/
	relOperator = 'relOperator'	# ==,>=,<,<>,=
	assignment  = 'assignment'	# :=
	delimiter   = 'delimiter'   # ,,.,;
	groupSymbol = 'groupSymbol'	# (,),{,},[,]
	end_of_file =  9 
	
	# number      = 0	
	# keyword     = 1   # if,while,...
	# id          = 2	# identifiers
	# addOperator = 3	# +,-
	# mulOperator = 4	# *,/
	# relOperator = 5	# ==,>=,<,<>
	# assignment  = 6	# :=
	# delimiter   = 7	# ,,.,;
	# groupSymbol = 8	# (,),{,},[,]
	# end_of_file = 9 
    


class Quad:
    def __init__(self, label, op, arg1, arg2, dest):
        self.label = label
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.dest = dest
    
    def __str__(self):
            return str(self.label) + ': ' + str(self.op) + ' ' + str(self.arg1) + ' ' + str(self.arg2) + ' ' + str(
            self.dest) + '\n'







#===============================# 
#       Lexical Analyzer        #
#===============================#

# Class responsible for breaking the input file into tokens
class Lex(Token):
    def __init__(self,
        input_file=None,
        file_name=None,
        token:Token = None,
        family=None,
        recognized_string=None,
        line_number=1,
        keywords=['program','declare','if','else','while','switchcase','forcase','incase','case','default','not','and','or','function',
		  'procedure','call','return','in', 'inout','input', 'print']):
            
        super().__init__(family, recognized_string, line_number)
        self._input_file = input_file
        self._file_name = file_name
        self._token = token
        self._keywords = keywords
        

    def __del__(self):
        # Destructors manually destroy an object
        pass

    def error(self,error_msg,line_number):
        print("Error in file:"+sys.argv[1]+' || line:'+str(line_number)+' || '+error_msg)
        #print("Error in file: testing.ci"+' || line: '+str(line_number)+' || '+error_msg)
        self._input_file.close()
        exit(1)

# Each time next_token is called, it returns the next token from the input file
    def next_token(self):
        while True:
            char = self._input_file.read(1)
            
            # automaton state 0
            while char == ' ' or char == "\n" or char == "\t":
                if char == '\n':
                    self._line_number += 1
                char = self._input_file.read(1)

     		# check eof
            if not char:
                token_string = 'End Of File'
                return Token(Family.end_of_file,token_string,self._line_number)

            # automaton state 1
            # Keywords, identifiers
            elif char.isalpha():
                token_string = char
                while char.isalpha() or char.isdigit():
                    if len(token_string) > 30:
                        token_string += char
                        self.error('Length of word can not exceed 30 characters. << {0:s} >>'.format(token_string),self._line_number)
                    char = self._input_file.read(1)
                    # Need a second check for char
                    # Ex. input: i<3
                    # char = i, token_string = i, next read -> char = <
                    # without this second if statement, token_string = i<
                    if char.isalpha() or char.isdigit():
                        token_string += char
                # Backtracking
                if char != '':
                    self._input_file.seek(self._input_file.tell() - 1)
                if token_string in self._keywords:
                    return Token(Family.keyword,token_string,self._line_number)
                else:
                    return Token(Family.id,token_string,self._line_number)
            
            # automaton state 2
		    # digits
            elif char.isdigit():
                token_string = char
                while char.isdigit():
                    char = self._input_file.read(1)
                    if char.isalpha():
                        token_string += char
                        self.error("Arithmetic constants can not contain letters. << {0:s} >>".format(token_string),self._line_number)
                    if int(token_string) > (2**32 -1) or int(token_string) < (-(2**32 -1)):
                        self.error('Arithmetic constants must be within -(2^32 - 1) and (2^32 - 1).',self._line_number)
                    if char.isdigit():
                        token_string += char
                self._input_file.seek(self._input_file.tell() - 1)
                return Token(Family.number, token_string, self._line_number)

            # automaton state 3
            # char = '<'
            elif char == '<':
                token_string = char
                char = self._input_file.read(1)
                if char == '=':
                    token_string += char
                    return Token(Family.relOperator, token_string, self._line_number)
                elif char == '>':
                    token_string += char
                    return Token(Family.relOperator, token_string, self._line_number)
                else:
                    self._input_file.seek(self._input_file.tell() - 1)
                    return Token(Family.relOperator, token_string, self._line_number)

            # automaton state 4
            # char = '>'
            elif char == '>':
                token_string = char
                char = self._input_file.read(1)
                if char == '=':
                    token_string += char
                    return Token(Family.relOperator, token_string, self._line_number)
                else:
                    self._input_file.seek(self._input_file.tell() - 1)
                    return Token(Family.relOperator, token_string, self._line_number)

            # automaton state 5
            # char = ':'
            elif char == ':':
                token_string = char
                char = self._input_file.read(1)
                if char == '=':
                    token_string += char
                    return Token(Family.assignment, token_string, self._line_number)
                else:				 
                    token_string += char
                    self.error('Char << : >> must be followed by char << = >>.', self._line_number)	
                    
            # Symbols +,-,*,/,=
            elif char == '+':
                token_string  = char
                return Token(Family.addOperator, token_string, self._line_number)
                
            elif char == '-':
                token_string  = char
                return Token(Family.addOperator, token_string, self._line_number)

            elif char == '*':
                token_string  = char
                return Token(Family.mulOperator, token_string, self._line_number)
                
            elif char == '/':
                token_string  = char
                return Token(Family.mulOperator, token_string, self._line_number)
            
            elif char == '=':
                token_string  = char
                return Token(Family.relOperator, token_string, self._line_number)

            # Delimeters , ; 
            elif char == ',':
                token_string = char	
                return Token(Family.delimiter, token_string, self._line_number)
            elif char == ';':
                token_string = char 
                return Token(Family.delimiter, token_string, self._line_number)
            #EOF
            # Different than end of program (".")
            elif char == '':
                token_string = char
                return Token(Family.end_of_file, token_string, self._line_number)
            
            # Grouping Symbols
            elif char == '(':
                token_string = char
                return Token(Family.groupSymbol, token_string, self._line_number)
            elif char == ')':
                token_string = char
                return Token(Family.groupSymbol, token_string, self._line_number)
            elif char == '{':
                token_string = char
                return Token(Family.groupSymbol, token_string, self._line_number)
            elif char == '}':
                token_string = char
                return Token(Family.groupSymbol, token_string, self._line_number)
            elif char == '[':
                token_string = char
                return Token(Family.groupSymbol, token_string, self._line_number)
            elif char == ']':
                token_string = char
                return Token(Family.groupSymbol, token_string, self._line_number)

            # End of program
            elif char == '.':
                token_string = char
                return Token(Family.delimiter, token_string, self._line_number)

            # automaton state 6
            # Comments
            elif char=='#':
                char = self._input_file.read(1)
                while char !='#':
                    char = self._input_file.read(1)
                    # Counting lines in comments
                    if char == '\n':
                        self._line_number += 1
                    # If we reach eof while in comments, error
                    if char=='': 
                        self.error('Reached eof without closing comments.',self._line_number)
            else: 
                token_string = char
                self.error('Illegal character << {0:s} >>.'.format(token_string),self._line_number)











#===============================#
#     Symbol Table Classes      #
#===============================#  

# Initially, we tried to implement the compiler with object oriented architecture. Unfortunately, we had issues with the inheritance of the classes
# and their dependencies. That's why, we settled with implementing the methods inside the Parser class. Table class was not used.  
class Table(Lex):
    pass

# Scope will be used to differentiate different levels of the cimple code, depending of the functions called.
class Scope():
    def __init__(self, nesting_level = 0,):
        self._nesting_level = nesting_level  # of scopes, 0 for main program
        self._entities_list = list()         # list of entities (variables, functions, etc...) in one scope
        self._offset = 12                    # 12 bytes for return address, return value and access 

    def get_next_offset(self):
        return self._offset + 4
        
class Entity():
    def __init__(self,name = None):
        self._name = name

class Variable(Entity):
    def __init__(self, name=None, offset = 0, datatype = None):
        super().__init__(name)
        self._offset = offset     # Distance from start of activation record
        self._datatype = datatype 

class FormalParameter(Entity):
    def __init__(self, name=None, mode = None, datatype = None):
        super().__init__(name)
        self._mode = mode              # Parameter mode: cv(value), ref, ret
        self._datatype = datatype     

# Refrained from inheriting name field from Entity class. Issues with isinstance method. Check isinstance documentation. 
class Parameter():
    def __init__(self, name=None, datatype=None, offset=0, mode = None):
        self._name = name
        self._offset = offset
        self._mode = mode
        self._datatype = datatype

class TemporaryVariable(Entity):
    # Cant have Variable as parent class because isinstance method in
    # print_symbol_table wont work. Read isinstance() for info
    def __init__(self, name=None, datatype=None, offset=0):
        super().__init__(name)
        self._datatype = datatype
        self._offset = offset

# Procedure does not return a value
class Procedure(Entity):
    def __init__(self, name=None, startingQuad = None,framelength = 0, formalParameters = list()):
        super().__init__(name)
        self._startingQuad = startingQuad           # Storing the label of the quad we are about to call
        self._framelength = framelength             # Length in bytes of the activation record
        self._formalParameters = formalParameters   # List of parameters
    
# Function does return a value
class Function():
    def __init__(self, name=None, datatype = None, formalParameters=list(),startingQuad=None, framelength=0):
        self._name = name
        self._startingQuad = startingQuad
        self._framelength = framelength
        self._formalParameters = formalParameters
        self._datatype = datatype

# Constants are not part of cimple. We created this class according to the theory given
class SymbolicConstant():
    def __init__(self, name = None, datatype = None, value = 0):
        self._name = name
        self._datatype = datatype 
        self._value = value












#===============================#
#        Syntax Analyzer        #
#===============================#

# Class responsible for checking the syntax of the input file. Because of inheritance issues, we ended up implementing all the methods here.
# We have them categorized according to their job. 
class Parser(Lex):
    def __init__(self, 
        family=None,
        recognized_string=None,
        line_number=None,
        file_name=None,
        token: Token = None,
        lexical_analyzer:Lex=None,
        label_number = 0,
        quads_list = list(),
        temp_var_number = 0,
        temp_var_list =list(),
        main_program_name = None,
        main_program_starting_quad = None,
        main_program_framelength = None,
        subprogram_flag = False,
        scopes_list = list(),
        ci_var_list = list(),
        inter_code_file = None,
        symbol_table_file = None,
        assembly_file = None,
        enter_in_main = False,
        pars_list = list()):

        super().__init__(family,recognized_string,line_number,file_name,token)

        self._lexical_analyzer = lexical_analyzer
        self._label_number = label_number       # var for counting the labels of the quads
        self._quads_list = quads_list           # list of quads. Basically, this is the output of the intermediate code
        self._temp_var_number = temp_var_number # var for counting temp variables
        self._temp_var_list = temp_var_list     # list for storing temp variables
        self._main_program_name = main_program_name # necessary to differentiate all the blocks of code (functions) from the main block (main program)
        self._main_program_starting_quad = main_program_starting_quad   # same as above
        self._main_program_framelength = main_program_framelength       # same as above
        self._subprogram_flag = subprogram_flag # flag if subprograms exist. If not, can produce C file
        self._scopes_list = scopes_list         # list of scopes
        self._ci_var_list = ci_var_list         # ci variables for production of c file         
        self._inter_code_file = inter_code_file # file for intermediate code, .int file
        self._symbol_table_file = symbol_table_file # file for the symbol table, .symb file
        self._file_name = file_name             # need to name of the input file to create all the other files with the same name and different type
        self._assembly_file = assembly_file     # asm file for assembly in riskV, .asm file
        self._enter_in_main = enter_in_main     # Used as a flag in the assembly file generator
        self._pars_list = pars_list             # list of parameters for assembly file










    #===========================================#
    #           Symbol Table Methods            #
    #===========================================#

    # New entry goes to the highest scope, the scope of the last function/procedure
    def add_variable(self,var_name):
        nesting_level = self._scopes_list[-1]._nesting_level
        # Check if variable entity already declared
        for entity in self._scopes_list[nesting_level]._entities_list:
            if entity._name == var_name and entity._datatype =='Variable':
                self.error('Variable << %s >> is already declared.' %var_name, self._line_number)
        # Check if variable entity is already used as a subprogram parameter
        for entity in self._scopes_list[nesting_level]._entities_list:
            if entity._name == var_name and entity._datatype =='Parameter':
                self.error('Variable << %s >> is subprogram parameter. Can not be declared.' %var_name, self._line_number)
        # Take the offset of last scope in the scope list. That's where we want to input the new variable
        var_offset = self._scopes_list[-1]._offset
        # Append the new variable at the last scope, at last place of the entities list
        self._scopes_list[-1]._entities_list.append(Variable(var_name,var_offset,'Variable'))
        # Increase the offset of the scope, for the next input
        self._scopes_list[-1]._offset = self._scopes_list[-1].get_next_offset()

    # New entry goes to the highest scope, the scope of the last function/procedure
    # Same logic as add_variable method above
    def add_function(self,func_name,datatype):
        nesting_level = self._scopes_list[-1]._nesting_level
        # Bug here. Logically, when we create a new Function object, a new formal_par_list should be created, because that list is a field in the object.
        # For some unknown reason, when we create a new Function/Procedure object, it doesn't create a new formal_par_list,
        # instead it copies the formal_par_list() from the previous Function/Procedure objects
        # We tried to fix that by creating an empty formal_par_list and passing that as input of the Function object at its creation
        # but at no avail. We can see the bug at the c file when the same parameter for a function gets printed multiple times
        formal_par_list = []
        for entity in self._scopes_list[nesting_level]._entities_list:
            if entity._name == func_name:
                self.error('Function/Procedure << %s >> already declared.' %func_name,self._line_number)
        self._scopes_list[-1]._entities_list.append(Function(func_name,datatype,formal_par_list))

    # Add parameter to the next scope. Works with the add_formal_param method to complete a function/procedure
    def add_parameter(self, par_name,mode):
        par_offset = self._scopes_list[-1].get_next_offset()
        self._scopes_list[-1]._offset = par_offset  # update the offset of the scope
        self._scopes_list[-1]._entities_list.append(Parameter(par_name,'Parameter',par_offset,mode))

    def add_temp_variable(self,tmp_var_name):
        tmp_var_offset = self._scopes_list[-1]._offset
        self._scopes_list[-1]._entities_list.append(TemporaryVariable(tmp_var_name,'Tmp_Variable',tmp_var_offset))
        # Increase the offset of the scope, for the next input
        self._scopes_list[-1]._offset = self._scopes_list[-1].get_next_offset()
        

    # New scope for function, procedure or the main program
    def add_new_scope(self):
        if not self._scopes_list:   # If scope list is empty then it returns false
            newScope = Scope(0)     # Create the main scope of nesting level of 0
            self._scopes_list.append(newScope)
        else:   # If scope list is not empty, add scope with the next nesting level
            # new scope is on one deeper nesting level
            newScope = Scope(self._scopes_list[-1]._nesting_level + 1)
            self._scopes_list.append(newScope)
    
    def remove_scope(self):
        self._scopes_list.pop()
    
    # Update startingQuad which was not available at creation
    def update_startingQuad(self,program_name):
        starting_quad = self.nextquad() # next quad will be the block quad, aka the start of the code
        if program_name == self._main_program_name:
            # This is to check if the only block is the main program block
            # There is no need for an actual starting quad because the main block
            # will not be called from somewhere else
            # Thats why we manually set it
            self._main_program_starting_quad = starting_quad
            return starting_quad
        self._scopes_list[-2]._entities_list[-1]._startingQuad = starting_quad
        return starting_quad

    # Add parameter to the function/procedure of the previous scope. Works with the add_parameter method to complete a function/procedure
    def add_formal_param(self,par_name, mode):
        self._scopes_list[-1]._offset += 4
        self._scopes_list[-2]._entities_list[-1]._formalParameters.append(FormalParameter(par_name, mode, 'Argument'))

    # Search information at the symbol table, starting from the highest scope
    # Returns the object
    def search_entity(self,entity_name):
        if not self._scopes_list:
            # if scopes_list is empty
            self.error('Entity list is empty',0)
        for scope in self._scopes_list:
            for entity in scope._entities_list:
                if entity._name == entity_name:
                    return entity
        self.error('Entity was not found',0)

    # Writes the symbol table into the symbol table file.
    # Write happens before the removal of each scope.
    def print_symbol_table(self):
            self._symbol_table_file.write('\nSymbol Table:\n')
            # Reversed scopes_list to print the LAST scope added
            for scope in reversed(self._scopes_list):
                self._symbol_table_file.write('\n(Scope ' + str(scope._nesting_level)+')')
                for entity in scope._entities_list:
                    # Using function isinstance to check what type of object is the entity we are checking
                    # Each entity needs each own print, because of different fields
                    if isinstance(entity, Variable):
                        self._symbol_table_file.write('<---| '+str(entity._datatype) + ': \'' +str(entity._name) + '\' / offset:' + str(entity._offset)+'|')
                    elif isinstance(entity,TemporaryVariable):
                            self._symbol_table_file.write('<---| '+str(entity._datatype) + ': \'' +str(entity._name) + '\'/ offset:'+ str(entity._offset)+'|')
                    elif isinstance(entity,Parameter):
                            self._symbol_table_file.write('<---| '+str(entity._datatype) + ': \'' +str(entity._name) + '\'/ offset:' + str(entity._offset) + ' ' + str(entity._mode)+'|')
                    elif isinstance(entity,Function):
                        self._symbol_table_file.write('<---| '+str(entity._datatype) + ': \'' +str(entity._name) + '\'/ Framelength:' + str(entity._framelength) + ' / Starting Quad:' + str(entity._startingQuad)+'|')
                        if((len(entity._formalParameters))>0):
                            self._symbol_table_file.write('<Arguments: ')                 
                            for parameter in entity._formalParameters:
                                self._symbol_table_file.write(' < Name: ' + str(parameter._name) + '  Mode: ' + str(parameter._mode)+'>')
                            self._symbol_table_file.write('> ')
                    else:
                        self._symbol_table_file.write(' <Arguments: None>')
                self._symbol_table_file.write('\n')
            self._symbol_table_file.write('\n===================================================================================================================================================\n')










    #===========================================#
    #        Intermediate Code Methods          #
    #===========================================#


    def genQuad(self, op=None, arg1='_', arg2='_', dest='_'):
        new_quad = Quad(self._label_number, op, arg1, arg2, dest)
        self._label_number += 1
        self._quads_list.append(new_quad)

    def nextquad(self):
        return self._label_number

    def newTemp(self):
        new_temp_var = 'T_' + str(self._temp_var_number)
        self._temp_var_list.append(new_temp_var)
        self.add_temp_variable(new_temp_var) # Add the temp variable to symbol table
        self._temp_var_number += 1
        return new_temp_var

    def makeList(self, label):
        new_list = list()
        new_list.append(label)  # make a new list with only the label of the quad
        return new_list

    def emptyList(self):    # return an empty list where labels of quads will be stored
        return list()

    def mergeList(self,list_a, list_b):
        return list_a + list_b

    # Scan all the quads labels for those is the provided label list
    # Fill in the dest of each quad with the provided dest
    def backpatch(self, label_list, dest):
        for i in range(len(self._quads_list)):
            if self._quads_list[i].label in label_list:
                self._quads_list[i].dest = dest

    # Write the quads in the intermediate code file, after the compilation completion
    def inter_code_file_gen(self,input_file_name):
        self._inter_code_file = open(input_file_name[:-2] + 'int','w')
        for quad in self._quads_list:
            self._inter_code_file.write(quad.__str__())
        self._inter_code_file.close()
            






    #===========================================#
    #             Final Code Methods            #
    #===========================================#

    # Searches every entity in every entity list in every scope for the given entity name
    # and it returns its nesting level
    def check_nesting_level(self,entity_name):
        if not self._scopes_list:  # scopes list is empty 
            return                 
        for scope in self._scopes_list:
            for entity in scope._entities_list:
                if entity_name == entity._name:
                    return scope._nesting_level


    # Creates assembly code for transferring the ADDRESS of a non local entity into $t0 of the current nesting level
    def gnlvcode(self,variable):
        #search at symbol table for the non local variable
        foreign_entity= self.search_entity(variable)
        #search for the scope level the variable is at
        scope_levels=self._scopes_list[-1]._nesting_level - self.check_nesting_level(foreign_entity._name)
        #point to parent
        self._assembly_file.write('  lw $t0, -4($sp)\n')
        # When scope_levels = 0 then we are at the variable nesting level
        while scope_levels>0:
            #for every ancestor
            self._assembly_file.write('  lw $t0, -4($t0)\n')
            scope_levels-=1
        self._assembly_file.write('  addi $t0, $t0, -%d\n'% foreign_entity._offset)



    # Creates assembly code for transferring entity from memory to register 
    def loadvr(self,variable, register_number):
        # li is being translated from the assign (:=) command
        if str(variable).isdigit():
            self._assembly_file.write("  li t%s, %s\n" %(register_number,variable))
        else:
            # Retrieve the entity
            # The entity can be on a different nesting level (scope) from the local one (the last one)
            # We need to check that
            entity = self.search_entity(variable)

            
            # Local var or par with value or temp var
            # Massive if, need to check a lot of things
           
            # For Variable, need to check if it is variable and if the nesting level of the variable
            # is the last nesting level. That is, if it is in the scope_list[-1]. We don't need gnlvcode, we have direct access to the variable

            # For Parameter, need to check the name, the nesting level and the input mode for cv

            # For temp variable the name is good enough

            if ((entity._datatype == 'Variable' and self.check_nesting_level(variable) == self._scopes_list[-1]._nesting_level)
                 or (entity._datatype == 'Parameter' and self.check_nesting_level(variable) == self._scopes_list[-1]._nesting_level and entity._mode == 'cv')
                 or (entity._datatype == "Tmp_Variable")):
                self._assembly_file.write("  lw t%s, -%d(sp)\n" %(register_number,entity._offset))
            
            # For Parameter in the same nesting level and input mode as reference
            # Because the par is with ref, we don't have the value, but the address. We need the value.
            elif(entity._datatype == 'Parameter' and self.check_nesting_level(variable) == self._scopes_list[-1]._nesting_level and entity._mode == 'ref'):
                self._assembly_file.write('  lw $t0, -%d($sp)\n' % entity._offset) # store into t0 the address of the par
                self._assembly_file.write('  lw $t%s, ($t0)\n' % register_number)  # use that address to get the value
            
            # Local var or parameter with cv which belongs to a ancestor (nesting level smaller)
            elif((entity._datatype == 'Variable' and self.check_nesting_level(variable) < self._scopes_list[-1]._nesting_level)
                  or entity._datatype == 'Parameter' and self.check_nesting_level(variable) < self._scopes_list[-1]._nesting_level and entity._mode == 'cv'):
                self.gnlvcode(variable) # gnlvcode stores into t0 the value
                self._assembly_file.write('  lw $t%s, ($t0)\n' % register_number)

            # Parameter with ref that belongs to an ancestor (smaller nesting level)
            elif(entity._datatype == 'Parameter' and self.check_nesting_level(variable) < self._scopes_list[-1]._nesting_level and entity._mode == 'ref'):
                self.gnlvcode(variable) # gnlvcode stores into t0 the address of the par, not the value
                self._assembly_file.write('  lw $t0, ($t0)\n')
                self._assembly_file.write('  lw $t%s, ($t0)\n' % register_number)

            # Global variable. Not using the gnlvcode method to reach the main program because for 
            # deep nesting level that would have high cost. That's why we are using a specific pointer
            # to the main program. 
            elif(entity._datatype == 'Variable' and self.check_nesting_level(variable) == 0): # nesting level = 0 because it's the main program
                self._assembly_file.write('  lw $t%s, -%d($gp)\n', register_number, entity._offset)

            else:
                self.error("Error with the loadvr method in the generation of the assembly file.",0)


    # Opposite of loadvr. Creates assembly code for storing the data of the register to the memory
    def storerv(self,register_number, variable):
        #the entity for storing to the register
        entity= self.search_entity(variable)
        #1.2.3.5 global variable
        nesting_level = self.check_nesting_level(entity._name)
        if (entity._datatype=='Variable' and self.check_nesting_level(entity._name)==0):# nesting level = 0 because it's the main program
            self._assembly_file.write('  sw $t%s, -%d($s0)\n' % (register_number, entity._offset))
        #1.2.3.1 local/temp variable or standard parameter with input mode value
        elif (entity._datatype=='Variable' and self.check_nesting_level(entity._name)==self._scopes_list[-1]._nesting_level) or (entity._datatype=='Parameter' and self.check_nesting_level(entity._name)==self._scopes_list[-1]._nesting_level and entity._mode=='cv') or (entity._datatype=='Tmp_Variable'):
            self._assembly_file.write('  sw $t%s, -%d($s0)\n' % (register_number, entity._offset))
        #1.2.3.2  parameter passed with reference
        elif (entity._datatype=='Parameter' and self.check_nesting_level(entity._name)==self._scopes_list[-1]._nesting_level and entity._mode=='ref'):
            self._assembly_file.write('  lw $t0, -%d($sp)\n' % entity._offset)
            self._assembly_file.write('  sw $t%s, 0($t0)\n' % register_number)
        ##@#1.2.3.3 local var, ancestor parameter with ref
        elif (entity._datatype=='Variable' and self.check_nesting_level(entity._name)<self._scopes_list[-1]._nesting_level)or ( entity._datatype=='Parameter' and self.check_nesting_level(entity._name)<self._scopes_list[-1]._nesting_level and entity._mode=='cv'):
            self.gnlvcode(variable)
            self._assembly_file.write('  sw $t%s, ($t0)\n' % register_number)
        ##1.2.3.4 parameter with ref from ancestor
        elif (entity._datatype=='Parameter' and self.check_nesting_level(entity._name)<self._scopes_list[-1]._nesting_level and entity._mode=='ref'):
            self.gnlvcode(variable)
            self._assembly_file.write('  lw $t0, ($t0)\n')
            self._assembly_file.write('  sw $t%s, ($t0)\n' % register_number)
        else:
            self.error("Error with the storerv method in the generation of the assembly file.",0)
    



    #===========================================#
    #            Final Code Generator           #
    #===========================================#

    def final_code_generator(self,quad,block_name):
        relational_operators = ['=', '<>', '<', '>', '<=', '>=']
        cond_jump_fin_code= ['beq', 'bne', 'blt', 'bgt', 'ble', 'bge']
        arithmetic_operators = ['+', '-', '*', '/']
        ar_operators_fin_code=['add', 'sub', 'mul', 'div']
        
        # At the start of the program the code needs to jump to the to the first command of the
        # main program. Thus the first command needs to be a jump. The label of the first command
        # of the main program is not yet known, but we can place a label before that command and
        # jump to that label. The next command after the label will be the first command of the main program
        if quad.label == 0: # first quad is quads_list
            # We don't print the L0 label for them j main because
            # that would ruin the label numbering fpr the rest of the labels
            self._assembly_file.write("j Lmain\n")
        
        # Write the label
        # For the main
        # We want to print the main label only once, when we first enter the main
        # That's why we need the flag, in order to not write the main label in
        # recursive calls of the main program
        if block_name == self._main_program_name and self._enter_in_main == False:
            # When we reach the main program we need to do two actions
            # to initialize two registers, the sp and the gp for the global variables
            # sp connects to the beginning of the stack which was given by the system for our program
            # We need to place it at the beginning of the activation record of the main program
            # Between the main program (global variables) and the point we call the main program
            # all the other functions will be implemented. Thus we need to move the sp as many bytes
            # as the activation record of the main program. That's where the gp will also be.
            self._assembly_file.write("Lmain:\n")
            self._assembly_file.write("  addi $sp, $sp, %d\n" % self._main_program_framelength)
            self._assembly_file.write("  mv $gp, $sp\n")
            self._enter_in_main = True
        # For every other label
        # Bug here. The commands that should be in main, end up in their own label
        # Those labels follow the main, which doesn't cause any issues
        else: 
            self._assembly_file.write("L_"+str(quad.label)+":\n")

        # Assembly code for each block
        if quad.op == 'begin_block':
            # When we reach the main program we need to do two actions
            # to initialize two registers, the sp and the gp for the global variables
            # sp connects to the beginning of the stack which was given by the system for our program
            # We need to place it at the beginning of the activation record of the main program
            # Between the main program (global variables) and the point we call the main program
            # all the other functions will be implemented. Thus we need to move the sp as many bytes
            # as the activation record of the main program. That's where the gp will also be.
            
            # For every other function, we only need to store it's address to the ra register
            # so when the function is completed, we do jump back to the point the function was called
            if block_name != self._main_program_name:
                self._assembly_file.write("  sw $ra, -0($sp)\n")
        
        elif quad.op == 'end_block':
            # When a function is completed, we need to load the address of the command that
            # called the function into the ra and then jump to it
            if block_name != self._main_program_name:
                self._assembly_file.write("  lw $ra, -0($sp)\n")
                self._assembly_file.write("  jr $ra\n")
        
        # Halt means the main program has completed. We need to terminate the assembly file
        elif quad.op == 'halt':
            self._assembly_file.write("  li $a0, 0\n")
            self._assembly_file.write("  li $a7, 93\n")
            self._assembly_file.write("  ecall\n")
        
        #Jumps
        if(quad.op=='jump'):
            self._assembly_file.write('  j L_%d\n' %quad.dest)

        elif (quad.op in relational_operators):
            self.loadvr(quad.arg1, '1')
            self.loadvr(quad.arg2, '2')
            self._assembly_file.write('  %s $t1, $t2, L_%s\n' %((cond_jump_fin_code[relational_operators.index(quad.op)]),quad.dest))
       
        # Assignment
        elif quad.op == ':=':
            self.loadvr(quad.arg1, '0')     # load variable (arg1) into t0
            self.storerv('0', quad.dest)    # move variable into the memory
        
        #Numeric Operations
        elif quad.op in arithmetic_operators:
            self.loadvr(quad.arg1, '1')
            self.loadvr(quad.arg2, '2')
            self._assembly_file.write('  %s $t1, $t2, $t1\n'% (ar_operators_fin_code[arithmetic_operators.index(quad.op)]))
            self.storerv('1', quad.dest)

        # Return value from function
        elif quad.op == "retv":
            self.loadvr(quad.arg1, '1')
            self._assembly_file.write("  lw $t0, -8($sp)\n")
            self._assembly_file.write("  sw $t1, ($t0)\n")
        
        # Input
        elif quad.op == 'inp':
            self._assembly_file.write("  li $a7, 5\n") # standard command for input
            self._assembly_file.write("  ecall\n")        
            self._assembly_file.write("  mv  $t0, $a0\n") # move the input to t0
            self.storerv('0',quad.arg1) # store the input into the variable

        # Ouput
        elif quad.op == 'out':
            self.loadvr(quad.arg1,'0')  # load the var into t0
            self._assembly_file.write("  mv $a0, $t0\n")  # move t0 to a0
            self._assembly_file.write("  li $a7, 1\n")    # for output
            self._assembly_file.write("  ecall\n")        # for output

        # Parameter
        elif quad.op == 'par':           
            
            if block_name == self._main_program_name:
                # caller is main, nesting level is zero
                caller_nesting_lvl = 0
                framelength = self._main_program_framelength
            else:
                # if the caller is not the main program, we need to find it
                # We also need the nesting level of this entity, that's why we created a new method
                caller = self.search_entity(block_name)
                caller_nesting_lvl = self.check_nesting_level(caller._name)
                framelength = caller._framelength
           
            # If the pars_list is empty 
            if not self._pars_list:
                # Before we pass in the first parameter, we need the fp to be at the stack 
                # of the function that will be created
                self._assembly_file.write('  addi $fp, $sp, %d\n' % framelength)
            
            self._pars_list.append(quad)
            
            # The offset of each parameter needs to be at the fourth+ place of the stack
            par_offset = 12 + 4 * self._pars_list.index(quad)
           
            # Parameter with value
            if quad.arg2 == 'cv':
                self.loadvr(quad.arg1, '0') # load the value of the parameter into $t0
                # copy the value from the register to the proper place in the stack
                self._assembly_file.write("  sw $t0, -%d($fp)" % par_offset)
            
            # Parameter with reference
            elif quad.arg2 == 'ref':
                variable = self.search_entity(quad.arg1)
                var_nesting_lvl = self.check_nesting_level(quad.arg1)
                # According to theory, if the caller function is in the same nesting level
                # as the variable we are planning on passin as parameter, then we don't need
                # to use gnvlcode to get the variable
                if caller_nesting_lvl == var_nesting_lvl:
                    if variable._datatype == 'Variable' or (variable._datatype == 'Parameter' and variable._mode == 'cv'):
                        self._assembly_file.write("  addi $t0, $sp, -%d\n" %variable._offset)
                        self._assembly_file.write("  sw $t0, -%d($fp)\n" %par_offset)    
                    elif variable._datatype == 'Parameter' and variable._mode == 'ref':
                        # Take the address of the variable
                        self._assembly_file.write("  lw $t0, -%d($sp)\n" %variable._offset)
                        # Place the address of the variable in the correct place in the stack of the new function
                        self._assembly_file.write("  sw $t0, -%d($fp)\n" %par_offset)

                # If the caller function is on a different nesting level from the variable
                else:
                    if variable._datatype == 'Variable' or (variable._datatype == 'Parameter' and variable._mode == 'cv'):
                        # get the variable from the parents/main
                        self.gnlvcode(quad.arg1)
                        # Place the address of the variable in the correct place in the stack of the new function
                        self._assembly_file.write("  sw $t0, -%d($fp)\n" %par_offset)
                    elif variable._datatype == 'Parameter' and variable._mode == 'ref':
                        # get the variable from the parents/main
                        self.gnlvcode(quad.arg1)
                        self._assembly_file.write("  lw $t0, ($t0)\n")
                        # Place the address of the variable in the correct place in the stack of the new function
                        self._assembly_file.write("  sw $t0, -%d($fp)\n" %par_offset)

            elif quad.arg2 == 'ret':
                variable = self.search_entity(quad.arg1)
                self._assembly_file.write('  addi $t0, $sp, -%d\n' % variable._offset)
                self._assembly_file.write('  sw $t0, -8($fp)\n')

        #call
        elif quad.op == 'call':

            if block_name != self._main_program_name:
                caller = self.search_entity(block_name)
                caller_nesting_level = self.check_nesting_level(block_name)
                framelength = caller._framelength
            else:
                caller_nesting_level = 0
                framelength = self._main_program_framelength

            to_call = self.search_entity(quad.dest)
            to_call_nesting_level = self.check_nesting_level(quad.arg1)

            # # We need to remove from the parameter list the parameters with ret mode
            # if self._pars_list:
            #     if self._pars_list[-1].arg2 == 'ret':
            #         self._pars_list.pop()
           
            # The syntax analyzer can not find catch the error where we for example
            # call f2(in x) but function f2 doesn't have parameter
            # We catch that error here

            # arguments check
            # if len(to_call._formalParameters) != len(self._pars_list):
            #     self.error('Subprogram \'%s\' arguments do not match definition' % to_call._name, 0)

            # What about what mode the parameters are?
            # TODO check the mode of the parameters

            #IF the nesting level is the same The functions have the same parent 
            if caller_nesting_level == to_call_nesting_level:
                self._assembly_file.write('  lw $t0,-4($sp)\n' )
                self._assembly_file.write('  sw $t0,-4($sp)\n' )
           
            #IF the nesting level is the difrent The caller is to_call parent
            else:
                self._assembly_file.write('  sw $sp,-4($fp)\n' )
            #move stack pointer to to_call
            self._assembly_file.write('  addi $sp,$sp, %d\n' % framelength )
            #call the function
            #check again
            self._assembly_file.write('  jal L_%d\n' % to_call._startingQuad)

            #get the stack pointer
            self._assembly_file.write('  addi $sp, $sp, -%d\n' % framelength)
            #check inside called function beginning sw ra,(sp) and at the end lw ra,(sp)  / jr ra



    #===========================================#
    #         Syntax Analyzer Methods           #
    #===========================================#

    def syntax_analyzer(self):
        self.get_token()
        self.program()
        print('Compilation successfully completed.')

    def get_token(self):
        self._token = self.next_token()

    def program(self):
        if self._token._recognized_string == 'program':
            self.get_token()
            self._main_program_name = self._token._recognized_string # this is the program name
            if self._token._family == 'id': # program name
                self.add_new_scope()        # add the scope of the main program
                self.get_token()
                self.block(self._main_program_name)
                # check for end of program
                if self._token._recognized_string == '.':
                    self.get_token()
                    if self._token._family != 9:    # end of file
                        self.error('No characters are allowed after the fullstop, indicating the end of the program.',self._line_number)
                else:
                    self.error('Every program should end with a fullstop. Fullstop at the end is missing.',self._line_number)
            else:
                self.error('The name of the program expected, after the keyword << program >> in line << {0:d} >>. The illegal program name << {1:s} >> appeared.'.format(self._line_number,self._token._recognized_string), self._line_number)
        else:
            self.error('Keyword << program >> expected in line {0:d}. All programs should start with the keyword << program >>. Instead, the word << {1:s} >> appeared.'.format(self._line_number,self._token._recognized_string),self._line_number)

    # Each function/procedure corresponds to one block
    def block(self,program_name):
        if self._token._recognized_string == '{':
            self.get_token()
            self.declarations()
            self.subprograms()
            # update starting quad of the block, after the declaration/subprograms
            # basically when the actual code of the block (function/procedure) begins
            starting_quad = self.update_startingQuad(program_name)
           
            # This self.genQuad will be executed AFTER all the functions
            # That is because subprograms is been executed first
            self.genQuad("begin_block", program_name, "_", "_")
            self.blockstatements()
            
            # Ending the program
            if program_name is self._main_program_name:
                self.genQuad("halt", "_", "_", "_")
            self.genQuad("end_block", program_name, "_", "_") # end block

            # Setting the framelength of a function. A new function will exist in the [-2] scope
            # but its parameters and declarations will be in the [-1] scope
            # The main program is an exception because when we set its framelength,
            # there is no other scope other than the last one.
            if program_name == self._main_program_name:
                self._main_program_framelength = self._scopes_list[-1]._offset
            else:
                self._scopes_list[-2]._entities_list[-1]._framelength = self._scopes_list[-1]._offset

            # Print the symbol table before deleting the scope of the completed function
            self.print_symbol_table()

            # Update the assembly file 
            # Program name is necessary to determine if we are at the main program 
            # Need to give a starting object in quads list to work.
            # Tried it with giving 0 but doesn't work.
            for quad in self._quads_list[starting_quad:]:
                self.final_code_generator(quad,program_name)
                # Halt = end of program. After halt there is the last quad of end block
                # but that is empty, meaning we would create an empty label in the end of the assembly file
                if quad.op == 'halt':
                    break
                #pass

            # Remove scope after printing the symbol table and updating the the assembly file
            self.remove_scope()

            if self._token._recognized_string == '}':
                self.get_token()
            else:
                curly_bracket_close = '}'
                self.error('Expected char << '+curly_bracket_close+' >>. Instead got char << {1} >>'.format(curly_bracket_close,self._token._recognized_string), self._line_number)
        else:
            curly_bracket_open = '{'
            self.error('Expected char << '+curly_bracket_open+' >>. Instead got char << {1} >>'.format(curly_bracket_open,self._token._recognized_string), self._line_number)
        
    # For if statements
    def ifStat(self):
        if self._token._recognized_string == '(':
            self.get_token()
            b_true, b_false = self.condition()
            if self._token._recognized_string == ')':
                self.get_token()
                self.backpatch(b_true, self.nextquad()) # this is where the true condition goes
                self.statements()
                # ifList is needed in order to bypass the else when if condition is met
                ifList = self.makeList(self.nextquad())
                self.genQuad('jump','_','_','_')
                self.backpatch(b_false, self.nextquad())
            else:
                self.error('Expected char << ) >>. Instead got {0:s}'.format(self._token._recognized_string),self._line_number)
            # The else part of the if condition
            self.elsepart()
            # self.backpatch ifList here to bypass else when if condition is met
            self.backpatch(ifList,self.nextquad())
        else:
            self.error('Expected char << ( >>. Instead got << {0:s} >>'.format(self._token._recognized_string),self._line_number)
            
    def elsepart(self):
        if self._token._recognized_string == 'else':
            self.get_token()
            self.statements()

    # In conditions
    def boolterm(self):
        b_true,b_false = self.boolfactor()
        while self._token._recognized_string == 'and':
            self.get_token()
            self.backpatch(b_true, self.nextquad())
            q2_true, q2_false = self.boolterm()
            b_false = self.mergeList(b_false, q2_false)
            b_true = q2_true
        return b_true, b_false

    def declarations(self):
        while self._token._recognized_string == 'declare':
            self.get_token()
            self.varlist()
            if self._token._recognized_string == ';':
                self.get_token()
            else:
                self.error('Expected << ; >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
    
    # In the declarations
    def varlist(self):  
        if self._token._family == 'id':
            self._ci_var_list.append(self._token._recognized_string)
            self.add_variable(self._token._recognized_string)           # add variable in symbol table
            self.get_token()
            while self._token._recognized_string == ',':
                self.get_token()
                if self._token._family == 'id':
                    self._ci_var_list.append(self._token._recognized_string)
                    self.add_variable(self._token._recognized_string)   # add variable in symbol table
                    self.get_token()
                else:
                    self.error('Expected << id >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)                  
                

    def subprograms(self):
        while self._token._recognized_string == 'function' or self._token._recognized_string == 'procedure':
            self._subprogram_flag = True
            # Don't consume token. Need it for subprogram!!!
            self.subprogram()
    # It might be redundant to create two if statements for function and procedure
    # When they implement the same code
    # But the differentiation might be necessary later on
    def subprogram(self): 
        if self._token._recognized_string == 'function':
            self.get_token()
            function_name = self._token._recognized_string
            datatype = 'Function'
            self.add_function(function_name, datatype)
            self.add_new_scope()
            if self._token._family == 'id': # name of function
                self.get_token()
                if self._token._recognized_string == '(':
                    self.get_token()
                    self.formalparlist()
                    if self._token._recognized_string == ')':
                        self.get_token()
                    else:
                        self.error('Expected << ) >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
                else:
                    self.error('Expected << ( >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
                self.block(function_name) # begin block of function
            else:
                self.error('Expected << id >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
        elif self._token._recognized_string == 'procedure':
            self.get_token()
            procedure_name = self._token._recognized_string
            datatype = 'Procedure'
            self.add_function(procedure_name,datatype)
            self.add_new_scope()
            if self._token._family == 'id':
                self.get_token()
                if self._token._recognized_string == '(':
                    self.get_token()
                    self.formalparlist()
                    if self._token._recognized_string == ')':
                        self.get_token()
                    else:
                        self.error('Expected << ) >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
                else:
                    self.error('Expected << ( >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
                self.block(procedure_name) # begin block of procedure
            else:
                self.error('Expected << id >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
        else:
            self.error('Expected << function >> or << procedure >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)

    # Go through the parameters of a function/procedure
    def formalparlist(self):
        self.formalparitem()
        while self._token._recognized_string == ',':
            self.get_token()
            self.formalparitem()

    # For each parameter in the parameter list
    def formalparitem(self):
        if self._token._recognized_string == 'in':
            self.get_token()
            if self._token._family == 'id':
                # Add parameter to the next scope
                self.add_parameter(self._token._recognized_string,'cv')
                # Add parameter to the function/procedure of the previous scope
                self.add_formal_param(self._token._recognized_string, 'cv')
                self.get_token()
            else:
                self.error('Expected << id >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
        elif self._token._recognized_string == 'inout':
            self.get_token()
            if self._token._family == 'id':
                # Add parameter to the next scope
                self.add_parameter(self._token._recognized_string,'ref')
                # Add parameter to the function/procedure of the previous scope
                self.add_formal_param(self._token._recognized_string, 'ref')
                self.get_token()
            else:
                self.error('Expected << id >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
        elif self._token._recognized_string == ')':
            pass
        else:
            self.error('Expected << in >> or << inout >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)

    # The actual code
    def statements(self):
        if self._token._recognized_string == '{':
            self.get_token()
            self.statement()
            while self._token._recognized_string == ';':
                self.get_token()
                self.statement()
            if self._token._recognized_string == '}':
                self.get_token()
            else:
                curly_bracket_close = ''
                self.error('Expected char << '+curly_bracket_close+' >>. Instead got char << {1} >>'.format(curly_bracket_close,self._token._recognized_string), self._line_number)
        else:
            self.statement()
            if self._token._recognized_string == ';':
                self.get_token()
            else:
                self.error('Expected << ; >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)        

    # Inside a block
    def blockstatements(self):
        self.statement()
        while self._token._recognized_string == ';':
            self.get_token()
            self.statement()

    # All the different statement types
    def statement(self):
        if self._token._family == 'id':
            dest_var = self._token._recognized_string # dest variable of assign statement
            if self.search_entity(dest_var) is None:
                self.error('Undefined variable id: << %s >>.' %dest_var, self._line_number)
            self._ci_var_list.append(self._token._recognized_string)
            self.get_token()
            assign_value = self.assignStat() 
            self.genQuad(":=", assign_value, "_", dest_var)
        elif self._token._recognized_string == 'if':
            self.get_token()
            self.ifStat()
        elif self._token._recognized_string == 'while':
            self.get_token()
            self.whileStat()
        elif self._token._recognized_string == 'switchcase':
            self.get_token()
            self.switchcaseStat()
        elif self._token._recognized_string == 'forcase':
            self.get_token()
            self.forcaseStat()
        elif self._token._recognized_string == 'incase':
            self.get_token()
            self.incaseStat()
        elif self._token._recognized_string == 'call':
            self.get_token()
            proc_name = self.callStat()
            self.genQuad('call','_','_',proc_name)
        elif self._token._recognized_string == 'return':
            self.get_token()
            self.returnStat()
        elif self._token._recognized_string == 'input':
            self.get_token()
            self.inputStat()
        elif self._token._recognized_string == 'print':
            self.get_token()
            self.printStat()
        
    # Method for the assignment (:=)
    def assignStat(self):
        if self._token._recognized_string == ':=':
            self.get_token()
            return self.expression()
        else:
            self.error('Expected << := >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)

    # Method for the while statement
    def whileStat(self):
        if self._token._recognized_string == '(':
            self.get_token()
            condQuad = self.nextquad()
            b_true, b_false = self.condition()
            if self._token._recognized_string == ')':
                self.get_token()
            else:
                self.error('Expected << ) >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
            self.backpatch(b_true,self.nextquad())
            self.statements()
            self.genQuad('jump', '_', '_', condQuad)
            self.backpatch(b_false,self.nextquad())
        else:
            self.error('Expected << ( >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)

    # Method for the switchcase statement
    # Read the switchcase documentation in theory
    def switchcaseStat(self):
        exitList = self.emptyList()
        if self._token._recognized_string == 'case':
            while self._token._recognized_string == 'case':
                self.get_token()
                if self._token._recognized_string == '(':
                    self.get_token()
                    b_true, b_false = self.condition()
                    if self._token._recognized_string == ')':
                        self.get_token()
                    else:
                            self.error('Expected << ) >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
                    self.backpatch(b_true, self.nextquad())
                    self.statements()
                    t = self.makeList(self.nextquad())
                    self.genQuad('jump', '_', '_', '_')
                    exitList = self.mergeList(exitList,t)
                    self.backpatch(b_false, self.nextquad())
                else:
                    self.error('Expected << ( >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
        else:
            self.error('Expected << case >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)            
        if self._token._recognized_string == 'default':
            self.get_token()
            self.statements()
            self.backpatch(exitList,self.nextquad())
        else:
            self.error('Expected << default >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)

    # Method for the forcase statement
    # Read the forecase documentation in theory
    def forcaseStat(self):
        if self._token._recognized_string == 'case':
            firstCondQuad = self.nextquad()
            while self._token._recognized_string == 'case':
                self.get_token()
                if self._token._recognized_string == '(':
                    self.get_token()
                    b_true, b_false = self.condition()
                    if self._token._recognized_string == ')':
                        self.get_token()
                    else:
                            self.error('Expected << ) >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
                    self.backpatch(b_true, self.nextquad())
                    self.statements()
                    self.genQuad('jump', '_', '_', firstCondQuad)
                    self.backpatch(b_false, self.nextquad())
                else:
                    self.error('Expected << ( >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
        else:
            self.error('Expected << case >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)            
        if self._token._recognized_string == 'default':
            self.get_token()
            self.statements()
        else:
            self.error('Expected << default >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)

    # Method for the incase statement
    # Read the incase documentation in theory
    def incaseStat(self):
        if self._token._recognized_string == 'case':
            flag = self.newTemp()
            firstCondQuad = self.nextquad()
            self.genQuad(':=',0,'_',flag)
            while self._token._recognized_string == 'case':
                self.get_token()
                if self._token._recognized_string == '(':
                    self.get_token()
                    b_true, b_false = self.condition()
                    if self._token._recognized_string == ')':
                        self.get_token()
                    else:
                            self.error('Expected << ) >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
                    self.backpatch(b_true, self.nextquad())
                    self.statements()
                    self.genQuad(':=',1,'_',flag)
                    self.backpatch(b_false, self.nextquad())
                else:
                    self.error('Expected << ( >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
        else:
            self.error('Expected << case >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)            
        self.genQuad('=',1,'_',firstCondQuad)

    # Method for the return value of a function (procedures don't return value)
    def returnStat(self):
        if self._token._recognized_string == '(':
            self.get_token()
            ret = self.expression()
            if self._token._recognized_string == ')':
                self.genQuad('retv',ret,'_','_')
                self.get_token()
            else:
                self.error('Expected << ) >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
        else:
            self.error('Expected << ( >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)

    # Method for calling a function/procedure
    def callStat(self):
        if self._token._family == 'id':
            proc_name = self._token._recognized_string            
            if self.search_entity(self._token._recognized_string) is None:
                self.error('Undefined variable id: << %s >>.' %self._token._recognized_string, self._line_number)
            self.get_token()
            if self._token._recognized_string == '(':
                self.get_token()
                self.actualparlist()
                if self._token._recognized_string == ')':
                    self.get_token()
                    return proc_name
                else:
                    self.error('Expected << ) >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
            else:
                self.error('Expected << ( >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)                
        else:
            self.error('Expected << id >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
    
    # Method for the print statement
    def printStat(self):
        if self._token._recognized_string == '(':
            self.get_token()
            out=self.expression()
            self.genQuad('out',out,'_','_')
            if self._token._recognized_string == ')':
                self.get_token()
            else:
                self.error('Expected << ) >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
        else:
            self.error('Expected << ( >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
    
    # Method for the input statement
    def inputStat(self):
        if self._token._recognized_string == '(':
            self.get_token()
            if self._token._family == 'id':
                if self.search_entity(self._token._recognized_string) is None:
                    self.error('Undefined variable id: << %s >>.' %self._token._recognized_string, self._line_number)
                self.genQuad('inp',self._token._recognized_string,'_','_')
                self._ci_var_list.append(self._token._recognized_string)
                self.get_token()
                if self._token._recognized_string == ')':
                    self.get_token()
                else:
                    self.error('Expected << ) >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
            else:
                self.error('Expected << id >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
        else:
            self.error('Expected << ( >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)

    # Used with the call method for a function
    def actualparlist(self):
        self.actualparitem()
        while self._token._recognized_string == ',':
            self.get_token()
            self.actualparitem()

    # Actual generation of quads for the parameters
    def actualparitem(self):
        if self._token._recognized_string == 'in':
            self.get_token()
            par = self.expression()
            self.genQuad('par',par,'cv','_')
        elif self._token._recognized_string == 'inout':
            self.get_token()
            if self._token._family == 'id':
                if self.search_entity(self._token._recognized_string) is None:
                    self.error('Undefined variable id: << %s >>.' %self._token._recognized_string, self._line_number)
                self.genQuad('par',self._token._recognized_string,'ref','_')
                self.get_token()
            else:
                self.error('Expected << id >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
        elif self._token._recognized_string == ')':
            pass
        else:
            self.error('Expected << in >> or << inout >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)

    # Actual condition in every if-type method
    def condition(self):
        b_true, b_false = self.boolterm()
        while self._token._recognized_string == 'or':
            self.get_token()
            self.backpatch(b_false, self.nextquad())
            q2_true, q2_false = self.boolterm()
            b_true = self.mergeList(b_true, q2_true)
            b_false = q2_false
        return b_true, b_false

    # For boolterm, aka conditions
    def boolfactor(self):
        if self._token._recognized_string == 'not':
            self.get_token()
            if self._token._recognized_string == '[':
                self.get_token()
                b_false, b_true = self.condition() # carefull with the order of the returns. Its a NOT
                if self._token._recognized_string == ']':
                    self.get_token()
                else:
                    self.error('Expected << ] >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
            else:
                self.error('Expected << [ >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
        elif self._token._recognized_string == '[':
            self.get_token()
            b_true, b_false = self.condition()
            if self._token._recognized_string == ']':
                self.get_token()
            else:
                self.error('Expected << ] >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
        else:
            var_1 = self.expression()
            rel_op = self.reloperator()
            var_2 = self.expression()
            b_true = self.makeList(self.nextquad())
            self.genQuad(rel_op, var_1,var_2,'_')
            b_false = self.makeList(self.nextquad())
            self.genQuad('jump', '_', '_', '_')
        return b_true, b_false
    
    # The actual expression, ex. x:=expression, print(expression)
    def expression(self):
        operator = self.optionalsign()
        if operator is not None:
            arg_1 = str(operator) + str(self.term())
        else:
            arg_1 = self.term()
        while self._token._family == 'addOperator':
            operator = self.addoperator()
            arg_2 = self.term()
            temp_var = self.newTemp()
            self.genQuad(operator, arg_1, arg_2, temp_var)
            arg_1 = temp_var
        return arg_1

    # Actual term, ex term = a * b * c
    def term(self):
        arg_1 = self.factor()
        while self._token._family == 'mulOperator':
            operator = self.muloperator()
            arg_2 = self.factor()
            temp_var = self.newTemp()
            self.genQuad(operator, arg_1, arg_2, temp_var)
            arg_1 = temp_var
        return arg_1

    # Each part of term, ex term = factor * factor * factor
    def factor(self):
        if self._token._family == 'number':
            arg_1 = self._token._recognized_string
            self.get_token()
        elif self._token._recognized_string == '(':
            self.get_token()
            arg_1 = self.expression()
            if self._token._recognized_string == ')':
                self.get_token()
            else:
                self.error('Expected << ) >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
        elif self._token._family == 'id':
            arg_1 = self._token._recognized_string
            if self.search_entity(self._token._recognized_string) is None:
                self.error('Undefined variable id: << %s >>.' %self._token._recognized_string, self._line_number)
            self.get_token()
            id_list = self.idtail()
            if id_list is not None: # Id_list is not empty
                tmp_var = self.newTemp()
                self.genQuad('par',tmp_var,'ret','_')
                self.genQuad('call','_','_',arg_1)
                arg_1 = tmp_var
        else:
            self.error('Expected << number >> or << ( >> for arithmetic expression or << id >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
        return arg_1

    # Used in factor. ex x := a * b * idtail
    # factor can be a number, an expression or an id. The id part is handled by the idtail expression
    def idtail(self):
        if self._token._recognized_string == '(':
            self.get_token()
            self.actualparlist()
            if self._token._recognized_string == ')':
                self.get_token()
                return True
            else:
                self.error('Expected << ) >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)

    # In expression, for when you need to start one with a sign (ex -1)
    def optionalsign(self):
        operator = self.addoperator()
        return operator

    # ex <,>, etc
    def reloperator(self):
        rel_op = None
        if self._token._family == 'relOperator':
            rel_op = self._token._recognized_string
            self.get_token()
        return rel_op 

    # ex +,-
    def addoperator(self):
        add_operator = None
        if self._token._recognized_string == '+' or self._token._recognized_string == '-':
            add_operator = self._token._recognized_string
            self.get_token()
        # Doesn't need error. It's called from optionalSign()
        return add_operator

    # ex *,/
    def muloperator(self):
        if self._token._family == 'mulOperator':
            operator = self._token._recognized_string
            self.get_token()
        return operator


#===============================#
#       C Code Generator        #
#===============================#  

# Used in main to generate the c file
# The c file is used solely for the grading of the project by the professor.
class CCodeGenerator(Parser):
    
    def __init__(self, subprogram_flag = None,  c_code_file = None, ci_var_list = list()):
        super().__init__(ci_var_list)
        self._subprogram_flag = subprogram_flag
        self._c_code_file = c_code_file

    # The actual generator method
    def generate_code(self):
        self._c_code_file.write('#include <stdio.h>\n\n')   # the first line in a c file
        arithmetic_operators = ['+', '-', '*', '/']         # used later
        relational_operators = ['<', '>', '=', '<=', '>=', '<>']    # used later
        # The c file is being generated according to the quads
        for quad in self._quads_list:

            if quad.op == 'begin_block':
                c_variable_line = ""  # Init
                # Write the variables from the cimple file to the c
                if self._ci_var_list:
                    for ci_variable in self._ci_var_list:
                        c_variable_line = c_variable_line + ci_variable + ',' + ' '
                # Write the temp variables
                if self._temp_var_list:
                    for self._temp_variable in self._temp_var_list:
                        c_variable_line = c_variable_line + self._temp_variable + ',' + ' '
                # Begin the actual code in c
                if c_variable_line != "":
                    self._c_code_file.write('int ' + c_variable_line[:-2] + ';' + '\n\n')
                    self._c_code_file.write('int main()\n{\n')  
            # End of file
            elif quad.op == 'halt':
                self._c_code_file.write('\tL_' + str(quad.label) + ': {}' +  '  //(' + str(quad.op) + ', ' + str(quad.arg1) + ', ' + str(
                        quad.arg2) + ', ' + str(quad.dest) + ')\n')
            # Close the c file
            elif quad.op == 'end_block':
                self._c_code_file.write('}')
            # Arithmetic expressions
            elif quad.op in arithmetic_operators:
                self._c_code_file.write(
                    '\tL_' + str(quad.label) + ': ' + str(quad.dest) + '=' + str(quad.arg1) + ' ' + str(quad.op) + ' ' + str(
                        quad.arg2) + ';' + '  //(' + str(quad.op) + ', ' + str(quad.arg1) + ', ' + str(
                        quad.arg2) + ', ' + str(quad.dest) + ')\n')
            # Assignment in cimple translated in c
            elif quad.op == ':=':
                self._c_code_file.write(
                    '\tL_' + str(quad.label) + ': ' + str(quad.dest) + '=' + str(quad.arg1) + ';' + '  //(' + str(
                        quad.op) + ', ' + str(quad.arg1) + ', ' + str(quad.arg2) + ', ' + str(quad.dest) + ')\n')
            # Relational expressions in cimple translated in c
            elif quad.op in relational_operators:
                if quad.op == '=':
                    ci_relational_operator = '=='
                elif quad.op == '<>':
                    ci_relational_operator = '!='
                else:
                    ci_relational_operator = quad.op
                self._c_code_file.write('\tL_' + str(quad.label) + ': ' + 'if (' + str(quad.arg1) + ci_relational_operator + str(
                    quad.arg2) + ')' + ' goto L_' + str(quad.dest) + ';' + '  //(' + str(quad.op) + ', ' + str(
                    quad.arg1) + ', ' + str(quad.arg2) + ', ' + str(quad.dest) + ')\n')
            # Jump in cimple translated in c
            elif quad.op == 'jump':
                self._c_code_file.write(
                    '\tL_' + str(quad.label) + ': ' + 'goto L_' + str(quad.dest) + ';' + '  //(' + str(quad.op) + ', ' + str(
                        quad.arg1) + ', ' + str(quad.arg2) + ', ' + str(quad.dest) + ')\n')
            # Input in cimple translated in c
            elif quad.op == 'inp':
                self._c_code_file.write(
                    '\tL_' + str(quad.label) + ': ' + 'scanf(\"%d\"' + ', &' + str(quad.arg1) + ')' + ';' + '  //(' + str(
                        quad.op) + ', ' + str(quad.arg1) + ', ' + str(quad.arg2) + ', ' + str(quad.dest) + ')\n')
            # Output in cimple translated in c
            elif quad.op == 'out':
                self._c_code_file.write(
                    '\tL_' + str(quad.label) + ': ' + 'printf(\"''%d\\n\"' + ', ' + str(quad.arg1) + ')' + ';' + '  //(' + str(
                        quad.op) + ', ' + str(quad.arg1) + ', ' + str(quad.arg2) + ', ' + str(quad.dest) + ')\n')
            # Output in cimple translated in c
            elif quad.op == 'retv':
                self._c_code_file.write(
                    '\tL_' + str(quad.label) + ': ' + 'return ' + str(quad.arg1) + ';' + '  //(' + str(
                        quad.op) + ', ' + str(quad.arg1) + ', ' + str(quad.arg2) + ', ' + str(quad.dest) + ')\n')


def main(input_file):
#def main():

    input_file_name = input_file    # will be used to create the .int, .c, .asm, files with the same name as the input file
    input_file = open(input_file,'r')
    
    # The next two lines have being used to input a testing.ci file into the compiler without using command line input
    # That is because debugging with command line input was tricky
    # Place the next two lines in comments and uncomment the equivalent two lines from above
    #input_file_name = "testing.ci"
    #input_file = open('testing.ci','r')

    parser = Parser(input_file) 
    parser._symbol_table_file = open(input_file_name[:-2] + 'symb','w') # create a new symb file with the same name as the input file
    parser._assembly_file = open(input_file_name[:-2] + 'asm', 'w') # create a new asm file with the same name as the input file

    # Initiate syntax analysis
    parser.syntax_analyzer()

    parser.inter_code_file_gen(input_file_name)
    parser._symbol_table_file.close()
    
    # If the cimple file has no subprograms, we can create the c file
    if parser._subprogram_flag == False:
        print('C-imple file has no subprograms. Generating C file...')
        c_generator = CCodeGenerator()
        c_generator._c_code_file = open(input_file_name[:-2] + 'c', 'w')
        c_generator.generate_code()
        c_generator._c_code_file.close()
    else:
        print('C-imple file has subprograms. C file generation aborted...')

    # close opened files
    parser._assembly_file.close()
    input_file.close()

main(sys.argv[1])
#main()