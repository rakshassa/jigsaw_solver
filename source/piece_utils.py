import constants

class PieceUtils(object):
    # turn the piece. Keep the same ORDER - just rotate the array
    def rotate_piece(self, side_ids):
        first = side_ids[0]
        rotated = side_ids[1:]
        rotated.append(first) # remove the first element and add it to the end
        return rotated

    # returns True if the specified edges have side_id=0 (meaning: a flat side on the piece)
    def edges_valid(self, vertical, horizontal, side_ids):
        # since the constants used for vert/hor are good indexes
        if vertical != None and side_ids[vertical] != 0: return False
        if horizontal != None and side_ids[horizontal] != 0: return False

        return True

    # returns TRUE if the piece fits against all non-NONE adjacent pieces
    def does_piece_fit(self, row, col, piece, positions):
        # print("Trying Piece: %s fits at row: %i and col: %i" % (str(piece), row, col))
        side_ids = piece[1:]
        # check the piece above me
        side_id = side_ids[constants.TOP]
        if side_id != 0:
            above = positions[row-1][col]
            if above != None:
                compare_side_ids = above[1:]
                if compare_side_ids[constants.BOTTOM] != side_id:
                    # print("Mismatch above")
                    return False

        # check the piece below me
        side_id = side_ids[constants.BOTTOM]
        if side_id != 0:
            above = positions[row+1][col]
            if above != None:
                compare_side_ids = above[1:]
                if compare_side_ids[constants.TOP] != side_id:
                    # print("Mismatch below")
                    return False

        # check the piece to the left
        side_id = side_ids[constants.LEFT]
        if side_id != 0:
            above = positions[row][col-1]
            if above != None:
                compare_side_ids = above[1:]
                if compare_side_ids[constants.RIGHT] != side_id:
                    # print("Mismatch left piece: %s against: %s with side_id: %i and %i" % (str(piece), str(above), side_id, above[constants.RIGHT]))
                    return False

        # check the piece to the right
        side_id = side_ids[constants.RIGHT]
        if side_id != 0:
            above = positions[row][col+1]
            if above != None:
                compare_side_ids = above[1:]
                if compare_side_ids[constants.LEFT] != side_id:
                    # print("Mismatch Right")
                    return False

        # print("Piece: %s fits at row: %i and col: %i" % (str(piece), row, col))
        return True
