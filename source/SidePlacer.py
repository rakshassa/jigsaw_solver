import itertools
import copy
import Constants
from PieceUtils import PieceUtils

class SidePlacer(object):
    def __init__(self, columns, rows, sides):
        self.rows = rows
        self.columns = columns
        # print("sideplacer rows: %i col: %i" % (rows, columns))

        self.utils = PieceUtils()
        # self.side_gen2 = itertools.permutations(sides) # calculate all possible permutations as a generator
        # length = sum(1 for ignore in self.side_gen2)
        # print("Total permutations for sides: %i" % length)
        self.side_gen = itertools.permutations(sides) # calculate all possible permutations as a generator
        self.valid_positions = []

    def place_sides(self, corner_placements):
        while(True):
            try:
                positions = copy.deepcopy(corner_placements)
                result = self.next_ordering(positions)
            except StopIteration:
                # this exception is thrown when the ordering generator is exhausted
                # print("Done placing side pieces")
                return self.valid_positions
            except KeyError:
                # something didn't fit - try the next ordering
                pass

    # returns FALSE when no more orderings exist
    # returns TRUE when all edges fit
    # throws KeyError when any piece doesn't fit
    def next_ordering(self, positions):
        ordering = None
        ordering = next(self.side_gen) # get next item from the generator

        # exit if any piece doesn't match adjacent pieces after fully rotating it
        # NOTE: edge pieces can only fit in one rotation, so no need to try other rotations
        element_idx = 0

        # for each side piece - rotate to the appropriate edge then attempt matching
        for idx in range(self.columns-2):
            col = idx+1 # skipping the corner slot

            # TOP
            # print("Try top")
            piece = ordering[element_idx]
            element_idx += 1
            rotated = self.rotate_side(Constants.TOP, None, piece)
            self.place_side(0, col, rotated, positions)

            # BOTTOM
            # print("try bottom")
            piece = ordering[element_idx]
            element_idx +=1
            rotated = self.rotate_side(Constants.BOTTOM, None, piece)
            self.place_side(self.rows-1, col, rotated, positions) # bottom

        # for each middle row
        # attempt to place in next open side slot (next row left-edge then right-edge)
        for idx2 in range(self.rows-2):
            row = idx2 + 1 # skipping corner slot

            # print("Try Left")
            piece = ordering[element_idx]
            element_idx +=1
            rotated = self.rotate_side(None, Constants.LEFT, piece)
            self.place_side(row, 0, rotated, positions) # LEFT

            # print("Try right")
            piece = ordering[element_idx]
            element_idx +=1
            rotated = self.rotate_side(None, Constants.RIGHT, piece)
            self.place_side(row, self.columns-1, rotated, positions) # RIGHT

        print("All sides fit")
        self.valid_positions.append(positions)
        return True

    def place_side(self, row, col, piece, positions):
        # validate that it fits with all adjacent pieces
        if self.utils.does_piece_fit(row, col, piece, positions):
            positions[row][col] = piece
            return

        raise KeyError("This piece does not fit")

    # rotate the pice so the ZERO edges are in the right place
    def rotate_side(self, vertical, horizontal, piece):
        piece_id = piece[0]
        side_ids = piece[1:]

        # try 4 rotations
        for _ in range(4):
            if self.utils.edges_valid(vertical, horizontal, side_ids):
                rotated = [piece_id, *side_ids]
                return rotated

            # print("Before Rotation: " + str(side_ids))
            side_ids = self.utils.rotate_piece(side_ids)
            # print("After Rotation: " + str(side_ids))

        raise ValueError("Invalid Side Piece: " + str(piece))
