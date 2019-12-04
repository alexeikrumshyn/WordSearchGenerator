import random
import Word as wd
from CustomExceptions import *

class WordSearchPuzzle:
	'''Class to produce a Word Search Puzzle.'''

	def __init__(self, word_list=[], height=10, width=10, show_answers=False):
		'''
		Parameters:
			word_list (string[]): list of words that are to be placed in the word search
			height (int): height of puzzle
			width (int): width of puzzle
			show_answers (boolean): True if only the letters of the words contained in words_list should be shown; False if the whole puzzle should be shown
		'''
		
		self.height, self.width = self.check_size_input(height, width)
		self.word_list = self.check_words_input(word_list)
		
		if not self.isboolean(show_answers):
			raise TypeError('show_answers must be a boolean type')
		self.show_answers = show_answers
		
		self.occupied = {}
		self.launch()

	def check_size_input(self, h, w):
		'''Validates size parameters.
		Parameters:
			h: height
			w: width
		'''
		
		if not isinstance(h, int) or not isinstance(w, int):
			raise TypeError('Please use an integer when setting the height and width.')
	
		if h<5 or h>50 or w<5 or h>50:
			raise SizeError('Invalid size. Please ensure the height and width values are between 5 and 50.')
			
		return h,w

	def check_words_input(self, word_list):
		'''Validate word list provided by user of class.'''
	
		valid_words = []
	
		if not isinstance(word_list, list):
			raise TypeError('Please use a list of strings when setting the words to be placed in the puzzle.')
	
		for word in word_list:
			if not isinstance(word, str):
				raise TypeError('Please use a list of strings when setting the words to be placed in the puzzle.')
				
			if len(word) < 3:
				raise WordLengthError('One of your words ('+word+') is too short. Words must be at least 3 characters.')
				
			if len(word) > self.width or len(word) > self.height:
				raise WordLengthError('One of your words ('+word+') is too long for the selected height and width.')
				
			if not word.isalpha():
				raise CharacterError('One of your words ('+word+') contains one or more non-alpha characters.')
			
			valid_words.append(word.upper())
		
		return valid_words

	def isboolean(self, var):
		'''Returns True if var is a boolean, False otherwise.'''
	
		if isinstance(var, bool):
			return True
		else:
			return False

	def get_letter(self, x, y):
		'''Returns letter on board at position (x,y).'''
		return self.puzzle_board[x][y]

	def launch(self):
		'''Launches functionality of class.'''
		self.generate_random_board()
		self.add_words()

	def generate_random_board(self):
		'''Creates a 2D array containing a random arrangement of letters.'''
	
		self.puzzle_board = []
		
		for _ in range(self.height):
			curr_row = []
			
			for _ in range(self.width):
				rnd = random.randint(65, 90) #A -> Z ascii values
				letter = str(chr(rnd))
				curr_row.append(letter)
				
			self.puzzle_board.append(curr_row)

	def set_word_pos(self, word):
		'''Sets a word's starting position on the board by first deciding the valid range of (x,y) coordinates based on the direction of the word, then calls Word.set_start_pos to set the value.'''
	
		def N():
			return [(0,self.width-1) , (0,self.height-word.length)]
		def S():
			return [(0,self.width-1) , (word.length-1,self.height-1)]
		def W():
			return [(0,self.width-word.length) , (0,self.height-1)]
		def E():
			return [(word.length-1, self.width-1) , (0,self.height-1)]
		def NW():
			return [N()[1] , W()[0]]
		def NE():
			return [N()[1] , E()[0]]
		def SW():
			return [S()[1], W()[0]]
		def SE():
			return [S()[1], E()[0]]

		#locals() returns a dictionary of functions in local scope
		word.set_start_pos( *locals()[word.direction]() )

	def get_move(self, word):
		'''Returns a word's movement in [x,y] format based on its direction.'''
	
		def N():
			return [0,1]
		def S():
			return [0,-1]
		def W():
			return [1,0]
		def E():
			return [-1,0]
		def NW():
			return [ N()[1] , W()[0] ]
		def NE():
			return [ N()[1] , E()[0] ]
		def SW():
			return [ S()[1], W()[0] ]
		def SE():
			return [ S()[1], E()[0] ]
	
		return locals()[word.direction]()

	def set_letters(self, word):
		'''Sets a word onto the board.'''
	
		move = self.get_move(word)
	
		for count, letter in enumerate(word.name):
			x = word.x_pos+(move[0]*count)
			y = word.y_pos+(move[1]*count)
			self.puzzle_board[x][y] = letter
			self.occupied[(x,y)] = letter #keep track of which coordinates are 'taken' by a letter in a word
	
	def check_collisions(self, word):
		'''Returns True if a letter in a word intersects with a letter in another word already on the board, AND the intersection point does not contain the same letter. Returns False otherwise.'''
		
		move = self.get_move(word)
		
		for count, curr_letter in enumerate(word.name):
			curr_x = word.x_pos+(move[0]*count)
			curr_y = word.y_pos+(move[1]*count)
			
			#check if coordinates are already occupied by a letter of another word
			for (x,y), letter in self.occupied.items():
				if (x,y) == (curr_x,curr_y): #if yes, check if the letter at that location is the same
					if letter != curr_letter:
						return True
				
		return False
	
	def add_words(self):
		'''Adds all words in self.word_list to the board.'''
	
		for word_name in self.word_list:
		
			word = wd.Word(word_name) #create a new Word object
			
			total_attempts = 100 #maximum attempts to find a spot on the board for the word
			found_collision = True
			
			for attempt in range(total_attempts):
				word.set_direction()
				self.set_word_pos(word)
				found_collision = self.check_collisions(word)
				if not found_collision:
					break #successfully found place for word, so break out
					
			if found_collision:
				print('Could not place '+word_name)
			else:
				self.set_letters(word)
	
	def __str__(self):
		'''@Override print() function'''
	
		output = ''
		for i in range(self.height):
			for j in range(self.width):
				
				if self.show_answers:
					if (i,j) in self.occupied.keys():
						output += self.get_letter(i,j)
					else:
						output += ' '
				else:
					output += self.get_letter(i,j)
					
				output += ' '
			output += '\n'
			
		return output
				