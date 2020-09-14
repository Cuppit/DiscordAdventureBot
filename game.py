"""

This module contains the class definition of a game instance.  This game instance is what's saved in
the game database as a player is playing the game, as well as what's recalled when a player
wants to start playing again after stopping.

The actual game has rooms, objects, and a player object.

20200910_2023: eventually the plan is for game data (room, object, word lists, etc.)
to be stored in and accessed from a database.  For now, the

"""

import constants


class Object:
    def __init__(self, name, description, is_obtainable, is_container):
        self.name = name
        self.desc = description
        self.is_obtainable = is_obtainable
        self.is_container = is_container
        if is_container:
            self.contents = []


class Character:
    def __init__(self, room):
        self.hp = int(5)
        self.inv = []
        self.room = room # Give this character the name of the room it was created in.
        self.room.characters.append(self)  # Make sure the ROOM ITSELF ALSO KNOWS that the character is now inside of it.

    def change_room(self, new_room):
        self.room.characters.remove(self)  # Update the original room to reflect this character is no longer in that room.
        self.room = new_room  # Update this character so it knows it's now inside the new room.
        self.room.characters.append(self)  # Update the new room to reflect this character is now inside of the room.


# This class contains details of a room.
class Room:

    # This is the init call that should be used.
    def __init__(self, name, desc, xcoord, ycoord, owningmap):  # test comments
        self.name = str(name)
        self.desc = str(desc)
        self.characters = []
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.owningmap = owningmap # the map this room belongs to.

        self.normal_exits = [] # Rooms that can be moved to from this room.
        for x in range(constants.NORMAL_DIRS_TOTAL):
            self.normal_exits.append(constants.DIR_CLOSED)


# This class is a container that holds a 2d array of rooms
class Map:
    def __init__(self, xdim, ydim):

        self.rooms = []
        for x in range(xdim):
            self.rooms.append([])
            for y in range(ydim):
                self.rooms[x].append(Room(None, None, x, y, self))



