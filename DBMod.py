"""

This script handles backend database management for the bot.

"""



#File for working/modifying/testing database

import sys  # Will use this to manage existing files.
import sqlite3
from sqlite3 import Error



#sql_connection() definition###
# Connects to our DB.  Creates the DB if it doesn't exist.
# ######################
def sql_connection():
    try:
        #TODO 20200909_2201: Design bot db, and write init function to check/set up on load.
        con = sqlite3.connect('TestDB.db')
        print("Successfully connected to the database.")
        return con
    except Error:
        print(Error)
# ######################            


# This creates a new "employees" table.  This might not be necessary.
def sql_table(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE employees(id integer PRIMARY KEY, name text, salary real, department text, position text, hireDate text)")
    con.commit()


# This creates a new users table if it doesn't already exist in the database.
def sql_create_users_log(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE users(id integer PRIMARY KEY, discordID text, displayName text, dateJoined text)")


# This sets up a fresh database.
def sql_init_db(con):
    None


# Called when a user joins the guild.  Checks whether or not
# the user is already in the DB, and if not, adds the user.
def add_user_to_db(con, member):
    print("User joined guild. CHECKING AGAINST DB: Member ID is: {}".format(member.id))
    cursorObj = con.cursor()
    cursorObj.execute("SELECT discordID FROM users WHERE discordID == \"{}\"".format(member.id))
    record_found = cursorObj.fetchone()
    if (record_found == None):
        print("NO PRIOR RECORD OF USER.  Logging user details in database: ")
        #first we build a tuple of the data items to insert into the table.

        toinsert = (member.id, member.display_name, member.joined_at)
        print("Created tuple of user properties to log in database.  Tuple contents:")
        print(toinsert)
        #then, we insert this tuple into the database.  The reason we don't use native
        #python string formatting to insert values into the execute()'s string parameter 
        #below is because it's unsafe; it leaves the database vulnerable to an SQL
        #injection attack.
        
        cursorObj.execute("INSERT INTO users VALUES (?,?,?)", toinsert)
        con.commit()
    else:
        print("Details of user:")
        print(record_found)

def msg_log(con, msg):
    print(str(msg.author.display_name+" : "+msg.content))
    cursorObj = con.cursor()
    toinsert = (msg.author.id, msg.author.display_name, msg.channel.name, msg.content)
    cursorObj.execute("INSERT INTO messagelogs VALUES (?,?,?,?)", toinsert)


# ## ---Main--- ## #

#con = sql_connection()
#sql_create_users_log(con)
