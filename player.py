def calculate_win_rate(player):
    """
    Calculate the player's win rate as a percentage.
    
    Returns:
    float: The win rate, rounded to 2 decimals.
    """
    if player.played > 0:
        return round(100 * player.wins / player.played, 2)
    return 0.0  # No matches played yet, win rate is 0%

class Player:
    '''Represents a tennis player with associated statistics and methods to modify them.'''
    def __init__(self, name, chance_to_win, wins=0, losses=0):
        """
        Initialize a new Player instance.
        
        Parameters:
        name (str): The player's name.
        chance_to_win (float): Probability of winning a point (0.0 to 1.0).
        wins (int, optional): Number of matches won. Defaults to 0.
        losses (int, optional): Number of matches lost. Defaults to 0.
        """
        self.name = name
        self.wins = wins
        self.losses = losses
        self.played = wins + losses  # Total number of matches played
        self.chance_to_win = chance_to_win
        self.win_rate = calculate_win_rate(self)  # Initial win rate calculation

    def add_win(self):
        """Increment the win count and update related stats."""
        # Updates stats
        self.wins += 1
        self.played += 1

        # Updates win rate after win
        self.win_rate = calculate_win_rate(self)

    def add_loss(self):
        """Increment the loss count and update related stats."""
        # Updates stats
        self.losses += 1
        self.played += 1

        # Updates win rate after loss
        self.win_rate = calculate_win_rate(self)

    def update_stats_in_file(self, filename = "players.txt"):
        """
        Update the player's stats in a file.
        
        Parameters:
        filename (str): The path to the file containing player data.
        """

        # Opens file
        with open(filename, "r") as file:
            lines = file.readlines()

        # Creates variables to use later
        updated_lines = []
        i = 0

        # Changes player values and lets the other ones be the same
        while i < len(lines):
            # Check if the current line matches the player's name
            if lines[i].strip() == self.name:
                updated_lines.append(lines[i])  # Adds player name
                updated_lines.append(f"{self.chance_to_win}\n")  # Adds chance to win
                updated_lines.append(f"{self.wins}\n")  # Get updated wins
                updated_lines.append(f"{self.losses}\n")  # Get updated losses
                i += 4  # Skip the original wins and losses lines
            else:
                updated_lines.append(lines[i])
                i += 1

        # Rewrite the file with updated content
        with open(filename, "w") as file:
            for index, line in enumerate(updated_lines):
                if index == len(updated_lines) - 1:  # Last line check
                    file.write(line.rstrip("\n"))  # Write without newline
                else:
                    file.write(line)  # Write line with newline

    def __lt__(self, other):
        """
        Compare two Player instances based on their win rate.
        """
        return self.win_rate < other.win_rate

    def __str__(self):
        """Return a string representation of the player in a structured table format with dynamic alignment."""

        length = 40 - len(self.name)

        # Player data aligned with the dynamic column width
        player_data = f"{self.name:<{length}} {self.wins:<10} {self.losses:<20} {self.win_rate:<1.1f}%"

        return f"{player_data}"

