import random

class Word:
	'''Class to hold a single word in a WordSearchPuzzle.'''

	def __init__(self, name):
		'''
		Parameters:
			name (string): name of the word
		'''
	
		self.name = name
		self.length = len(name)
		
	def set_direction(self):
		DIRECTIONS = ['N','S','E','W','NE','NW','SE','SW']
		rnd = random.randint(0,7)
		self.direction = DIRECTIONS[rnd]

	def set_start_pos(self, x_range, y_range):
		self.x_pos = random.randint(*x_range)
		self.y_pos = random.randint(*y_range)