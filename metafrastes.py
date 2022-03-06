 # test
# This is test comment

##test ange

# This is a test 1
# This is a test 2

# This is a test 3
 main
from os import error
import sys

class Token:
	# properties: recognized_string, family, line_numbers
	def __init__(self, family, recognized_string, line_number):
		self.family = family
		self.recognized_string = recognized_string
		self.line_number = line_number

	def set_family(self, family_type): # What does this do?
		self.family_type = family_type

class Family: 
	def __init__(self):
		pass
	# TODO make family things

def lex(input_file):
	while True:
	
		# read each character
		char = input_file.read(1)
		
		# check eof
		if not char:
			break
		
		# automaton state 0
		elif char == " " or char == "\n" or char == "\t":
			continue

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
				token_string += char
				#TODO store line number
				#TODO Backtracking

		# automaton symbols +,-,*,/,=
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

		# automaton state 6
		#COMMENTS
		elif char=='#':
			char = input_file.read(1)
			while char !='#':
				char = input_file.read(1)
				#todo line number ++ if /n
				if char=='': 
					error("TODO line number")

		

		#delimeters , ; 
		elif char == ',':
			token_string = char	# TODO terurn token
		elif char == ';':
			token_string = char # TODO terurn token
		#EOF
		elif char == '':
			pass	# TODO return token
			#EOF
		
		#GROUPING
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
		
		#EOP
		elif char == '.':
			token_string = char
		
		#COMMENTS
		elif char=='#':
			char = input_file.read(1)
			while char !='#':
				char = input_file.read(1)
				#todo line number ++ if /n
				if char=='': 
					error() # TODO line numbers
		else: 
			error() # TODO line numbers


def main():
#def main(input_file):

	#input_file = open(input_file,'r')
	input_file = open('factorial.txt','r')

	token = lex(input_file)

	input_file.close	

#main(sys.argv[1])
main()

