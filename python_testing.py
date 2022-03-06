class Token:
	# properties: recognized_string, family, line_numbers
	def __init__(self, recognized_string, family, line_number):
		self.recognized_string = recognized_string
		self.family = family
		self.line_number = line_number

	def __str__():
		pass
		
class Lex(Token):
	'''
	Make the token:Token in __init__
	'''
	def __init__(self, current_line, file_name):
		self.current_line = current_line
		self.file_name = file_name

	def __del():
		pass

	def next_token():Token
	pass
	
	def __error():
		pass
		
	
