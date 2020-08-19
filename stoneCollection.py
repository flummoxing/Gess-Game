from stone import *

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
