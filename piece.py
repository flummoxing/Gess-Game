from stone import Stone
from stoneCollection import StoneCollection

class Piece:
    """
    A Piece is a 3x3 group of Stones. It can contain up to 9 of a given player's stones.
    A player's piece cannot contain stones that belond to the opposite player.
    A Piece has a set of valid directions it can move, depending on the locations of its stones:
        NW  N   NE
        W       E
        SW  S   SE
    """

    def __init__(self, center, stones):
        """
        Constructor for Piece class.
        Piece is initialized with a center and a list of the stones it contains.
        A Piece has a set of valid directions it can move, depending on the locations of its stones:
            NW  N   NE
            W       E
            SW  S   SE
        The Piece class represents these directions with a set of tuples (row displ., col displ.):
        (1, -1)   (1, 0)    (1, 1)
        (0, -1)   (0, 0)    (0, 1)
        (-1, -1)  (-1, 0)   (-1, 1)
        This reflects the layout of the board: (1, 1) means the Piece can travel in the positive row and column direction. (-1, 1) means Piece can travel in negative row direction and positive column direction.
        A Piece can travel an unlimited unobstructed distance if it has a stone in the center. Otherwise, it can travel up to 3 squares in one move.
        Parameters:
            center: (tuple) (row, column) of the Piece's center
            stones: (list) of the Stone objects within the Piece's 3x3 area.
        """

        self._center = center
        self._stoneList = stones
        self._directions = self.__determine_directions()
        self._maxDistance = self.__determine_max_distance()

    def __determine_directions(self):
        """Determines which directions the Piece can move and returns these as a list."""

        directions = []
        for stone in self._stoneList:
            stoneCoords = stone.get_location()  # (row-index, column-index)
            directionTuple = (
                stoneCoords[0] - self._center[0], stoneCoords[1] - self._center[1])
            directions.append(directionTuple)

        if (0, 0) in directions:        # Center has no bearing on direction, so remove
            directions.remove((0, 0))

        return directions

    def __determine_max_distance(self):
        """
        Determine how far the Piece is allowed to move.
        If there is a stone in the Piece's center, it can move any (unobstructed) distance.
        Otherwise, it can move up to 3 squares.
        Returns:
            maxDistance (int or None): Maximum distance Piece can travel
        """
        maxDistance = 3

        for stone in self._stoneList:
            if stone.get_location() == self._center:     # If there is a stone in the center
                maxDistance = None

        return maxDistance

    def get_stone_list(self):
        """Returns Piece's list of Stones."""

        return self._stoneList

    def get_directions(self):
        """Returns the list of valid direction tuples in which the piece can move."""

        return self._directions

    def get_max_distance(self):
        """Returns the maximum distance a Piece can move."""

        return self._maxDistance

    def contains_color(self, color):
        """
        Checks if this Piece contains at least one stone of given color.
        Returns True if Piece contains at least one stone of given color, False if not.
        """

        for stone in self._stoneList:
            if stone.get_owner() == color:
                return True

        return False

    def is_legal(self, player):
        """
        Determines whether this instance of Piece is legal for whoever is playing it.
        Rules:
        3x3 piece cannot contain stones of opponent's color or be empty.
        A piece with one single stone in the center is invalid because it has no valid directions.
        Returns True if Piece is legal, False if not.
        """

        oneCenterStone = False
        if len(self._stoneList) == 1:
            if self._stoneList[0].get_location == self._center:
                oneCenterStone = True

        conditions = [not self.contains_color(OPPONENT[player]), self._stoneList, not oneCenterStone]

        if not all(conditions):
            return False

        return True

    def pick_up(self):
        """ 'Picks up' Piece, temporarily hiding it from other operations."""

        for stone in self._stoneList:
            stone.hide()

    def put_down(self, destination):
        """Places Piece in a given location, unhiding its stones and updating its stones' locations."""

        displ = get_displacement(self._center, destination)

        for stone in self._stoneList:
            stone.reveal()
            stone.move(displ[0], displ[1])
