import random

class Match:
    '''Represents a tennis match between two players, including scoring and match outcomes.'''
    def __init__(self, players):
        """
        Initialize a new Match instance.
        
        Parameters:
        players (list): A list of Player instances participating in the match.
        """
        self.players = players
        self.points = [0, 0]  # Points for each player
        self.games = [0, 0]   # Games won by each player in the current set
        self.sets = [[0, 0, 0], [0, 0, 0]]  # Each player's games in sets (3 sets total)

    def add_points(self, player_index):
        """
        Add points to the specified player and handle tennis scoring logic.
        
        Parameters:
        player_index (int): The index of the player to whom points are added.
        """

        # Sets variables for player and other
        other_index = 1 - player_index
        current_points = self.points[player_index]
        other_points = self.points[other_index]

        # Code to decide what the new points should be
        point_progression = {0: 15, 15: 30, 30: 40}
        if current_points in point_progression:
            self.points[player_index] = point_progression[current_points]
        elif current_points == 40:
            if other_points == 40:
                self.points[player_index] = "Adv"
            elif other_points == "Adv":
                self.points[other_index] = 40
            else:
                self.points[player_index] = "Winner"
                self.points[other_index] = "Loser"
        elif current_points == "Adv":
            self.points[player_index] = "Winner"
            self.points[other_index] = "Loser"

    def reset_points(self):
        """Reset the points for both players to 0."""
        self.points = [0, 0]

    def add_game(self, player_index, current_set):
        """
        Add a game to the specified player's score in the current set or return True if set is won.
        
        Parameters:
        player_index (int): The index of the player who won the game.
        current_set (int): The index of the current set.
        """
        # Sets variables for player and other
        other_index = 1 - player_index
        self.games[player_index] += 1
        
        # Updates the sets list with updated status
        self.sets[player_index][current_set] = self.games[player_index]
        self.sets[other_index][current_set] = self.games[other_index]

        # Code to decide if someone has won the set
        if self.games[player_index] >= 6 and (self.games[player_index] - self.games[other_index]) >= 2:
            return True
        return False

    def reset_games(self):
        """Reset the games won by both players to 0."""
        self.games = [0, 0]
    
    def calculate_point(self, server, receiver):
        """
        Calculate the winner of a point using a DnD-inspired roll system.

        Parameters:
        server (int): Index of the player serving.
        receiver (int): Index of the player receiving.

        Returns:
        int: Index of the player who won the point.
        """
        # Server advantage: roll two random numbers, take the higher
        server_roll = max(random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))
        receiver_roll = max(random.uniform(0, 1), random.uniform(0, 1))

        # Multiply each roll by the player's chance to win
        server_score = server_roll * self.players[server].chance_to_win
        receiver_score = receiver_roll * self.players[receiver].chance_to_win

        # Determine the winner
        if server_score >= receiver_score:
            return server  # Server wins
        else:
            return receiver  # Receiver wins

    def simulate_point(self, server):
        """
        Simulate a single point in the match.

        Parameters:
        server (int): Index of the player serving.
        """
        receiver = 1 - server
        point_winner = self.calculate_point(server, receiver)
        self.add_points(point_winner)

    def calculate_sets_won(self, player_index):
        """
        Calculate the number of sets a player has won.

        Parameters:
        player_index (int): The index of the player (0 or 1).

        Returns:
        int: The number of sets the player has won.
        """
        sets_won = 0
        for set_index in range(len(self.sets)):
            # If the player's score is higher than the opponent's in this set
            if self.sets[player_index][set_index] > self.sets[1 - player_index][set_index]:
                sets_won += 1
        return sets_won

    def __str__(self):
        return f"Sets: {self.sets} | Points: {self.points}"