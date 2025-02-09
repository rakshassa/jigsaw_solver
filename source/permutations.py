"""
Handles generating permutations of corner placements in a jigsaw puzzle.
"""

import copy

import constants
from corner_placer import CornerPlacer

class Permutations:
    """
    A class responsible for generating permutations of corner placements in a jigsaw puzzle.
    """

    def __init__(self, columns, rows, corners):
        """
        Initializes the Permutations object with puzzle dimensions and corner pieces.

        :param columns: Number of columns in the puzzle.
        :param rows: Number of rows in the puzzle.
        :param corners: List of corner pieces.
        """
        self.rows = rows
        self.columns = columns
        self.corners = corners

        self.corner_handler = CornerPlacer(columns, rows, corners)
        self.initialize_puzzle()

    def initialize_puzzle(self):
        """
        Initializes the puzzle by creating an empty grid and placing the first corner.
        """
        self.base_positions = self.__build_empty_positions()

        # Hardcoding one arbitrary corner piece in the top-left
        # ensures we skip rotated solutions that are otherwise identical.
        self.corner_handler.place_corner(constants.TOP, constants.LEFT, self.corners[0], self.base_positions)

        print("After initial corner placement:")
        print(self.base_positions)

    def next_corner(self):
        """
        Generates the next valid corner placement permutation.

        :return: A 2D list representing the puzzle positions with corners placed,
                 or None if no more permutations exist.
        """
        positions = copy.deepcopy(self.base_positions)

        if not self.corner_handler.place_corners(positions):
            print("There are no more corner positions available")
            return None

        return positions

    def __build_empty_positions(self):
        """
        Creates an empty 2D list to represent puzzle positions.

        :return: A 2D list initialized with None values.
        """
        return [[None] * self.columns for _ in range(self.rows)]