class Game:
    def __init__(self):

        self.map = None
        if not constants.PULL_FROM_DB:  # If we aren't loading the game from the database, do this.
            self.map = Map(3, 3)  # Generate a blank 3x3 room map.

        '''
            map of carved out section of 3x3 initial map:
            x x -
            - x -
            - x x
        '''

        self.map.rooms[0][0].name = "The Cave of Wonders"
        self.map.rooms[0][0].desc = "You find yourself inside of a cave.  The cave is quite wondrous."
        self.map.rooms[0][0].normal_exits[constants.E_EXIT]=constants.DIR_OPEN

        self.map.rooms[1][0].name = "The Entrance to the Cave of Wonders"
        self.map.rooms[1][0].desc = "Here, you see a glowing sign pointing to the east, saying 'CAVE OF WONDERS: THIS WAY'."
        self.map.rooms[1][0].normal_exits[constants.W_EXIT]=constants.DIR_OPEN
        self.map.rooms[1][0].normal_exits[constants.S_EXIT]=constants.DIR_OPEN

        self.map.rooms[1][1].name = "a Dark Forest Road"
        self.map.rooms[1][1].desc = "Overhanging branches leave little room for light here."
        self.map.rooms[1][1].normal_exits[constants.N_EXIT]=constants.DIR_OPEN
        self.map.rooms[1][1].normal_exits[constants.S_EXIT]=constants.DIR_OPEN

        self.map.rooms[1][2].name = "a Quaint Roadway"
        self.map.rooms[1][2].desc = "This road is well-trodden, and filled with wonder."
        self.map.rooms[1][2].normal_exits[constants.N_EXIT]=constants.DIR_OPEN
        self.map.rooms[1][2].normal_exits[constants.E_EXIT]=constants.DIR_OPEN

        self.map.rooms[2][2].name = "your Cabin Home"
        self.map.rooms[2][2].desc = "This home requires wood."
        self.map.rooms[2][2].normal_exits[constants.W_EXIT]=constants.DIR_OPEN

        self.pc = Character(self.map.rooms[2][2])  # This is the character currently designated as the player character.

    '''
       -Explains commands/controls
       -Starts a new game
       -Begins the game
       -Saves user session in DB.
    '''


    # This moves the pc to the room specified in room_to_go.
    def move_character_to_room(self, character, room_to_go):
        room_to_go: Room
        if (character.room is not None) and isinstance(character.room, Room): # Ensure character is already in a room.
            character.room.characters.remove(self.pc)  # Remove the player character from it's old room.
        room_to_go.characters.append(character)

    def start(self):
        toreturn = "***THE ADVENTURE BEGINS***\n"
        toreturn += "\nYou wake up in your cabin in the woods.\n"
        toreturn += self.pc.room.desc


        return toreturn

    def parse(self, msg):
        room = self.pc.room
        firstword = msg.split()[0]
        toreturn = ""
        if firstword == "help":
            toreturn += "Here is a list of commands:\n-look : receive description of your environment and all exits.\n-north/(n) : attempt to move north."
            toreturn += "\n-inventory (inv) : receive a list of carried items in inventory."
            toreturn += "\n-east (e) : attempt to move east."
            toreturn += "\n-south (s) : attempt to move south."
            toreturn += "\n-west (w) : attempt to move west."
            toreturn += "\n-get <object> : attempt to acquire an object."
            toreturn += "\n-use <object> on <target> : attempt to use an item (usually in inventory) on some visible target object, or other item in inventory."
            toreturn += "\n-help : display this help dialogue."

        elif firstword == "look":
            toreturn += "CURRENT LOCATION: "+room.name+"\n"
            toreturn += room.desc+"\n\n"
            if room.normal_exits[constants.N_EXIT] is constants.DIR_OPEN:
                toreturn += "To the *north*, you see "+room.owningmap.rooms[room.xcoord][room.ycoord-1].name+".\n"
            if room.normal_exits[constants.E_EXIT] is constants.DIR_OPEN:
                toreturn += "To the *east*, you see "+room.owningmap.rooms[room.xcoord+1][room.ycoord].name+".\n"
            if room.normal_exits[constants.W_EXIT] is constants.DIR_OPEN:
                toreturn += "To the *west* you see "+room.owningmap.rooms[room.xcoord-1][room.ycoord].name+".\n"
            if room.normal_exits[constants.S_EXIT] is constants.DIR_OPEN:
                toreturn += "To the *south*, you see "+room.owningmap.rooms[room.xcoord][room.ycoord+1].name+".\n"

        elif firstword == "north" or firstword == "n":
            if room.normal_exits[constants.N_EXIT] is constants.DIR_OPEN:
                self.pc.change_room(room.owningmap.rooms[room.xcoord][room.ycoord-1])
                toreturn += "You go north.\n\n"
                toreturn += self.parse("look")
            else:
                toreturn = "There's no way to go north right now."
        elif firstword == "east" or firstword == "e":
            if room.normal_exits[constants.E_EXIT] is constants.DIR_OPEN:
                self.pc.change_room(room.owningmap.rooms[room.xcoord+1][room.ycoord])
                toreturn += "You go east.\n\n"
                toreturn += self.parse("look")
            else:
                toreturn = "There's no way to go east right now."
        elif firstword == "south" or firstword == "s":
            if room.normal_exits[constants.S_EXIT] is constants.DIR_OPEN:
                self.pc.change_room(room.owningmap.rooms[room.xcoord][room.ycoord+1])
                toreturn += "You go south.\n\n"
                toreturn += self.parse("look")
            else:
                toreturn = "There's no way to go south right now."
        elif firstword == "west" or firstword == "w":
            if room.normal_exits[constants.W_EXIT] is constants.DIR_OPEN:
                self.pc.change_room(room.owningmap.rooms[room.xcoord-1][room.ycoord])
                toreturn += "You go west.\n\n"
                toreturn += self.parse("look")
            else:
                toreturn = "There's no way to go west right now."
        else:
            toreturn = "Sorry, I didn't understand that (or I haven't implemented that yet...sorry!) \n" \
                       "Try typing '-help' to get a list of commands."
        return toreturn



            # print("**CRITICAL ERROR IN game.py, 'Game("+str(self)+").move_pc_to_room("+str(self)+", "+str(Room)+"): Attempted to move character to non-room or non-existant room.***")




            #self.rooms.append(Room("Cabin", "This is your log cabin."))

