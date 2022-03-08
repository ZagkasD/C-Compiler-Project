# Zagkas Dimosthenis 4359 cse84359
# Andreou Aggelos    4628 cse84628

from lib2to3.pgen2 import token
import sys

class Token:
    def __init__(self,family=None,recognized_string=None,line_number=None):
        self._family = family
        self._recognized_string = recognized_string
        self._line_number = line_number
    
    def __str__(self):
        return (self._recognized_string+' \tfamily:"'+self._family+'", line:'+str(self._line_number))

  
class Family: 

	number      = 'number'	
	keyword     = 'keyword'	   	# if,while...
	id          = 'id'			# identifiers
	addOperator = 'addOperator'	# +,-
	mulOperator = 'mulOperator'	# *,/
	relOperator = 'relOperator'	# ==,>=,<,<>
	assignment  = 'assignmet'	# :=
	delimiter   = 'delimiter'   # ,,.,;
	groupSymbol = 'groupSymbol'	# (,),{,},[,]
	end_of_file =  9 
	'''
	number      = 0	
	keyword     = 1 # if,while...
	id          = 2	# identifiers
	addOperator = 3	# +,-
	mulOperator = 4	# *,/
	relOperator = 5	# ==,>=,<,<>
	assignment  = 6	# :=
	delimiter   = 7	# ,,.,;
	groupSymbol = 8	# (,),{,},[,]
	end_of_file = 9 
	'''


class Lex(Token):
    def __init__(self,input_file=None,file_name=None,token:Token = None,family=None,recognized_string=None,line_number=1):
        super().__init__(family, recognized_string, line_number)
        self._input_file = input_file
        self._file_name = file_name
        self._token = token

    def __del__(self):
        print('Destructor called. Lex object deleted.')

    def error(self,error_msg,line_number):
#        print("Error in file:"+sys.argv[1]+' || line:'+str(line_number)+' || '+error_msg+' << '+token_string+' >>')
        print("Error in file: testing.txt"+' || line: '+str(line_number)+' || '+error_msg)
        exit(1)


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
                if token_string in keywords:
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

            # Delimeters , ; 
            elif char == ',':
                token_string = char	
                return Token(Family.delimiter, token_string, self._line_number)
            elif char == ';':
                token_string = char 
                return Token(Family.delimiter, token_string, self._line_number)
            #EOF
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

