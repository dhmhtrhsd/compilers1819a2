import plex

class ParseError(Exception):
	pass

class MyParser:
	
	def __init__(self):
		letter = plex.Range('azAZ')
		digit = plex.Range('01')
		digitvalue = plex.Rep1(digit) #oi times twn metavlitwn a kai b
		name = letter + plex.Rep(letter|digit)
		space = plex.Any(' \n\t')
		Keyword = plex.Str('print','PRINT')
		equals = plex.Str( '=')
		leftparen = plex.Str('(')
		rightparen = plex.Str(')')
		and_token = plex.Str('&')
		or_token = plex.Str('|')
		xor_token = plex.Str('^')
		
		self.lexicon = plex.Lexicon([   
			(Keyword, 'PRINT_TOKEN'),
			(name, 'ID_TOKEN'),
			(equals, 'EQUALS_TOKEN'),
			(leftparen, '('),
			(rightparen, ')'),
			(and_token, '&'),
			(or_token, '|'),
			(xor_token, '^'),
			(digitvalue, 'digitvalue'),
			(space, plex.IGNORE)			
		])
			
	def createScanner(self,fp):
		self.scanner = plex.Scanner(self.lexicon,fp)
		self.la , self.text = self.next_token()

	def next_token(self):
		return self.scanner.read()
	
	def match(self,token):
		print(self.la)
		if self.la == token:
			self.la,self.text=self.next_token()
		else:
			raise ParseError("found {} instead of {}".format(self.la,token))

	def parse(self,fp):
		self.createScanner(fp)
		self.stmt_list()

	def stmt_list(self):
		if self.la == 'ID_TOKEN' or self.la == 'PRINT_TOKEN':
			self.stmt()
			self.stmt_list()
		elif self.la == None:
			return
		else:
			raise ParseError("Expected id_token or print_token")
			
	def stmt(self):
		if self.la == 'ID_TOKEN':
			self.match('ID_TOKEN')
			self.match('EQUALS_TOKEN')
			self.expr()
		elif self.la == 'PRINT_TOKEN':
			self.match('PRINT_TOKEN')
			self.expr()
		else:
			raise ParseError("Expected id_token or print_token")
			
	def expr(self):
		if self.la == '(' or self.la == 'ID_TOKEN' or self.la == 'digitvalue':
			self.term()
			self.term_tail()
		#elif self.la == ')' or self.la == 'ID_TOKEN' or self.la == None or self.la == 'PRINT_TOKEN' :
			#return self.term()
		else:
			raise ParseError("Expected ( or id")
			
	def term_tail(self):
		if self.la == '^':
			self.match('^')
			self.term()
			self.term_tail()
		elif self.la == 'ID_TOKEN' or self.la == 'PRINT_TOKEN' or self.la == None or self.la == ')':
			return
		else:
			raise ParseError("Expected ^, ID_TOKEN, PRINT_TOKEN, )") 
		
	def term(self):
		if self.la == '(' or self.la == 'ID_TOKEN' or self.la == 'digitvalue':		
			self.factor()
			self.factor_tail()
		else:
			raise ParseError("Expected (, ID_TOKEN or digitvalue") 

	def factor_tail(self):
		if self.la == '|':
			self.match('|')
			self.factor()
			self.factor_tail()
		elif self.la == '^' or self.la == 'ID_TOKEN' or self.la == 'PRINT_TOKEN' or self.la == None or self.la == ')':
			return
		else:
			raise ParseError("Expected |, ^, ID_TOKEN, 'PRINT_TOKEN', )") 

	def factor(self):
		if self.la == '(' or self.la == 'ID_TOKEN' or self.la == 'digitvalue':
			self.atom()
			self.atom_tail()
		else:
			raise ParseError("Expected ( or id or a digitvalue.")
			
	def atom_tail(self):
		if self.la == '&':
			self.match('&')
			self.atom()
			self.atom_tail()
		elif self.la == '|' or self.la == '^' or self.la == 'ID_TOKEN' or self.la == 'PRINT_TOKEN' or self.la == None or self.la == ')':
			return
		else:
			raise ParseError("Expected &, |, ^, ID_TOKEN, PRINT_TOKEN, )")
		
	def atom(self):
		if self.la == '(':
			self.match('(')
			self.expr()
			self.match(')')
		elif self.la == 'ID_TOKEN':
			self.match('ID_TOKEN')
		elif self.la == 'digitvalue':
			self.match('digitvalue')
		else:
			raise ParseError("Expected ( or id or digitvalue ")
		
parser = MyParser()

with open('in.txt', 'r') as fp:
	parser.parse(fp)