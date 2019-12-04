import WordSearchPuzzle as wsp

def main():

	'''Tests WordSearchPuzzle class by creating a simple puzzle.'''

	words = ['HELLO', 'BACKLIGHT', 'RAPTORS', 'COMPUTER', 'SENATORS', 'PYTHON']

	puzzle = wsp.WordSearchPuzzle(word_list=words, show_answers=True)
	print(puzzle)
	
main()