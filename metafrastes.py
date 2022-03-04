from inspect import _void
from os import error


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
				error(": must be followed by =", line_number, char_number)

		''' automaton state 6
		# char = '#'
		#elif char == '#':
			token_string = char
			char = input_file.read(1)
			if char == '}':
				token_string += char
				# TODO return token <=
				pass
			else:
				# TODO return token >
				error(": must be followed by =", line_number, char_number)'''

		#delimeters , ; ( ) . 
		elif char == ',':
			token_string = char
		
			token_string = char
		elif char == ';':
			token_string = char
		#EOF
			token_string = char
		elif char == '':
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
				error(#TODO line number#)

		else: error(#todo wrong symbol)
import sys
def main():
#def main(input_file):

	#input_file = open(input_file,'r')
	input_file = open('factorial.txt','r')

	token = lex(input_file)

	input_file.close	

#main(sys.argv[1])
main()

