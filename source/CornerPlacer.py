import itertools

import Constants
from PieceUtils import PieceUtils

class CornerPlacer(object):
    def __init__(self, columns, rows, corners):
        self.rows = rows
        self.columns = columns

        self.utils = PieceUtils()

        self.corner_gen2 = itertools.permutations(corners[1:])
        length = sum(1 for ignore in self.corner_gen2)
        print("Total permutations for corners: %i" % length)

        # calculate all possible permutations as a generator
        self.corner_gen = itertools.permutations(corners[1:])

    # place the 3 remaining corners (first one is always fixed in top/left)
    def place_corners(self, positions):
        try:
            ordering = next(self.corner_gen) # get next item from the generator
            self.place_corner(Constants.TOP, Constants.RIGHT, ordering[0], positions)
            self.place_corner(Constants.BOTTOM, Constants.LEFT, ordering[1], positions)
            self.place_corner(Constants.BOTTOM, Constants.RIGHT, ordering[2], positions)
        except StopIteration:
            return False

        return True

    def place_corner(self, vertical, horizontal, piece, positions):
        # determine placement
        row = 0 if vertical == Constants.TOP else self.rows-1
        column = 0 if horizontal == Constants.LEFT else self.columns-1
        # print("Placing piece at row: %i and column: %i" % (row, column))

        # rotate the pice so the ZERO edges are in the right place
        piece_id = piece[0]
        side_ids = piece[1:]

        # try 4 rotations
        for _ in range(4):
            if self.utils.edges_valid(vertical, horizontal, side_ids):
                # print("Rows: %i, top-left: %s, next: %s" % (len(positions), str(positions[0][0]), str(positions[0][1])))
                # print("Placed corner: %s at row: %i and column: %i" % (str(side_ids), row, column))
                positions[row][column] = [piece_id, *side_ids]
                # print("Rows: %i, top-left: %s, next: %s" % (len(positions), str(positions[0][0]), str(positions[0][1])))
                return

            # print("Before Rotation: " + str(side_ids))
            side_ids = self.utils.rotate_piece(side_ids)
            # print("After Rotation: " + str(side_ids))

        raise ValueError("Invalid Corner Piece: " + str(piece))
