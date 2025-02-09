"""
Provides utility functions for manipulating and validating puzzle pieces.
"""

import constants

class PieceUtils:
    """
    A utility class for performing operations on puzzle pieces,
    such as rotating pieces and checking if they fit in a given position.
    """

    def rotate_piece(self, side_ids):
        """
        Rotates a piece by shifting its side IDs.

        :param side_ids: List of side IDs representing the edges of the piece.
        :return: A new list of side IDs after rotation.
        """
        first = side_ids[0]
        rotated = side_ids[1:]
        rotated.append(first)  # Remove the first element and add it to the end
        return rotated

    def edges_valid(self, vertical, horizontal, side_ids):
        """
        Checks if the specified edges have side_id=0, meaning a flat edge.

        :param vertical: The vertical position (TOP or BOTTOM) to check.
        :param horizontal: The horizontal position (LEFT or RIGHT) to check.
        :param side_ids: List of side IDs representing the edges of the piece.
        :return: True if both specified edges are flat (0), otherwise False.
        """
        if vertical is not None and side_ids[vertical] != 0:
            return False
        if horizontal is not None and side_ids[horizontal] != 0:
            return False
        return True

    def does_piece_fit(self, row, col, piece, positions):
        """
        Checks if a piece fits against all non-None adjacent pieces in the puzzle grid.

        :param row: The row position of the piece.
        :param col: The column position of the piece.
        :param piece: The piece being placed, represented by a list where the first element
                      is the piece ID and the rest are side IDs.
        :param positions: 2D list representing the current puzzle grid.
        :return: True if the piece fits, otherwise False.
        """
        side_ids = piece[1:]

        # Check the piece above
        side_id = side_ids[constants.TOP]
        if side_id != 0:
            above = positions[row-1][col]
            if above is not None:
                compare_side_ids = above[1:]
                if compare_side_ids[constants.BOTTOM] != side_id:
                    return False

        # Check the piece below
        side_id = side_ids[constants.BOTTOM]
        if side_id != 0:
            below = positions[row+1][col]
            if below is not None:
                compare_side_ids = below[1:]
                if compare_side_ids[constants.TOP] != side_id:
                    return False

        # Check the piece to the left
        side_id = side_ids[constants.LEFT]
        if side_id != 0:
            left = positions[row][col-1]
            if left is not None:
                compare_side_ids = left[1:]
                if compare_side_ids[constants.RIGHT] != side_id:
                    return False

        # Check the piece to the right
        side_id = side_ids[constants.RIGHT]
        if side_id != 0:
            right = positions[row][col+1]
            if right is not None:
                compare_side_ids = right[1:]
                if compare_side_ids[constants.LEFT] != side_id:
                    return False

        return True
