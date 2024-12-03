'''
Tennis match simulation and statistic viewer

Made by Tage Hermansson
'''

import tkinter as tk
import ui
from player import Player
from match import Match

def import_players():
    '''
    Imports players from the text file 'players.txt'.

    Reads the file line by line to create Player objects with their
    name, chance to win a serve, wins, and losses.
    '''
    players = []

    try:
        with open("players.txt", "r") as file:
            name = file.readline().strip()
            # Read player data until the end of the file
            while name:
                chance_to_win = float(file.readline().strip())
                wins = int(file.readline().strip())
                losses = int(file.readline().strip())
                player = Player(name, chance_to_win, wins, losses)
                players.append(player)
                name = file.readline().strip()  # Read next name or terminate the loop
    except FileNotFoundError:
        print("Error: File not found.")

    return sorted(players, reverse = True)

def print_players(players):
    '''
    Prints all players with their index number and statistics.

    Parameters:
    players (list): List of Player objects to be printed.
    '''

    index = 1
    for player in sorted(players):
        print(f"{index}. {player}")
        index += 1

def create_match(player_1, player_2):
    '''
    Creates a Match instance between two chosen players.

    Parameters:
    player_1 (Player): The first player for the match.
    player_2 (Player): The second player for the match.

    Returns:
    Match: A Match object initialized with the two players.
    '''
    return Match([player_1, player_2])

def create_player():
    '''
    Creates a new player with user input and add it to 'players.txt'.

    Prompts the user for the player's name and chance to win their serve,
    then writes this information to the file.
    '''
    name = input("What is the name of the player?: ")
    chance_to_win = input("What is the player's chance to win serve? (as a decimal): ")
    with open("players.txt", "a") as file:
        file.write(f"\n{name}\n{chance_to_win}\n0\n0")  # Default wins and losses are set to 0

def menu():
    '''
    Prints the menu options and returns the user's choice.

    Returns:
    str: The user's choice.
    '''
    return input(
        "\nMenu\n"
        "Do you want to (p) play a match, (a) add a player, (v) view stats, "
         "(s) simulate a season or (q) quit?\n"
        "Write here: "
    )

def main():
    '''
    The main function - a control loop for the program, displaying the menu
    and executing user choices until the user chooses to quit.
    '''
    choice = ""  # Initialize variable to track user choice
    players = import_players()  # Load players from file
    root = tk.Tk()
    menu = ui.MenuUI(root, players)
    root.mainloop()

# Run the main function to start the program
if __name__ == "__main__":
    main()
