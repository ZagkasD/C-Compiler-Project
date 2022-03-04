def lex(input_file):
	while True:
	
		# read each character
		char = input_file.read(1)
		
		# check eof
		if not char:
			break
		
		# automaton state 0
		elif char == " " or char == "\n" or char == "\t":
			print('state 0')
			continue

		# automaton state 1
		elif char.isalpha():
			while char.isalpha() or char.isdigit():
				print('state 1')
				break
			
		#print(char)

import sys

def main():
#def main(input_file):

	#input_file = open(input_file,'r')
	input_file = open('factorial.txt','r')

	token = lex(input_file)

	input_file.close	

#main(sys.argv[1])
main()

