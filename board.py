from stone import *
from stoneCollection import StoneCollection
from piece import Piece
from move import Move

class Board:
    """
    Represents the GessGame board: a collection of stones belonging to each side.
    
    Board class is responsible for recording moves and captures, checking if a path is clear
    between one location and another, and checking whether a given player still has a ring alive.
    """

    def __init__(self):
        """
        Board has a StoneCollection representing the stones on the Gess board.
        """

        self._allStones = StoneCollection()

    def create_piece(self, center):
        """
        Creates Piece with the stones about the given center.
        
        :param: center (tuple): center of desired piece
        :return: Piece object
        """

        stoneList = self._allStones.get_stones_about_center(center)
        piece = Piece(center, stoneList)

        return piece

    def capture(self, center):
        """Captures stones about a given center, i.e. removes all stones in the 3x3 area."""

        capturedStones = self._allStones.get_stones_about_center(center)
        for stone in capturedStones:
            if not stone.is_hidden():   # Hidden stones belong to a piece and shouldn't be removed.
                self._allStones.remove(stone.get_location())

    def move_piece(self, piece, destination):
        """
        Takes a Piece and moves all its stones to a given destination.
        Deletes all stones that the Piece would overlap, i.e. all stones at the Piece's destination.
        """

        piece.pick_up()  # Hides stones in Piece
        self.capture(destination) # "Capture" (i.e. delete) non-hidden stones at destination
        piece.put_down(destination) # Move piece stones

        # If any stones have gone out of bounds, remove them
        for stone in piece.get_stone_list():
            if 20 in stone.get_location() or 1 in stone.get_location():
                self._allStones.remove(stone.get_location())

    def is_path_clear(self, piece, origin, destination, direction):
        """
        Checks if there are any obstructions (stones of either color) between origin and destination.
        Returns True if path is clear, False if there is an obstruction.
        """

        piece.pick_up() # Hide origin and destination

        # Trace path from origin center to destination center and check for stones
        isClear = True
        center = origin
        while center != destination and isClear == True:
            stones = self._allStones.get_stones_about_center(center)
            stonesAboutCenter = StoneCollection(stones)
            if not stonesAboutCenter.is_empty():
                isClear = False
            center = (center[0] + direction[0], center[1] + direction[1])

        piece.put_down(origin)  # Replace piece (un-hide its stones)

        return isClear

    def has_ring(self, player):
        """
        Checks if this player still has a ring.
        A ring is a 3x3 area filled with same-color pieces except at its center.
        Because outer rows/columns of board are out-of-bounds, ring center could only be
        at [3...18] inclusive.
        Function loops through gameboard coordinates, treating every empty square as potential ring center.
        If 8 unhidden stones are found (center is guaranteed empty), it is a ring.
        :param: player (string): "WHITE" or "BLACK" to look for their ring
        :return: True if this player has a ring, False if not
        """

        # Loop through board coordinates
        for row in range(INNER_LOWER_BOUND+1, INNER_UPPER_BOUND):
            for col in range(INNER_LOWER_BOUND+1, INNER_UPPER_BOUND):
                # Treat any empty stone as center
                if self._allStones.get_stone_at_location((row, col)) is None:
                    stoneList = self._allStones.get_stones_about_center((row, col))    # Get stones in footprint
                    anyHidden = False
                    for stone in stoneList:
                        if stone.is_hidden():
                            anyHidden = True
                    if len(stoneList) == COUNT_FOR_RING and not anyHidden: # Hidden stones don't count
                        potentialRing = Piece((row, col), stoneList)
                        if not potentialRing.contains_color(OPPONENT[player]):  # Check for opponent stones
                            return True

        return False

    def display(self):
        """Displays board for debug purposes."""

        # Print column letters along top
        print('     ', end='')
        for i in range(1, 21):
            print(COL_LETTERS[i], end="   ")
            # if i < 10:
            #     print("  " + str(i) + " ", end='')
            # else:
            #     print(" " + str(i) + " ", end='')
        print()

        for row in range(BOARD_SIZE, 0, -1):
            if row < 10:
                print(str(row) + "  | ", end='')
            else:
                print(str(row) + ' |', end=' ')
            for col in range(1, BOARD_SIZE + 1):
                stone = self._allStones.get_stone_at_location((row, col))
                if stone is None:
                    print('-', end=' | ')
                else:
                    if stone.get_owner() == "WHITE":
                        print('W', end=' | ')
                    else:
                        print('B', end=' | ')
            print()

class BoardMixedUp(Board):
    """
    Identical to Board except initializes to different starting layouts, for testing purposes.

    Here the white and black pieces are all mixed up. 
    Used for testing if Piece effectively determines its legality.
    There are no rings here, so used for testing the hasRing function too.
    
    """

    def fillStartingLayout(self):
        """
        Populates Board with game pieces in their starting layout. Black pieces are represented by 'B', white pieces by 'W'
        """

        layout = [[None for i in range(self._height)] for j in range(self._width)]

        # Describes column locations of stones in a given row.
        # "First row" denotes player's first row of pieces--those closest to them.
        firstAndThirdRow = [2, 4, 6, 7, 8, 9, 10, 11, 12, 13, 15, 17]
        secondRow = [1, 2, 3, 5, 7, 8, 9, 10, 12, 14, 16, 17, 18]
        fourthRow = [2, 5, 8, 11, 14, 17]

        # Here, rows 2 and 17 are swapped, so stones are jumbled and there's no valid ring
        whiteStones = {18: firstAndThirdRow, 2: secondRow, 16: firstAndThirdRow, 13: fourthRow}
        blackStones = {1: firstAndThirdRow, 17: secondRow,  3: firstAndThirdRow, 6: fourthRow}

        for row in whiteStones:
            for column in whiteStones[row]:
                layout[row][column] = 'W'
        for row in blackStones:
            for column in blackStones[row]:
                layout[row][column] = 'B'     

        return layout       