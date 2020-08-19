import unittest
from stone import *
from stoneCollection import StoneCollection
from board import BoardMixedUp
from piece import Piece
from move import Move
from Gess import GessGame

FOOTPRINT_SIZE = 3
BOARD_SIZE = 20

class Test_TestBoard(unittest.TestCase):
    """Tests Board"""

    def setUp(self):
        self.board = Board()    # board in regular starting layout
        self.mixed = BoardMixedUp()
        self.footprint = [['W', 'W', None], ['W', None, None], [None, 'W', 'W']] # sample footprint

    def test_outer_rows_clear_when_footprint_placed_at_edge1(self):
        """Tests that outer rows are empty when footprint is placed at the lower left edge"""

        self.board.place_footprint((1,1), self.footprint)
        for square in self.board._array[0]:
            self.assertIsNone(square)

    def test_outer_rows_clear_when_footprint_placed_at_edge2(self):
        """Tests that outer rows are empty when footprint is placed at far right edge"""

        self.board.place_footprint((11,18), self.footprint)
        for row in range(BOARD_SIZE):
            square = self.board._array[row][19]
            self.assertIsNone(square)

    def test_board_copy_equals_array(self):
        """Make sure copy == the array in Board"""

        copy = self.board.get_copy()
        self.assertEqual(self.board._array, copy)

    def test_board_copy_is_not_array(self):
        """Make sure copy is not the same object as the array in Board"""

        copy = self.board.get_copy()
        self.assertIsNot(self.board._array, copy)

    def test_has_ring_when_no_ring(self):
        """Tests that no ring is detected when no ring exists."""

        result = self.mixed.has_ring('W')
        self.assertFalse(result)
    
    def test_has_ring(self):
        """Tests that ring is accurately detected."""

        result = self.board.has_ring('B')
        self.assertTrue(result)

class Test_TestPiece(unittest.TestCase):
    """Tests for Piece class"""

    def setUp(self):

        self.board = Board()
        self.mixed = BoardMixedUp()

        # Invalid Piece: White Piece with only one stone in center
        self.centerStone = (13, 2) 
        self.invalidPiece = Piece(self.centerStone, self.board.get_footprint(self.centerStone), 'W') 

        # Invalid Piece: multiple stone colors
        self.center = (17, 13)
        self.invalidPiece2 = Piece(self.center, self.mixed.get_footprint(self.center), 'B') 
        
        # Valid Piece: valid for white. Has no center stone
        self.center2 = (15, 7) 
        self.validPiece = Piece(self.center2, self.board.get_footprint(self.center2), 'W') 
        
        # Valid for White. Has center stone (among others)
        self.center3 = (17, 2)
        self.validPiece2 = Piece(self.center3, self.board.get_footprint(self.center3), 'W') 


    # def test_directions_center_stone(self):
    #     """Tests that directions accurately registers center stone"""
        
    #     directions = self.invalidPiece.get_directions()

    #     self.assertEqual(directions, [(0,0)])

    def test_center_stone_invalid(self):
        """Tests that single center stone is recognized as illegal"""

        self.assertFalse(self.invalidPiece.is_legal('W'))

    def test_opponent_color_invalid(self):
        """Tests that Piece with opponent's color stones in footprint marked invalid"""

        self.assertFalse(self.invalidPiece2.is_legal('W'))

    def test_valid_piece_is_valid(self):
        """Tests that valid piece accurately marked legal"""

        self.assertTrue(self.validPiece.is_legal('W'))

    def test_directions_sample_piece(self):
        """Tests that directions are accurately gotten for a sample piece"""

        expected = [(1, -1), (1, 0), (1, 1)]
        self.assertEqual(self.validPiece.get_directions(), expected)

    def test_distance_center_stone(self):
        """Tests that distance is accurate (unlimited) for piece with stone in center"""

        self.assertIsNone(self.validPiece2.get_max_distance())

    def test_distance_no_center(self):
        """Tests that distance is 3 for piece without stone in center"""

        self.assertEqual(self.validPiece.get_max_distance(), 3)

class Test_TestMove(unittest.TestCase):
    """Tests for Move class."""

    def setUp(self):
        self.board = Board()
        self.center = (17, 2)
        #self.piece = Piece(self.center, self.board.get_footprint(self.center), 'W')
        #self.move = Move(self.piece, 'W', self.board.get_copy(), self.center, (13, 2))

    def test_move_with_obstructed_path(self):
        """Tests moving down 8 rows, but path is blocked by own piece."""

        center = (17, 2)
        invalidDest = (9,2)
        piece = Piece(center, self.board.get_footprint(center), 'W')
        move = Move(piece, 'W', self.board.get_copy(), center, invalidDest)

        self.assertFalse(move.is_trajectory_legal())   

    def test_move_legal_with_unobstructed_path(self):
        """Test black moving up 3 rows, with path unoccupied."""
        
        center = (5, 17)
        dest = (8, 17)
        piece = Piece(center, self.board.get_footprint(center), 'B')
        move = Move(piece, 'B', self.board.get_copy(), center, dest)
        
        self.assertTrue(move.is_trajectory_legal())

    def test_move_legal_invalid_direction(self):
        """Test moving direction the Piece can't move"""
        center = (12, 9)
        dest = (10, 9)
        piece = Piece(center, self.board.get_footprint(center), 'W')
        move = Move(piece, 'W', self.board.get_copy(), center, dest)
        
        self.assertFalse(move.is_trajectory_legal())

    def test_move_invalid_distance(self):
        """Tests moving a direction the Piece can't go."""
        center = (14, 10)
        dest = (10, 10)
        piece = Piece(center, self.board.get_footprint(center), 'W')
        move = Move(piece, 'W', self.board.get_copy(), center, dest)

        self.assertTrue(move.is_trajectory_legal)

    def test_valid_distance(self):
        """Checks if valid distance recognized as valid"""

        center = (12, 11)
        dest = (13, 11)
        piece = Piece(center, self.board.get_footprint(center), 'W')
        move = Move(piece, 'W', self.board.get_copy(), center, dest)

        self.assertTrue(move.is_distance_valid())

    def test_invalid_distance(self):
        """Test invalid ditsance for piece"""

        center = (12, 11)
        dest = (5, 11)
        piece = Piece(center, self.board.get_footprint(center), 'W')
        move = Move(piece, 'W', self.board.get_copy(), center, dest)
        self.assertFalse(move.is_distance_valid())

    def record_valid_move(self):
        center = (14, 2)
        dest = (13, 2)
        piece = Piece(center, self.board.get_footprint(center), 'W')
        move = Move(piece, 'W', self.board.get_copy(), center, dest)

        self.assertTrue(move.record())
    

if __name__ == '__main__':
    unittest.main()