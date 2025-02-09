"""
Places side pieces inside an already arranged border
Verifies placements are valid
Finds all valid permutations including all rotations of pieces
"""

import itertools
import copy

import constants
from piece_utils import PieceUtils

class SidePlacer:
    """
    A class responsible for placing side pieces in a puzzle grid.
    It generates all possible permutations of side pieces and attempts to fit them correctly.
    """
    def __init__(self, columns, rows, sides):
        """
        Initializes the SidePlacer with the puzzle dimensions and side pieces.

        :param columns: Number of columns in the puzzle grid.
        :param rows: Number of rows in the puzzle grid.
        :param sides: List of side pieces to be placed.
        """
        self.rows = rows
        self.columns = columns
        self.utils = PieceUtils()

        # Generator for all possible permutations of side pieces
        self.side_gen = itertools.permutations(sides)
        self.valid_positions = []

    def place_sides(self, corner_placements):
        """
        Attempts to place side pieces in all possible valid positions.

        :param corner_placements: The puzzle grid with corner pieces placed.
        :return: A list of valid puzzle configurations with sides placed.
        """
        while True:
            try:
                positions = copy.deepcopy(corner_placements)
                self.next_ordering(positions)
            except StopIteration:
                return self.valid_positions  # No more permutations available
            except KeyError:
                pass  # Skip invalid configurations

    def next_ordering(self, positions):
        """
        Retrieves the next ordering of side pieces and attempts to place them.

        :param positions: The puzzle grid with corner pieces placed.
        :return: True if all sides fit correctly, otherwise raises KeyError.
        """
        ordering = next(self.side_gen)  # Get the next permutation of side pieces
        element_idx = 0

        # Place top and bottom side pieces
        for idx in range(self.columns - 2):
            col = idx + 1  # Skip corner slots

            piece = ordering[element_idx]
            element_idx += 1
            rotated = self.rotate_side(constants.TOP, None, piece)
            self.place_side(0, col, rotated, positions)  # Top side

            piece = ordering[element_idx]
            element_idx += 1
            rotated = self.rotate_side(constants.BOTTOM, None, piece)
            self.place_side(self.rows - 1, col, rotated, positions)  # Bottom side

        # Place left and right side pieces
        for idx2 in range(self.rows - 2):
            row = idx2 + 1  # Skip corner slots

            piece = ordering[element_idx]
            element_idx += 1
            rotated = self.rotate_side(None, constants.LEFT, piece)
            self.place_side(row, 0, rotated, positions)  # Left side

            piece = ordering[element_idx]
            element_idx += 1
            rotated = self.rotate_side(None, constants.RIGHT, piece)
            self.place_side(row, self.columns - 1, rotated, positions)  # Right side

        print("All sides fit")
        self.valid_positions.append(positions)
        return True

    def place_side(self, row, col, piece, positions):
        """
        Places a side piece at the specified position if it fits.

        :param row: Row index where the piece is to be placed.
        :param col: Column index where the piece is to be placed.
        :param piece: The side piece to be placed.
        :param positions: The current puzzle grid.
        :raises KeyError: If the piece does not fit in the given position.
        """
        if self.utils.does_piece_fit(row, col, piece, positions):
            positions[row][col] = piece
            return
        raise KeyError("This piece does not fit")

    def rotate_side(self, vertical, horizontal, piece):
        """
        Rotates a side piece until it has the correct orientation
        with flat edges facing the puzzle border.

        :param vertical: Specifies whether the piece is on the top or bottom edge.
        :param horizontal: Specifies whether the piece is on the left or right edge.
        :param piece: The side piece to be rotated.
        :return: The correctly rotated side piece.
        :raises ValueError: If the piece cannot be rotated to a valid orientation.
        """
        piece_id = piece[0]
        side_ids = piece[1:]

        for _ in range(4):  # Try all four rotations
            if self.utils.edges_valid(vertical, horizontal, side_ids):
                return [piece_id, *side_ids]
            side_ids = self.utils.rotate_piece(side_ids)

        raise ValueError("Invalid Side Piece: " + str(piece))
