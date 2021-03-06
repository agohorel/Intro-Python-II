import sys
import time
from room import Room
from player import Player
from item import Item, Treasure

# controls main game loop
done = False

# Declare all the rooms

room = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mount beckons", [Item("stick", "a small stick, perhaps useful for crafting a torch"), Item("rock", "a primitive but effective home defense tool")]),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east.""", [Item("lamp", "an old, disused lamp that's run out of fuel"), Item("dagger", "a rusty shiv")]),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm.""", [Item("rope", "a short rope, too short to use for climbing, but perhaps useful for other purposes?"), Item("chain", "a heavy chain")]),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air.""", [Item("cannister", "a bent up fuel cannister, still a few drops left")]),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south.""", [Treasure("goblet", "a shimmering golden goblet", 15000), Treasure("necklace", "a jewel-encrusted necklace w/ cryptic engravings", 5000)]),
}


# Link rooms together

room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']

#
# Main
#

# Make a new player object that is currently in the 'outside' room.

player = Player("alex", room['outside'])

# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.


def help():
    print("\n### NAVIGATION COMMANDS ###")
    print("west or w - travel west")
    print("east or e - travel east")
    print("north or n - travel north")
    print("south or s - travel south")
    print("\n### ITEM COMMANDS ###")
    print("take, grab, get [item name] - pick up an item")
    print("drop, toss, discard [item name] - drop an item\n")
    print("\n### GAME OPTIONS ###")
    print("q, quit, exit - exit the game")
    time.sleep(3)


def death():
    print("\nYour greed has angered The Ancient Ones. An incomprehensible energy overtakes the room. Your mind recoils, the confusion immeasurable. In reality only a few moments pass, but you feel trapped inside eternity. Your body falls to the dirty floor a crumpled shadow of itself. You fade into the blackness...")
    time.sleep(7)
    print("\n\n\n\033[91m" + "YOU DIED") # set red color 
    time.sleep(.75)
    print("\u001b[0m" + "ouch.") # reset color
    global done
    done = True


def navigation(choice):
    try:
        if choice == "q" or choice == "quit" or choice == "exit":
            global done
            done = True
        elif choice == "n" or choice == "north":
            player.current_room = player.current_room.n_to
        elif choice == "s" or choice == "south":
            player.current_room = player.current_room.s_to
        elif choice == "e" or choice == "east":
            player.current_room = player.current_room.e_to
        elif choice == "w" or choice == "west":
            player.current_room = player.current_room.w_to
        elif choice == "help" or choice == "instructions" or choice == "man":
            help()
        else:
            print(
                "Invalid selection - enter 'help' to see list of valid commands")
            time.sleep(2)
    except:
        print("\n**** Can't go further in this direction! Try another. ****\n")
        time.sleep(2)


def item_interaction(choice):
    action, item = choice

    if action == "take" or action == "grab" or action == "get":
        for idx, i in enumerate(player.current_room.items):
            if i.name == item:
                player.pickup_item(i)
                player.inventory[-1].on_take()
                if player.current_room.name == "Treasure Chamber" and len(player.current_room.items) == 0:
                    death()
            else:
                if (idx == 0):  # prevent duplicate prints
                    warn_invalid_item()

    elif action == "drop" or action == "toss" or action == "discard":
        for idx, i in enumerate(player.inventory):
            if i.name == item:
                player.inventory[-1].on_drop()
                player.drop_item(i)
            else:
                if (idx == 0):
                    warn_invalid_item()
    else:
        print("\nInvalid command - enter 'help' for a list of commands")
        time.sleep(2)


def display_room_items():
    if len(player.current_room.items):
        print("\nYou see the following items:")
        print(*player.current_room.items, sep="\n")
    else:
        print("\nThe room before you contains no useful items")


def display_player_inventory():
    if len(player.inventory):
        print("\nYou are carrying the following items:")
        print(*player.inventory, sep="\n")
    else:
        print("\nYou have no items in your inventory")
    time.sleep(2)


def display_current_location():
    print("\n----------------------------------------------\n")
    print("Current Location: " + player.current_room.name)
    print("\nDescription: " + player.current_room.description)


def warn_invalid_item():
    print("\nItem not available - you can only pick up items in the room or drop ones in your inventory.")
    time.sleep(2)


# main game loop
while done != True:
    display_current_location()
    display_room_items()
    choice = input("\nWhat will you do? ").split(" ")

    if (len(choice) == 1 and choice[0] != "i" and choice[0] != "inventory"):
        navigation(choice[0])
    elif (choice[0] == "i" or choice[0] == "inventory"):
        display_player_inventory()
    else:
        item_interaction(choice)
