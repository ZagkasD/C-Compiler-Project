# Zagkas Dimosthenis 4359 cse84359
# Andreou Aggelos    4628 cse84628

# Test

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

    def error(self,error_msg,line_number,token_string):
        print("Error in file:"+sys.argv[1]+' || line:'+str(line_number)+' || '+error_msg+' << '+token_string+' >>')
#        print("Error in file: testing.txt"+' || line: '+str(line_number)+' || << '+token_string+' >> '+error_msg)
        exit(1)

    def error_simple(self,error_msg,line_number):
        print("Error in file:"+sys.argv[1]+' || line:'+str(line_number)+'||'+error_msg)
#        print("Error in file: testing.txt"+' || line: '+str(line_number)+' || '+error_msg)
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
                break

            # automaton state 1
            # Keywords, identifiers
            elif char.isalpha():
                token_string = char
                while char.isalpha() or char.isdigit():
                    if len(token_string) > 30:
                        token_string += char
                        self.error('Length of word can not exceed 30.',self._line_number,token_string)
                    char = self._input_file.read(1)
                    # Need a second check for char
                    # Ex. input: i<3
                    # char = i, token_string = i, next read -> char = <
                    # without this second if statement, token_string = i<
                    if char.isalpha() or char.isdigit():
                        token_string += char
                # Backtracking
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
                        self.error("Arithmetic constants can not contain letters.",self._line_number,token_string)
                    if int(token_string) > (2**32 -1) or int(token_string) < (-(2**32 -1)):
                        self.error_simple('Arithmetic constants must be within -(2^32 - 1) and (2^32 - 1)',self._line_number)
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
                    self.error_simple('Char << : >> must be followed by char << = >>', self._line_number)	
                    
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
                        self.error_simple('Reached eof without closing comments',self._line_number)
            else: 
                token_string = char
                self.error('Illegal character',self._line_number,token_string)

class Parser(Lex):
    def __init__(self, family=None, recognized_string=None, line_number=None, file_name=None, token: Token = None, lexical_analyzer:Lex=None):
        super().__init__(family, recognized_string, line_number, file_name, token)
        self._lexical_analyzer = lexical_analyzer

keywords=['program','declare','if','else','while','switchcase','forcase','incase','case','default','not','and','or','function',
		  'procedure','call','return','in', 'inout','input', 'print']

def main(input_file):
#def main():
    input_file = open(input_file,'r')
#    input_file = open('testing.txt','r')

    l = Lex(input_file)
    k = Token()
    k = l.next_token()
    while k != None:
        print(k)
        k = l.next_token()

main(sys.argv[1])
#main()