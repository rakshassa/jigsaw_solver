"""
Calculates placement for Corner pieces.
"""

import itertools

import constants
from piece_utils import PieceUtils

class CornerPlacer:
    """
    A class responsible for placing corner pieces in a jigsaw puzzle.
    """

    def __init__(self, columns, rows, corners):
        """
        Initializes the CornerPlacer with puzzle dimensions and corner pieces.

        :param columns: Number of columns in the puzzle.
        :param rows: Number of rows in the puzzle.
        :param corners: List of corner pieces.
        """
        self.rows = rows
        self.columns = columns

        self.utils = PieceUtils()

        # self.corner_gen2 = itertools.permutations(corners[1:])
        # length = sum(1 for ignore in self.corner_gen2)
        # print("Total permutations for corners: %i" % length)

        # Calculate all possible permutations as a generator
        self.corner_gen = itertools.permutations(corners[1:])

    def place_corners(self, positions):
        """
        Places the three remaining corner pieces, assuming the first is fixed.

        :param positions: 2D list representing puzzle positions.
        :return: True if placement is successful, False if no more permutations exist.
        """
        try:
            ordering = next(self.corner_gen)  # Get next item from the generator
            self.place_corner(constants.TOP, constants.RIGHT, ordering[0], positions)
            self.place_corner(constants.BOTTOM, constants.LEFT, ordering[1], positions)
            self.place_corner(constants.BOTTOM, constants.RIGHT, ordering[2], positions)
        except StopIteration:
            return False

        return True

    def place_corner(self, vertical, horizontal, piece, positions):
        """
        Places a single corner piece at the specified position.

        :param vertical: Vertical placement (TOP or BOTTOM).
        :param horizontal: Horizontal placement (LEFT or RIGHT).
        :param piece: The corner piece to be placed.
        :param positions: 2D list representing puzzle positions.
        :raises ValueError: If the corner piece cannot be placed correctly.
        """
        # Determine placement coordinates
        row = 0 if vertical == constants.TOP else self.rows - 1
        column = 0 if horizontal == constants.LEFT else self.columns - 1
        # print("Placing piece at row: %i and column: %i" % (row, column))

        # Rotate the piece so the zero edges are in the correct place
        piece_id = piece[0]
        side_ids = piece[1:]

        # Try 4 rotations
        for _ in range(4):
            if self.utils.edges_valid(vertical, horizontal, side_ids):
                positions[row][column] = [piece_id, *side_ids]
                return

            # print("Before Rotation: " + str(side_ids))
            side_ids = self.utils.rotate_piece(side_ids)
            # print("After Rotation: " + str(side_ids))

        raise ValueError("Invalid Corner Piece: " + str(piece))
