import itertools
import copy

import Constants
from PieceUtils import PieceUtils

class SearchComplete(Exception):
    pass

class MiddlePlacer(object):
    def __init__(self, columns, rows, middles):
        self.rows = rows
        self.columns = columns

        self.utils = PieceUtils()
        self.middle_gen2 = itertools.permutations(middles) # calculate all possible permutations as a generator
        length = sum(1 for ignore in self.middle_gen2)
        # print("Total permutations for middles: %i" % length)
        self.middle_gen = itertools.permutations(middles) # calculate all possible permutations as a generator
        self.valid_positions = []

    def place_middles(self, start_positions):
        # print("Border Looks like this:")
        # print(start_positions)
        while(True):
            try:
                positions = copy.deepcopy(start_positions)
                self.next_ordering(positions)
            except StopIteration:
                # print("Done placing middle pieces")
                return self.valid_positions
            except SearchComplete:
                pass

    # returns FALSE when no more orderings exist
    # returns TRUE when all edges fit
    # throws KeyError when any piece doesn't fit
    def next_ordering(self, positions):
        ordering = next(self.middle_gen) # get next item from the generator

        # for each rotation of the first piece:
        #   if fits, recursively try the next piece in the next position
        #   if all pieces fit, then we have success in this ordering
        #   if any piece fails to fit in any rotation, return False (up one level of recursion)
            # try next rotation on previous piece
            # remove the previous piece from positions since that rotation failed to match next piece
            # if a new rotation fits, drop it in and recursion to next piece again.
        #   if first piece tried all 4 rotations without success, then we failed

        result = self.try_piece(ordering, 0, 1, 1, positions)
        if result:
            print("All middles fit")
            return True


    def try_piece(self, pieces, piece_idx, row, col, positions):
        piece = pieces[piece_idx]
        # print("Trying Piece: %s in row: %i col: %i" % (str(piece), row, col))

        piece_id = piece[0]
        side_ids = piece[1:]

        # try each rotation
        for _ in range(4):
            side_ids = self.utils.rotate_piece(side_ids)
            rotated = [piece_id, *side_ids]
            if self.utils.does_piece_fit(row, col, rotated, positions):
                # add it to the puzzle - we can remove it if next pieces fail
                positions[row][col] = rotated
                # print("Placing Piece: %s in row: %i col: %i" % (str(rotated), row, col))

                # is this the last piece?
                if piece_idx == (len(pieces)-1):
                    print("All pieces fit in this order!")

                    # store the correct answer
                    self.valid_positions.append(positions)

                    # exit the recursion
                    raise SearchComplete("All pieces fit in this order!")

                # recursively try next pieces
                result = self.try_piece(pieces, piece_idx+1, *self.next_middle_position(row, col), positions)
                if result == False:
                    # remove this piece and try other rotations
                    positions[row][col] = None
                else:
                    raise ValueError("should never get here because all pieces fit and SearchComplete should have been raised")
            else:
                # the piece doesn't fit in this rotation, try the next rotation
                pass

        # None of the rotations fit, go back and try the previous piece in a new rotation
        # print("No Rotations Fit - reverting")
        return False

    # never lives in first row, last row, first col, or last col
    def next_middle_position(self, row, col):
        if (col == (self.columns-2)):
            return [row+1, 1]

        return [row, col+1]

