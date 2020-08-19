from piece import Piece
from stone import *
from stoneCollection import StoneCollection

class Move:
    """
    Represents a move in the Gess game.
    
    This Move class is aware of the parameters of the particular move being made. In other words, it knows which player is making the move, what Stones are currently on the board, and where the player is trying to move from and to.
    The Move class is responsible for determining the legality (according to the rules of Gess) of the move its instance represents.
    """

    def __init__(self, originTuple, destinationTuple, piece, currentPlayer, board):
        self._origin = originTuple
        self._destination = destinationTuple
        self._currentPlayer = currentPlayer
        self._board = board
        self._piece = piece
        self._rowDisplacement = self._destination[0] - self._origin[0]
        self._colDisplacement = self._destination[1] - self._origin[1]
        self._direction = self.__determine_direction()

    def __determine_direction(self):
        """
        Determines direction this Piece is traveling in.
        
        Returns:
            direction (tuple): (row-increase/decrease, column-increase/decrease) 
                e.g. (1,0) means move is horizontal to the west
        """

        rowDirection = 0
        colDirection = 0

        # Check for increasing or decreasing column direction
        if self._colDisplacement != 0:
            colDirection = self._colDisplacement // abs(self._colDisplacement)
        # Check for increasing or decreasing row direction
        if self._rowDisplacement != 0:
            rowDirection = self._rowDisplacement // abs(self._rowDisplacement)

        return (rowDirection, colDirection)

    def is_direction_valid(self):
        """
        Cross-references with its Piece to see if the Piece can actually move in the intended
        direction. Also checks that movement is properly diagonal.
        
        Returns True if the direction is valid, False if not.
        """
        
        # If movement is not horizontal or vertical, check that it is properly diagonal
        if self._rowDisplacement and self._colDisplacement:
            if abs(self._rowDisplacement) != abs(self._colDisplacement):
                return False

        # Check if Piece has this direction tuple
        if self._direction not in self._piece.get_directions():
            return False

        return True

    def is_distance_valid(self):
        """
        Determines the distance this move is attempting to traverse, and references
        with Piece to see if the Piece can legally travel that far.
        Returns True if Piece can travel that distance, False if not.
        """

        # None if Piece can move any distance
        maxDistance = self._piece.get_max_distance()

        # If there is a max distance, check that displacement does not exceed it
        if self._piece.get_max_distance() is not None:
            if abs(self._rowDisplacement) > maxDistance or abs(self._colDisplacement) > maxDistance:
                return False

        return True

    def is_legal(self):
        """
        Checks if this Move is legal.
        The Piece must be a valid piece for the current player.
        The move's path must be clear, its distance and direction must correspond with Piece,
        and the move cannot destroy the player's own last ring.
        Returns True if the move is legal, False if not.
        """

        self._piece.pick_up()  # Hide piece to be able to check that last ring is not being broken

        legalPiece = self._piece.is_legal(self._currentPlayer)
        validDirection = self.is_direction_valid()
        validDistance = self.is_distance_valid()
        if not (legalPiece and validDirection and validDistance):
            return False

        ringUnbroken = self._board.has_ring(self._currentPlayer)
        pathClear = self._board.is_path_clear(self._piece, self._origin, self._destination, self._direction)
        if not (ringUnbroken and pathClear):
            return False

        self._piece.put_down(self._origin)  # Un-hide piece

        return True
