import copy

import constants
from corner_placer import CornerPlacer

class Permutations(object):
    def __init__(self, columns, rows, corners):
        self.rows = rows
        self.columns = columns
        self.corners = corners

        self.corner_handler = CornerPlacer(columns, rows, corners)
        self.initialize_puzzle()

    def initialize_puzzle(self):
        self.base_positions = self.__build_empty_positions()

        # hard coding one arbitrary corner piece in the top/left ensures we skip rotated solutions that are otherwise identical
        self.corner_handler.place_corner(constants.TOP, constants.LEFT, self.corners[0], self.base_positions)

        print("After initial corner placement:")
        print(self.base_positions)

    def next_corner(self):
        positions = copy.deepcopy(self.base_positions)

        if self.corner_handler.place_corners(positions) == False:
            print("There are no more corner positions available")
            return None
        # print("All corners placed: " + str(positions))
        return positions


    ####################################################################

    # start with an array of arrays of the appropriate size (filled with None values)
    def __build_empty_positions(self):
        result = []
        for _ in range(self.rows):
            row = [None] * self.columns
            result.append(row)

        return result
