"""

This module holds "constants" in the project, or variables
that shouldn't be changed at runtime.

"""


'''
These "constants" refer to the 'normal_exits' property of the Room object defined in game.py.  This is a list of 
4 booleans, with each index of the list referring to a different direction in the room.     
'''
N_EXIT = 0
E_EXIT = 1
S_EXIT = 2
W_EXIT = 3

NORMAL_DIRS_TOTAL = 4 # Because there are only 4 'normal' directions, north, east, south, and west.

DIR_OPEN = True
DIR_CLOSED = False

PULL_FROM_DB = False # <---SET THIS TO TRUE TO START USING DATABASE DATA.  If false, the game will instead build "hard-coded" data for the game at initialization, used for testing purposes.

