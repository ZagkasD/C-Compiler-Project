from pickle import NONE
import sys

# Global Variables
line_number = 1
input_file = NONE

class Token:
	# properties: family, recognized_string, line_numbers
	def __init__(self, family, recognized_string, line_number):
		self.family = family
		self.recognized_string = recognized_string
		self.line_number = line_number

	def set_family(self, family_type):
		self.family_type = family_type

class Family: 
	def __init__(self):
		pass
	
	number = 0	
	keyword = 1
	id = 2
	addOperator = 3	# +.-
	mulOperator = 4	# *,/
	relOperator = 5	# ==,>=,<,<>
	assignment = 6	# :=
	delimiter = 7	# ,,.,;
	groupSymbol = 8	# (,),{,},[,]

# argv[1] is the first console argument, aka file name
def error( error_msg,line_number):
	print("Error in File",sys.argv[1], 'line', line_number, error_msg)
	exit(1)


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
				char = input_file.read(1)
				token_string += char
				# TODO store line number
				# TODO Backtracking
			#TODO KEYWORDS
		
		# automaton state 2
		# digits
		elif char.isdigit():
			token_string = char
			while char.isdigit():
				char = input_file.read(1)
				if char.isalpha():
					error("Arithmetic constants can not contain letters.", line_number)
				token_string += char
				# TODO add char limit
				# TODO Backtracking
			return Token(Family.number, token_string, line_number)

		# Symbols +,-,*,/,=
		elif char == '+':
				# TODO return token
				pass
		elif char == '-':
			# TODO return token
			pass
		elif char == '*':
			# TODO return token
			pass
		elif char == '/':
			# TODO return token
			pass
		elif char == '+':
			# TODO return token
			pass

		# automaton state 3
		# char = '<'
		elif char == '<':
			token_string = char
			char = input_file.read(1)
			if char == '=':
				token_string += char
				# TODO return token <=
				pass
			elif char == '>':
				# TODO return token <>
				pass

			else:
				# TODO return token <
				pass

		# automaton state 4
		# char = '>'
		elif char == '<':
			token_string = char
			char = input_file.read(1)
			if char == '=':
				token_string += char
				# TODO return token <=
				pass
			else:
				# TODO return token >
				pass

		# automaton state 5
		# char = ':'
		elif char == ':':
			token_string = char
			char = input_file.read(1)
			if char == '=':
				token_string += char
				# TODO return token <=
				pass
			else:
				# TODO return token >
				error(": must be followed by =") # TODO make this nice

		# Delimeters , ; 
		elif char == ',':
			token_string = char	# TODO teturn token
		elif char == ';':
			token_string = char # TODO teturn token

		#EOF
		elif char == '':
			pass	# TODO return token
		
		# Grouping Symbols
		elif char == '(':
			token_string = char
		elif char == ')':
			token_string = char
		elif char == '{':
			token_string = char
		elif char == '}':
			token_string = char
		elif char == '[':
			token_string = char
		elif char == ']':
			token_string = char
		
		# End of program
		elif char == '.':
			token_string = char
		
		# automaton state 6
		# Comments
		elif char=='#':
			char = input_file.read(1)
			while char !='#':
				char = input_file.read(1)
				#todo line number ++ if /n
				if char=='': 
					error() # TODO line numbers
		else: 
			error() # TODO line numbers


#def main():
def main(input_file):

	input_file = open(input_file,'r')
	#input_file = open('testing.txt','r')

	token = lex(input_file)

	input_file.close	

main(sys.argv[1])
#main()

