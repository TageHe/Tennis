from player import Player
from tkinter import ttk
from match import Match
import tkinter as tk
import threading
import time

class MenuUI:
    '''Represents a menu UI where the user can interact with the program.'''
    def __init__(self, root, players):
        """
        Initialize a new Menu instance.
        
        Parameters:
        all_players (list): A list of all Player instances.
        """

        # Sets up a window
        self.root = root
        self.players = players
        self.root.title("Tennis Match Simulator")
        self.root.geometry("800x400")
        self.player_labels = []

        # It's here because the players apparently needs to be initialized
        self.selected_players = [Player("", 0), Player("", 0)]

        # The code for dropdown menu choice
        def selection_changed(event):
            print(players[len(players) - 1])
            selection1 = self.dropdown_1.get()
            selection2 = self.dropdown_2.get()

            if selection1:
                self.selected_players[0] = self.map_players().get(selection1, None)
            if selection2:
                self.selected_players[1] = self.map_players().get(selection2, None)

            print(f"{selection1} vs {selection2}")

        # Creates the dropdown menus
        self.dropdown_1 = ttk.Combobox(values = self.get_player_names())
        self.dropdown_1.bind("<<ComboboxSelected>>", selection_changed)
        self.dropdown_1.place(x = 50, y = 200)

        self.dropdown_2 = ttk.Combobox(values = self.get_player_names())
        self.dropdown_2.bind("<<ComboboxSelected>>", selection_changed)
        self.dropdown_2.place(x = 250, y = 200)

        # Create Match button
        self.start_button = tk.Button(root, text = "Create Match", command = self.create_match, font=("Arial", 12))
        self.start_button.grid(row = 4, column = 0, padx = 10, pady = 10)

        # Show stats button
        self.show_button = tk.Button(root, text = "Show Stats", command = self.create_player_labels, font=("Arial", 12))
        self.show_button.grid(row = 5, column = 0, padx = 10, pady = 10)

        # Creates add player button
        self.add_player_button = tk.Button(root, text = "Add Player", command = self.add_player, font = ("Arial", 12))
        self.add_player_button.grid(row = 6, column = 0, padx = 10, pady = 10)

        # Creates update button
        self.add_player_button = tk.Button(root, text = "Update", command = self.config_dropdowns, font = ("Arial", 12))
        self.add_player_button.grid(row = 6, column = 1, padx = 10, pady = 10)
    
    def get_player_names(self):
        return list(self.map_players())
    
    def map_players(self):
        return {player.name: player for player in self.players}
    
    def config_dropdowns(self):
        self.dropdown_1.config(values = self.get_player_names())
        self.dropdown_2.config(values = self.get_player_names())
    
    def create_match(self):
        '''Creates match between selected players.'''
        # Checks if two players are chosen
        if len(self.selected_players[0].name) > 0 and len(self.selected_players[1].name) > 0:
            if self.selected_players[0] != self.selected_players[1]:
                # Code to create match
                match = Match(self.selected_players)
                root = tk.Tk()
                gui = GUI(root, match, 0.1)
                root.mainloop()
            else:
                print("ERROR: Nice try, you can't play against yourself")
        else:
            print("ERROR: Must choose exactly two players")

    def create_player_labels(self):
        """
        Dynamically creates labels for each player in the given list and adds them to the GUI.
        """
        # Define column widths
        name_width = 25
        wins_width = 10
        losses_width = 10
        win_rate_width = 10

        # Create a table header with alignment
        header = (
            f"{'Nr':<4}{'Name':<{name_width}}{'Wins':<{wins_width}}"
            f"{'Losses':<{losses_width}}{'Win Rate':<{win_rate_width}}"
        )

        # Initialize the table with the header
        player_table = header

        # Add each player's data to the table
        for index, player in enumerate(self.players):
            player_table += (
                f"\n{(index + 1):<4}{player.name:<{name_width}}"
                f"{player.wins:<{wins_width}}{player.losses:<{losses_width}}"
                f"{player.win_rate:<{win_rate_width}.1f}%"
            )

        # Create a label for the table
        player_label = tk.Label(self.root, text=player_table, justify="left", font=("Courier", 10), anchor="w")

        # Place the label in the GUI
        player_label.place(x=450, y=50)

    
    def add_player(self):
        root = tk.Tk()
        ui = AddPlayerUI(root, self)
        root.mainloop