class Parser(Lex):
    def __init__(self, family=None, recognized_string=None, line_number=None, file_name=None, token: Token = None, lexical_analyzer:Lex=None):
        super().__init__(family, recognized_string, line_number, file_name, token)
        self._lexical_analyzer = lexical_analyzer

    def program(self):
        if self._token._recognized_string == 'program':
            self.get_token()
            if self._token._family == 'id':
                self.block()
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
    
    def syntax_analyzer(self):
        self.get_token()
        self.program()
        print('Compilation successfully completed.')

    def get_token(self):
        self._token = self.next_token()

    def ifStat(self):
        self.get_token()
        if self._token._recognized_string == '(':
            self.get_token()
            self.condition()
            if self._token._recognized_string == ')':
                self.get_token()
                self.statements()
            else:
                self.error('Expected char << ) >>. Instead got {0:s}'.format(self._token._recognized_string),self._line_number)
            self.elsepart()
        else:
            self.error('Expected char << ( >>. Instead got << {0:s} >>'.format(self._token._recognized_string),self._line_number)
            
    def elsepart(self):
        if self._token._recognized_string == 'else':
            self.get_token()
            self.statements()

    def boolterm(self):
        self.boolfactor()
        while self._token._recognized_string == 'and':
            self.get_token
            self.boolfactor()

    def block(self):
        self.get_token()
        if self._token._recognized_string == '{':
            self.declarations()
            self.subprograms()
            self.blockstatements()
            if self._token._recognized_string == '}':
                self.get_token()
            else:
                curly_bracket_close = '}'
                self.error('Expected char << '+curly_bracket_close+' >>. Instead got char << {1} >>'.format(curly_bracket_close,self._token._recognized_string), self._line_number)
        else:
            curly_bracket_open = '{'
            self.error('Expected char << '+curly_bracket_open+' >>. Instead got char << {1} >>'.format(curly_bracket_open,self._token._recognized_string), self._line_number)
        
    def declarations(self):
        self.get_token()
        while self._token._recognized_string == 'declare':
            self.varlist()

    def varlist(self):
        self.get_token()
        if self._token._family == 'id':
            self.get_token()
            while self._token._recognized_string == ',':
                self.get_token()
                if self._token._family != 'id':
                    self.get_token()
                    break
                self.get_token()
            self.get_token()

    def subprograms(self): # while condition?
        pass
        
    def subprogram(self):
        self.get_token()
        if self._token._recognized_string == 'function':
            self.get_token()
            if self._token._family == 'id':
                self.get_token()
                if self._token._recognized_string == '(':
                    self.formalparlist()
                    if self._token._recognized_string != ')':
                        self.error('Expected << ) >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
                else:
                    self.error('Expected << ( >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
                self.get_token()
                self.block()
            else:
                self.error('Expected << id >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
        elif self._token._recognized_string == 'procedure':
            self.get_token()
            if self._token._family == 'id':
                self.get_token()
                if self._token._recognized_string == '(':
                    self.formalparlist()
                    if self._token._recognized_string != ')':
                        self.error('Expected << ) >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
                else:
                    self.error('Expected << ( >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
                self.get_token()
                self.block()
            else:
                self.error('Expected << id >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
        else:
            self.error('Expected << function >> or << procedure >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)

    def formalparlist(self):
        self.formalparitem()
        self.get_token()
        while self._token._recognized_string == ',':
            self.formalparitem()
            self.get_token()

    def formalparitem(self):
        self.get_token()
        if self._token._recognized_string == 'in':
            self.get_token()
            if self._token._family != 'id':
                self.error('Expected << id >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
        elif self._token._recognized_string == 'inout':
            self.get_token()
            if self._token._family != 'id':
                self.error('Expected << id >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
        else:
            self.error('Expected << in >> or << inout >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)

    def statements(self): # WRONG
        self.statement()
        self.get_token()
        if self._token._recognized_string == ';':
            return
        elif self._token._recognized_string == '{':
            self.statement()
            self.get_token()
            while self._token._recognized_string == ';':
                self.statement()
                self.get_token()
            if self._token._recognized_string != '}':
                self.error()
        else:
            self.error()
        

    def blockstatements(self):
        self.statement()
        self.get_token()
        while self._token._recognized_string == ';':
            self.statement()
            self.get_token()


    def statement(self): # whats the condition for choosing?
        self.assignStat()
        pass

    def assignStat(self):
        self.get_token()
        if self._token._family == 'id':
            self.get_token()
            if self._token._recognized_string == ':=':
                self.expression()
            else:
                self.error('Expected << := >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
        else:
            self.error('Expected << id >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)

    def whileStat(self):
        self.get_token()
        if self._token._recognized_string == 'while':
            self.get_token()
            if self._token._recognized_string == '(':
                self.condition()
                self.get_token()
                if self._token._recognized_string != ')':
                    self.error('Expected << ) >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
                self.statements()
            else:
                self.error('Expected << ( >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)
        else:
            self.error('Expected << while >>. Instead got << {0} >>'.format(self._token._recognized_string),self._line_number)

    def switchcaseStat(self):
        self.get_token()
        if self._token._recognized_string == 'switchcase':
            self.get_token()
            while self._token._recognized_string == 'case':
                self.get_token()
                if self._token._recognized_string == '(':
                    self.condition()
                    self.get_token()
                    if self._token._recognized_string != ')':
                        self.error()
                    self.statements()
                    self.get_token()
                else:
                    self.error()
            if self._token._recognized_string == 'default':
                self.statements()
            else:
                self.error()
        else:
            self.error()

    def forcaseStat(self):
        self.get_token()
        if self._token._recognized_string == 'forcase':
            self.get_token()
            while self._token._recognized_string == 'case':
                self.get_token()
                if self._token._recognized_string == '(':
                    self.condition()
                    self.get_token()
                    if self._token._recognized_string != ')':
                        self.error()
                    self.statements()
                    self.get_token()
                else:
                    self.error()
            if self._token._recognized_string == 'default':
                self.statements()
            else:
                self.error()
        else:
            self.error()

    def incaseStat(self):
        self.get_token()
        if self._token._recognized_string == 'incase':
            self.get_token()
            while self._token._recognized_string == 'case':
                self.get_token()
                if self._token._recognized_string == '(':
                    self.condition()
                    self.get_token()
                    if self._token._recognized_string == ')':
                        self.statements()
                        self.get_token()
                    else:
                        self.error()
                else:
                    self.error()
        else:
            self.error()

    def returnStat(self):
        self.get_token()
        if self._token._recognized_string == 'return':
            self.get_token()
            if self._token._recognized_string == '(':
                self.expression()
                self.get_token()
                if self._token._recognized_string != ')':
                    self.error()
            else:
                self.error()
        else:
            self.error()

    def callStat(self):
        self.get_token()
        if self._token._recognized_string == 'call':
            self.get_token()
            if self._token._family == 'id':
                self.get_token()
                if self._token._recognized_string == '(':
                    self.actualparlist()
                    self.get_token()
                    if self._token._recognized_string != ')':
                        self.error()
                else:
                    self.error()                
            else:
                self.error()
        else:
            self.error()

    def printStat(self):
        self.get_token()
        if self._token._recognized_string == 'print':
            self.get_token()
            if self._token._recognized_string == '(':
                self.expression()
                self.get_token()
                if self._token._recognized_string != ')':
                    self.error()
            else:
                self.error()
        else:
            self.error()

    def inputStat(self):
        self.get_token()
        if self._token._recognized_string == 'input':
            self.get_token()
            if self._token._recognized_string == '(':
                self.get_token()
                if self._token._family == 'id':
                    self.get_token()
                    if self._token._recognized_string != ')':
                        self.error()
                else:
                    self.error()
            else:
                self.error()
        else:
            self.error()
        pass

    def actualparitem():
        pass

    def actualparlist():
        pass

    def addoperator():
        pass

    def boolfactor():
        pass

    def condition():
        pass

    def expression():
        pass

    def factor():
        pass

    def idtail():
        pass
    
    def muloperator():
        pass

    def optionalsign():
        pass

    def reloperator():
        pass

    def term():
        pass

keywords=['program','declare','if','else','while','switchcase','forcase','incase','case','default','not','and','or','function',
		  'procedure','call','return','in', 'inout','input', 'print']

#def main(input_file):
def main():
#    input_file = open(input_file,'r')
    input_file = open('testing.txt','r')

    #l = Lex(input_file)
    #k = Token()
    p = Parser(input_file)
    
    p.syntax_analyzer()
    
    '''
    k = l.next_token()
    while k != None:
        print(k)
        k = l.next_token()
    '''

#main(sys.argv[1])
main()