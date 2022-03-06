# Zagkas Dimosthenis 4359 cse84359
# Andreou Aggelos    4628 cse84628
import sys

class Token:
	# properties: family, recognized_string, line_numbers
	def __init__(self, family_type, recognized_string, line_number):
		self.family_type = family_type
		self.recognized_string = recognized_string
		self.line_number = line_number

	def set_family_type(self, family_type):
		self.family_type = family_type

class Family: 

	number = 'number'	
	keyword = 'keyword'		# if,while...
	id = 'id'			# identifiers
	addOperator = 'addOperator'	# +,-
	mulOperator = 'mulOperator'	# *,/
	relOperator = 'relOperator'	# ==,>=,<,<>
	assignment = 'assignmet'	# :=
	delimiter = 'delimiter'	# ,,.,;
	groupSymbol = 'groupSymbol'	# (,),{,},[,]
	end_of_file = 9 
	'''
	number = 0	
	keyword = 1		# if,while...
	id = 2			# identifiers
	addOperator = 3	# +,-
	mulOperator = 4	# *,/
	relOperator = 5	# ==,>=,<,<>
	assignment = 6	# :=
	delimiter = 7	# ,,.,;
	groupSymbol = 8	# (,),{,},[,]
	end_of_file = 9 
	'''

keywords=['program','declare','if','else','while','switchcase','forcase','incase','case','default','not','and','or','function',
		  'procedure','call','return','in', 'inout','input', 'print']

# Global Variables
line_number = 1
token = Token(None,None,None)

# argv[1] is the first console argument, aka file name
def error( error_msg,line_number):
	#print("Error in file:",sys.argv[1],'||','line:', line_number,'||', error_msg)
	print("Error in file: testing.txt",'||','line:', line_number,'||', error_msg)
	exit(1)

#========================
#      Lex Analyzer
#========================

def lex(input_file):
	global line_number
	while True: 
	
		# read first character
		char = input_file.read(1)

		# automaton state 0
		while char == ' ' or char == "\n" or char == "\t":
			if char == '\n':
				line_number += 1
			char = input_file.read(1)

		# check eof
		if not char:
			break

		# automaton state 1
		# Keywords, identifiers
		elif char.isalpha():
			token_string = char
			while char.isalpha() or char.isdigit():
				if len(token_string) > 30:
					error('Length of word can not exceed 30.',line_number)
				char = input_file.read(1)
				# Need a second check for char
				# Ex. input: i<3
				# char = i, token_string = i, next read -> char = <
				# without this second if statement, token_string = i<
				if char.isalpha() or char.isdigit():
					token_string += char
			# Backtracking
			input_file.seek(input_file.tell() - 1)
			if token_string in keywords:
				return Token(Family.keyword,token_string,line_number)
			else:
				return Token(Family.id,token_string,line_number)

		# automaton state 2
		# digits
		elif char.isdigit():
			token_string = char
			while char.isdigit():
				char = input_file.read(1)
				if char.isalpha():
					error("Arithmetic constants can not contain letters.", line_number)
				if int(token_string) > (2**32 -1) or int(token_string) < (-(2**32 -1)):
					error('Arithmetic constants must be within -(2^32 - 1) and (2^32 - 1)')
				if char.isdigit():
					token_string += char
			input_file.seek(input_file.tell() - 1)
			return Token(Family.number, token_string, line_number)

		# automaton state 3
		# char = '<'
		elif char == '<':
			token_string = char
			char = input_file.read(1)
			if char == '=':
				token_string += char
				return Token(Family.relOperator, token_string, line_number)
			elif char == '>':
				token_string += char
				return Token(Family.relOperator, token_string, line_number)
			else:
				input_file.seek(input_file.tell() - 1)
				return Token(Family.relOperator, token_string, line_number)

		# automaton state 4
		# char = '>'
		elif char == '>':
			token_string = char
			char = input_file.read(1)
			if char == '=':
				token_string += char
				return Token(Family.relOperator, token_string, line_number)
			else:
				input_file.seek(input_file.tell() - 1)
				return Token(Family.relOperator, token_string, line_number)

		# automaton state 5
		# char = ':'
		elif char == ':':
			token_string = char
			char = input_file.read(1)
			if char == '=':
				token_string += char
				return Token(Family.assignment, token_string, line_number)
			else:				 
				error(': must be followed by =', line_number)			
		
		# Symbols +,-,*,/,=
		elif char == '+':
			token_string  = char
			return Token(Family.addOperator, token_string, line_number)
			
		elif char == '-':
			token_string  = char
			return Token(Family.addOperator, token_string, line_number)

		elif char == '*':
			token_string  = char
			return Token(Family.mulOperator, token_string, line_number)
			
		elif char == '/':
			token_string  = char
			return Token(Family.mulOperator, token_string, line_number)

		# Delimeters , ; 
		elif char == ',':
			token_string = char	
			return Token(Family.delimiter, token_string, line_number)
		elif char == ';':
			token_string = char 
			return Token(Family.delimiter, token_string, line_number)
		#EOF
		elif char == '':
			token_string = char
			return Token(Family.end_of_file, token_string, line_number)
		
		# Grouping Symbols
		elif char == '(':
			token_string = char
			return Token(Family.groupSymbol, token_string, line_number)
		elif char == ')':
			token_string = char
			return Token(Family.groupSymbol, token_string, line_number)
		elif char == '{':
			token_string = char
			return Token(Family.groupSymbol, token_string, line_number)
		elif char == '}':
			token_string = char
			return Token(Family.groupSymbol, token_string, line_number)
		elif char == '[':
			token_string = char
			return Token(Family.groupSymbol, token_string, line_number)
		elif char == ']':
			token_string = char
			return Token(Family.groupSymbol, token_string, line_number)
		
		# End of program
		elif char == '.':
			token_string = char
			return Token(Family.delimiter, token_string, line_number)
		
		# automaton state 6
		# Comments
		elif char=='#':
			char = input_file.read(1)
			while char !='#':
				char = input_file.read(1)
				# Counting lines in comments
				if char == '\n':
					line_number += 1
				# If we reach eof while in comments, error
				if char=='': 
					error('Reached eof without closing comments',line_number)
		else: 
			error('Illegal character.',line_number)


def main():
#def main(input_file):

	#input_file = open(input_file,'r')
	input_file = open('testing.txt','r')
	while True:
		token = lex(input_file)
		print(token.recognized_string, 'family:', token.family_type, 'line:', token.line_number)


#main(sys.argv[1])
main()

