"""
Handles the placement of middle pieces in a jigsaw puzzle.
"""

import itertools
import copy

from piece_utils import PieceUtils

class SearchComplete(Exception):
    """
    Exception raised when a valid puzzle solution is found.
    """


class MiddlePlacer:
    """
    A class responsible for placing middle pieces in a jigsaw puzzle grid.
    """

    def __init__(self, columns, rows, middles):
        """
        Initializes the MiddlePlacer with puzzle dimensions and middle pieces.

        :param columns: Number of columns in the puzzle.
        :param rows: Number of rows in the puzzle.
        :param middles: List of middle pieces.
        """
        self.rows = rows
        self.columns = columns

        self.utils = PieceUtils()

        # Calculate all possible permutations as a generator
        self.middle_gen = itertools.permutations(middles)
        self.valid_positions = []

    def place_middles(self, start_positions):
        """
        Attempts to place all middle pieces in the puzzle grid.

        :param start_positions: 2D list representing puzzle positions with borders in place.
        :return: A list of valid middle piece placements.
        """
        while True:
            try:
                positions = copy.deepcopy(start_positions)
                self.next_ordering(positions)
            except StopIteration:
                return self.valid_positions
            except SearchComplete:
                pass

    def next_ordering(self, positions):
        """
        Attempts the next permutation of middle pieces.

        :param positions: 2D list representing puzzle positions.
        :raises StopIteration: If no more permutations exist.
        """
        ordering = next(self.middle_gen)  # Get next permutation of middle pieces
        self.try_piece(ordering, 0, 1, 1, positions)

    def try_piece(self, pieces, piece_idx, row, col, positions):
        """
        Recursively attempts to place each middle piece in the puzzle grid.

        :param pieces: List of middle pieces.
        :param piece_idx: Index of the piece being placed.
        :param row: Row index for placement.
        :param col: Column index for placement.
        :param positions: 2D list representing puzzle positions.
        :return: False if the piece cannot be placed; otherwise, raises SearchComplete.
        :raises SearchComplete: If all pieces are successfully placed.
        """
        piece = pieces[piece_idx]
        piece_id = piece[0]
        side_ids = piece[1:]

        # Try each rotation
        for _ in range(4):
            side_ids = self.utils.rotate_piece(side_ids)
            rotated = [piece_id, *side_ids]
            if self.utils.does_piece_fit(row, col, rotated, positions):
                positions[row][col] = rotated

                # Check if this is the last piece
                if piece_idx == (len(pieces) - 1):
                    print("All pieces fit in this order!")
                    self.valid_positions.append(positions)
                    raise SearchComplete("All pieces fit in this order!")

                # Recursively try next pieces
                newpos = self.next_middle_position(row, col)
                result = self.try_piece(pieces, piece_idx + 1, *newpos, positions)
                if result is False:
                    positions[row][col] = None
                else:
                    raise ValueError("SearchComplete should have been raised")

        return False

    def next_middle_position(self, row, col):
        """
        Determines the next position for placing a middle piece.

        :param row: Current row index.
        :param col: Current column index.
        :return: A tuple (row, col) indicating the next position.
        """
        if col == (self.columns - 2):
            return [row + 1, 1]
        return [row, col + 1]
