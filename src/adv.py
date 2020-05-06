from room import Room
from player import Player

# Declare all the rooms

room = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mount beckons", ["stick", "rock"]),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east.""", ["lamp", "dagger"]),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm.""", ["rope", "chain"]),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air.""", ["rock"]),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south.""", ["goblet", "necklace"]),
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


while True:
    print("Current Location: " + player.current_room.name)
    print("\nDescription: " + player.current_room.description)
    print("\nYou see the following items:")
    print(*player.current_room.items, sep=", ")
    choice = input("\nWhich way do you want to go? ")

    if choice == "q":
        quit()

    try:
        if choice == "n":
            player.current_room = player.current_room.n_to
        elif choice == "s":
            player.current_room = player.current_room.s_to
        elif choice == "e":
            player.current_room = player.current_room.e_to
        elif choice == "w":
            player.current_room = player.current_room.w_to
        else:
            print(
                "Invalid selection - valid inputs are 'n', 's,', 'e', 'w' directions or 'q' to quit")
    except:
        print("\nCan't go further in this direction! Try another.\n")
