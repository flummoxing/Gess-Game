# Author: Alexa Langen
# Date: 1 June 2020
# Description: An implementation of an abstract board game called Gess. Rules
# can be found here: https://www.chessvariants.com/crossover.dir/gess.html

from stone import *
from stoneCollection import StoneCollection
from piece import Piece
from move import Move
from board import Board

class GessGame:
    """
    Represents a game of Gess.
    GessGame class keeps track of the current game board, monitors and updates whose turn it is and the current game state (including registering resignations and checking for victory conditions).
    In its make_move() method, it interacts with Board, Move, and Piece classes to register a player's move.
    """

    def __init__(self):
        """
        Constructor for GessGame class. 
        GessGame has a Board initialized to its starting layout. Black goes first.
        """

        self._gameState = "UNFINISHED"  
        self._gameBoard = Board()
        self._currentPlayer = "BLACK"

    def get_game_state(self):
        """
        Returns current game state.
        :return: (string) "UNFINISHED", "BLACK_WON", or "WHITE_WON"
        """

        return self._gameState

    def assign_victory(self, victor):
        """
        Changes game state to assign victory to the victor.
        :param: victor (string) "WHITE" or "BLACK"
        """

        if victor == "WHITE":
            self._gameState = "WHITE_WON"
        if victor == "BLACK":
            self._gameState = "BLACK_WON"

    def resign_game(self):
        """
        Allows the current player to concede the game, giving opponent the win.
        Updates game state. 
        """

        self.assign_victory(OPPONENT[self._currentPlayer])

    def check_victory(self):
        """
        Checks for victory, i.e. if current player has destroyed opponent's last ring.
        :return: True if victory has occurred, False if not
        """

        if self._gameBoard.has_ring(OPPONENT[self._currentPlayer]):
            return False
        return True

    def make_move(self, currentCenter, newCenter):
        """
        Parameters:
            currCenterInput (string): the center of the piece the player wishes to move. Format should match
            <row letter, column number> e.g. 'a19', 'm4', etc. Must fall within 18x18 area of play.
            newCenterInput (string): the center of the piece the player wishes to move. Same rules as for above parameter.
        Returns:
            True if move was made successfully, False if not.
        """

        if self.is_game_over():
            return False

        # Convert input and validate
        origin = self.__convert_to_numeric_tuple(currentCenter)
        destination = self.__convert_to_numeric_tuple(newCenter)
        if not origin or not destination:   # If input was invalid
            return False

        # Create piece object, move object, and validate
        piece = self._gameBoard.create_piece(origin)
        move = Move(origin, destination, piece, self._currentPlayer, self._gameBoard)
        if not move.is_legal():
            return False

        # Execute move and check for victory
        self._gameBoard.move_piece(piece, destination)
        if self.check_victory():
            self.assign_victory(self._currentPlayer)

        # Toggle whose turn it is
        self._currentPlayer = OPPONENT[self._currentPlayer]

        return True

    def is_input_coordinate_valid(self, coordinate):
        """
        Validate input, checking both for type of input and for out-of-bounds input.
        Receives coordinate and ensures it has the format <one letter, one number> eg. 'a15', 'b16', etc. 
        Column designation must be between 'b' and 's' inclusive. 
        Row designation must be between 1 and 18. 
        Parameters:
            coordinate (string): coordinate of location on board.
        Returns:
            True if valid, False if not.
        """

        # If input is not a string, return False
        if type(coordinate) != str:
            return False

        # Validate column. Column letter must be between 'b' and 's' inclusive.
        if coordinate[0].lower() not in COL_LETTERS[INNER_LOWER_BOUND:INNER_UPPER_BOUND+1]:
            return False

        # Validate row. Row index must be between 1 and 18 inclusive.
        try:
            rowIndex = int(coordinate[1:])
        except ValueError:  # If second part of coordinate is not a digit string
            return False
        else:
            if rowIndex < INNER_LOWER_BOUND or rowIndex > INNER_UPPER_BOUND:
                return False

        return True

    def __convert_to_numeric_tuple(self, coordinate):
        """
        Validates coordinate and, if it is valid,
        create tuples containing numerical row- and column- index of each coordinate.
        Presupposes input has been validated.
        Parameters:
            coordinate (string): board coordinate
        Returns:
            tuple containing numerical row- and column- index of coordinate
        """

        if not self.is_input_coordinate_valid(coordinate):
            return False

        return (int(coordinate[1:]), COL_LETTERS.index(coordinate[0].lower()))

    def is_game_over(self):
        """Returns True if game state is anything but unfinished."""

        if self.get_game_state == "UNFINISHED":
            return True
        return False

    def game_loop(self):
        """Represents one turn for each player."""
    
    def run_game(self):
        """Runs the game in the terminal. """

        while self._gameState == "UNFINISHED":
            print("Current player: ", self._currentPlayer)
            userInput = input("Enter origin center or press R to resign or Q to quit: ")
            if userInput == 'R':
                self.resign_game()
                print(self._currentPlayer + " chose to resign.")
            elif userInput == 'Q':
                print("Thanks for playing.")
                return
            else:
                origin = userInput
                dest = input("Enter destination: ")
                if not(self.make_move(origin, dest)):
                    print("\n Invalid move. Try again")
                else:
                    print()
                    self._gameBoard.display()
        print("Result: ", self.get_game_state())

def main():
    game = GessGame()
    print("Welcome to Gess!")
    game._gameBoard.display()
    game.run_game()

if __name__ == "__main__":
    main()