class GUI:
    '''Represents the window for each match, displaying the score etc.'''
    def __init__(self, root, match, interval):
        """
        Initialize a new GUI instance.
        
        Parameters:
        match (Match): The match which is to be simulated.
        interval (float): The interval (speed) of the match, where smaller = faster.
        """
        # Sets basic variables
        self.match = match
        self.interval = interval
        self.running = False
        self.current_set = 0

        # Setup the GUI layout
        self.root = root
        self.root.title(f"{match.players[0].name} vs {match.players[1].name}")
        self.root.geometry("800x400")

        # Player Names
        self.player1_label = tk.Label(root, text = match.players[0].name, font = ("Arial", 16))
        self.player1_label.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.player2_label = tk.Label(root, text = match.players[1].name, font = ("Arial", 16))
        self.player2_label.grid(row = 1, column = 0, padx = 10, pady = 10)

        # Set and Point Displays
        self.set_labels = []
        for i in range(3):  # Three sets
            set_label1 = tk.Label(root, text = "0", font = ("Arial", 14))
            set_label1.grid(row = 0, column=i + 1, padx = 10, pady = 10)
            set_label2 = tk.Label(root, text = "0", font = ("Arial", 14))
            set_label2.grid(row = 1, column=i + 1, padx = 10, pady = 10)
            self.set_labels.append([set_label1, set_label2])

        self.points_1_label = tk.Label(root, text = "0", font = ("Arial", 16))
        self.points_1_label.grid(row = 0, column = 4, padx = 10, pady = 10)
        self.points_2_label = tk.Label(root, text = "0", font = ("Arial", 16))
        self.points_2_label.grid(row = 1, column = 4, padx = 10, pady = 10)

        # Match Status
        self.status_label = tk.Label(root, text = "Match Ongoing", font = ("Arial", 14))
        self.status_label.grid(row = 3, column = 2, padx = 10, pady = 10)

        # Control Buttons
        self.start_button = tk.Button(root, text = "Start Match", command = self.start_simulation, font = ("Arial", 12))
        self.start_button.grid(row = 4, column = 0, padx = 10, pady = 10)

    def update_display(self):
        """Update the GUI with the latest match state."""
        for i in range(3):  # Update set scores
            self.set_labels[i][0].config(text=self.match.sets[0][i])
            self.set_labels[i][1].config(text=self.match.sets[1][i])
        self.points_1_label.config(text=self.match.points[0])
        self.points_2_label.config(text=self.match.points[1])
    
    def update_players_in_file(self):
        '''Updates both players in the match.'''
        for player in self.match.players:
            player.update_stats_in_file()

    def simulate_point(self):
        """Simulate points live in the match."""
        # Checks if the program should run
        while self.ongoing():
            self.match.simulate_point(server = sum(self.match.games) % 2)
            self.update_display()

            # Checks if a game is over
            if "Winner" in self.match.points:
                winner = self.match.points.index("Winner")
                self.check_game_over(winner)

                # Checks if the match is over
                if self.match_over():
                    self.status_label.config(text = f"{self.match.players[winner].name} Wins the Match!")
                    self.match.players[winner].add_win()
                    self.match.players[1 - winner].add_loss()
                    self.update_players_in_file()
                    self.stop_simulation()
            
            self.update_display()
            time.sleep(self.interval)
    
    def ongoing(self):
        if self.running and self.current_set < 3:
            return True
        else:
            return False
    
    def check_game_over(self, winner):
        if self.match.add_game(winner, self.current_set):  # Runs add_game code which checks if the set is won
            self.current_set += 1  # Move onto next set
            self.match.reset_games()
            print(self.match.calculate_sets_won(0) - self.match.calculate_sets_won(1))  # Prints score for debugging
        self.match.reset_points()

    def match_over(self):
        diff = self.match.calculate_sets_won(0) - self.match.calculate_sets_won(1)
        if self.current_set == 3 or (self.current_set == 2 and diff in (2, -2)):
            return True
        else:
            return False

    def start_simulation(self):
        """Start the match simulation in a separate thread."""
        self.running = True
        self.start_button.destroy()
        threading.Thread(target = self.simulate_point).start()

    def stop_simulation(self):
        """Stop the match simulation."""
        self.running = False

class AddPlayerUI:
    def __init__(self, root, menu):
        '''Sets up the window'''
        # Setup the GUI layout
        self.root = root
        self.root.title("Add a Player")
        self.root.geometry("400x200")
        self.menu = menu
        
        # Title Label
        self.title_label = tk.Label(root, text = "Add New Player", font = ("Arial", 16))
        self.title_label.grid(row = 0, column = 0, padx = 5, pady = 5)
        
        # Player Name Input
        self.name_label = tk.Label(root, text = "Player Name:", font = ("Arial", 14))
        self.name_label.grid(row = 1, column = 0, padx = 5, pady = 5)
        
        self.name_entry = tk.Entry(root, font = ("Arial", 14))
        self.name_entry.grid(row = 1, column = 1, padx = 5, pady = 5)

        # Player chance to win Input
        self.name_label = tk.Label(root, text = "Player Chance:", font = ("Arial", 14))
        self.name_label.grid(row = 3, column = 0, padx = 5, pady = 5)

        self.chance_entry = tk.Entry(root, font = ("Arial", 14))
        self.chance_entry.grid(row = 3, column = 1, padx = 5, pady = 5)
        
        # Submit Button
        self.submit_button = tk.Button(root, text = "Add Player", font = ("Arial", 14), command = self.add_player)
        self.submit_button.grid(row = 2, column = 0, padx = 5, pady = 5)

    def add_player(self):
        '''Adds player if the values are correct'''
        try:
            # Retrieve player name from the input field
            player_name = self.name_entry.get()
            player_chance = self.chance_entry.get()

            # Validate player_name
            name_parts = player_name.split()
            if len(name_parts) != 2 or len(name_parts[0]) != 1:
                raise ValueError("Name must consist of two words, and the first word must be one letter long.")

            # Validate player_chance
            if not player_chance.isdigit():
                raise ValueError("Chance must be a numeric value.")
            chance_value = int(player_chance)
            if chance_value < 1 or chance_value > 99:
                raise ValueError("Chance must be between 1 and 99.")

            # If validation passes, add the player
            new_player = Player(player_name, float(chance_value) / 100)
            self.menu.players.append(new_player)
            print(new_player)
            self.add_player_to_file(new_player)

            # Clear input fields
            self.name_entry.delete(0, tk.END)
            self.chance_entry.delete(0, tk.END)

        except ValueError as e:
            # Handle validation errors
            print(f"Error: {e}")

    
    def add_player_to_file(self, player):
        with open("players.txt", "a") as file:
            file.write(f"\n{player.name}\n{player.chance_to_win}\n0\n0")  # Default wins and losses are set to 0
