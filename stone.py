BOARD_SIZE = 20
# Columns designated with these letters. None aligns to 1-indexing
COL_LETTERS = [None, 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
               'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't']
# Outermost edges of 20x20 board
OUTER_LOWER_BOUND = 1
OUTER_UPPER_BOUND = BOARD_SIZE
# Actual gameplay area is the 18x18 square within the complete board
INNER_LOWER_BOUND = 2
INNER_UPPER_BOUND = BOARD_SIZE - 1

COUNT_FOR_RING = 8

OPPONENT = {"WHITE": "BLACK", "BLACK": "WHITE"}

class Stone:
    """
    Represents one of the 43 stones belonging to a player in Gess. Can be hidden to allow Move to perform tests without
    affecting the location of the Stone.
    """

    def __init__(self, location, owner):
        """Constructor for Stone class."""
        self._row = location[0]
        self._column = location[1]
        self._owner = owner
        self._hidden = False

    def get_location(self):
        """Returns stone's location on GessGame board, as a tuple (row, column)."""

        return (self._row, self._column)

    def get_owner(self):
        """Returns which player owns this stone."""

        return self._owner

    def is_hidden(self):
        """Returns whether stone is hidden."""

        return self._hidden

    def move(self, rowDisp, colDisp):
        """
        Translates stone by given displacement.
        Parameters:
            rowDisp, colDisp: (int) row and column displacement.
        """

        self._row += rowDisp
        self._column += colDisp

    def hide(self):
        """Hides the Stone."""

        self._hidden = True

    def reveal(self):
        """Makes Stone no longer hidden."""

        self._hidden = False

    def __str__(self):
        return (self._owner + " stone at row " + str(self._row) + ", column " + str(self._column))

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self._owner!r}, {(self._row, self._column)!r})')
