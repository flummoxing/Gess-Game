# Author: Alexa Langen
# Date: 1 June 2020
# Description: An implementation of an abstract board game called Gess. Rules
# can be found here: https://www.chessvariants.com/crossover.dir/gess.html


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


class StoneCollection:
    """Represents a collection of stones."""

    def __init__(self, stoneList=None):
        """
        Constructor for StoneCollection. 
        Parameters:
            stoneList: (list of Stone objects). If None, StoneCollection is populated
            to contain the Stones present in the initial GessGame layout.
        """

        if stoneList is None:
            self._stoneList = self.populate()
        else:
            self._stoneList = stoneList

    def get_stone_list(self):
        """Returns a copy of the list of Stones in the Army."""

        return list(self._stoneList)

    def is_empty(self):
        """Returns True if self._stoneList is an empty list OR if it contains only hidden stones."""

        for stone in self._stoneList:
            if not stone.is_hidden():
                return False

        return True

    def get_stone_at_location(self, targetLoc):
        """
        Searches for stone at target location. 
        Parameters:
            targetLoc (tuple): (row-index, column-index) of desired Stone.
        Return:
            Stone object at target location, or None if not found.
        """

        for stone in self._stoneList:
            if stone.get_location() == targetLoc:
                return stone

        return None

    def get_stones_about_center(self, center):
        """
        Takes a tuple (row-index, column-index) and searches for Stones in the 3x3 area,
        i.e. the Stones (if any) the given center location and those
        immediately adjacent to that location (left, right, top, bottom, and diagonal).
        Returns a list of any stones it finds.
        Parameters:
            center (tuple): (row-index, column-index) of desired center.
        Returns:
            list of Stone objects at locations including and adjacent to the center (returns an empty list
            if no such stones were found at those locations).
        """

        locationsToSearch = []

        # Get coordinates of 3x3 area
        for rowOffset in range(-1, 2):
            for colOffset in range(-1, 2):
                locationsToSearch.append(
                    (center[0] + rowOffset, center[1] + colOffset))

        stonesAboutCenter = []

        # Search collection for stones located within the 3x3 area
        for coordinate in locationsToSearch:
            # If stone is found
            if self.get_stone_at_location(coordinate) is not None:
                stonesAboutCenter.append(
                    self.get_stone_at_location(coordinate))

        return stonesAboutCenter

    def remove(self, targetLoc):
        """
        Removes stone at target location from collection. If no such stone exists, returns False.
        """

        for stone in self._stoneList:
            if stone.get_location() == targetLoc:
                self._stoneList.remove(stone)
                return True
        return False

    def populate(self):
        """
        Populates StoneCollection with list of Stones from the GessGame starting layout.
        Updates StoneCollection's stoneList.
        """

        stoneList = []

        # Describes column locations of stones in a given row.
        # "First row" denotes player's first row of pieces--those closest to them.
        firstRank = [3, 5, 7, 8, 9, 10, 11, 12, 13, 14, 16, 18]
        secondRank = [2, 3, 4, 6, 8, 9, 10, 11, 13, 15, 17, 18, 19]
        thirdRank = firstRank
        fourthRank = [3, 6, 9, 12, 15, 18]

        # How each player has pieces laid out initially
        stoneLayout = {"WHITE": {19: firstRank, 18: secondRank, 17: thirdRank, 14: fourthRank},
                       "BLACK": {2: firstRank, 3: secondRank, 4: thirdRank, 7: fourthRank}}

        for playerColor in stoneLayout:
            for row in stoneLayout[playerColor]:
                for column in stoneLayout[playerColor][row]:
                    stoneList.append(Stone((row, column), playerColor))

        return stoneList


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

        # Print column #s along top
        print('   ', end='')
        for i in range(1, 21):
            if i < 10:
                print("  " + str(i) + " ", end='')
            else:
                print(" " + str(i) + " ", end='')
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
            # for stone in self._allStones.get_stone_list():
            #     if stone.get_location() == (row, col):
            #         if stone.get_owner == "WHITE":
            #             print('W', end =' ')
            #         else:
            #             print('B', end = ' ')
            #     print('-', end = ' ')
            # print()


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

        return (int(coordinate[1:]), COL_LETTERS.index(coordinate[0]))

    def is_game_over(self):
        """Returns True if game state is anything but unfinished."""

        if self.get_game_state == "UNFINISHED":
            return True
        return False


def get_displacement(origin, destination):
    """Returns a tuple with the row and column displacement between origin and destination."""

    return (destination[0] - origin[0], destination[1] - origin[1])


# game = GessGame()

# print()
# print()
# game._gameBoard.display()

# while True:
#     print("Current game state: ", game.get_game_state())
#     print("Current player: ", game._currentPlayer)
#     origin = input("Enter origin center or press R to resign or Q to quit: ")
#     if origin == 'R':
#         game.resign_game()
#         print(game.get_game_state())
#         break
#     if origin == 'Q':
#         break
#     dest = input("Enter destination: ")
#     print(game.make_move(origin, dest), end=' ')
#     for column_index in range(BOARD_SIZE):
#         print(COL_LETTERS[column_index], ":", column_index, ", ", end=' ') #guidelines, remove
#     print()
#     game._gameBoard.display()
