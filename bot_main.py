"""
This is the main file from which the bot is ran.
"""


import discord # As of this comment writing, Discord API works with Python 3.6
import DBMod # Import script with functions responsible for handling database management
import random # Used for random number generation
import game # Used to store the Adventure Game state
import TokenSelector # This project's custom GUI utility module for picking a token stored in a file on the filesystem.
import sys

'''
20201025_1347: The bot should attempt to read the token from a file included in the local directory.  If it doesn't 
exist, then it can default to the "tokenselector" dialog.
'''

try:
    with open ('adventurebot.token') as f:
        TOKEN = f.readline()
except IOError:
    print("'discordbot.token' file not found.  Defaulting to TokenSelector prompt: ")
    TOKEN = TokenSelector.token_select_dialog()
    client = discord.Client()

#Active connection to the bot's DB
dbCon = DBMod.sql_connection()

#Storage variable for active running game sessions.
game_sessions = {}

#--------------------------
# --- UTILITY FUNCTIONS ---
# -------------------------

'''
20200910_2102: I'm putting down the text adventure game for a moment and focusing on
what originally piqued my interest in Discord bots; making a rudimentary dice roller
bot.  This should take me 10 minutes at most now that I know how to parse strings
a lot quicker in Python.
'''


# Given the number of dice and the number of sides per die, this returns a list of die rolls using those params.
def roll_dice(num_dice, num_sides):
    rolls = []
    for x in range(num_dice):
        rolls.append(random.randint(1,num_sides))
    return rolls


def dice_roll_msg(msg):  # 'msg' is the original user message the bot received.
        helpmsg = "SYNTAX: '!roll <x>d<y>'\nx = number of dice to roll\ny = number"
        to_return = ""
        dicerolls = []
        inputs = msg.split()[1].split("d")
        if len(inputs) is 2:
            if inputs[0].isnumeric() and inputs[1].isnumeric():
                num_to_roll = int(inputs[0])
                max_roll = int(inputs[1])
                dicerolls = roll_dice(num_to_roll, max_roll)
                roll = msg.split()[1]
                rollstomod = str(dicerolls)[1:-1].split(", ")
                for x in range(len(rollstomod)):
                    if int(rollstomod[x]) == 1 and (max_roll == 20):
                        rollstomod[x]="1 (Fug.)"
                    elif (int(rollstomod[x]) == 20) and (max_roll == 20):
                        rollstomod[x]="20 (YEET!)"
                roll = ", ".join(rollstomod)


                to_return += "ROLLING: "+roll+"\nROLL RESULTS: "+str(dicerolls)+"\nTOTAL: "+str(sum(dicerolls))
            else:
                return "Sorry, I didn't understand that.  It looks like one of the characters in your roll isn't a number?\n"+helpmsg
        else:
            return "Sorry, I didn't understand that.\n"+helpmsg

        return to_return



# ----------------------
# --- DISCORD EVENTS ---
# ----------------------

@client.event
async def on_message(message):

    msg = message.content
    channel = message.channel

    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if msg.startswith('!help'):
        msg = "I can be interacted with using the following commands:\n" \
              "!help         : displays this help message\n" \
              "!roll <x>d<y> : returns x random numbers in the range [1,y].  (ex: '!roll 1d6')\n" \
              "!play         : Begins a new session of the Adventure Game for you (if you don't have one running already)" \
              "              : once you have a game session running, you can type '-help' for game specific commands."
        await channel.send(msg)



    if msg.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await channel.send("hi "+message.author.mention)
        #await client.send_message(message.channel, msg)

    elif msg.startswith('!die'):
        msg = '{0.author.mention}, I\'m sorry, but I can\'t die yet.'.format(message)
        await channel.send(msg)

    elif msg.startswith('!roll'):
        await channel.send(dice_roll_msg(msg))

    elif msg.startswith("!play"):
        if message.author.id not in game_sessions:
            await channel.send("Loading game session for {0}:".format(message.author.mention))
            game_sessions[message.author.id] = game.Game()
            await channel.send(game_sessions[message.author.id].start())

        else:
            await channel.send("You currently have a game session running.  Type '-help' for a list of commands!")

    elif msg.startswith("!"):
        await channel.send("Sorry, I didn't understand that.  Type '!help' for some commands I understand.")


    if msg.startswith("-"):
        toprint = game_sessions[message.author.id].parse(msg[1:])
        await channel.send(toprint)
    #DBMod.msg_log(dbCon, message)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    print('Hi! I\'m running now! say \'!hello\' to me!')

@client.event
async def on_member_join(member):

    msg = 'Thanks for joining.'
    nick = member.nick
    id = member.id
    display_name = member.display_name
    DBMod.add_user_to_db(dbCon, member)
    print('Member (display_name={}, nick={}, id={}) joined.'.format(display_name, nick, id))

# -------------------
# --- MAIN SCRIPT ---
#--------------------


client.run(TOKEN)
