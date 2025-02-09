# side with number=0 is an edge
# The sides of the pieces are named sequentially, clockwise, starting with the left side.
# Each piece is numbered sequentially, and the first piece is the piece number 1.

class Sorter:
    def sort_pieces(self, pieces):
        corners = []
        sides = []
        middles = []

        for piece in pieces:
            side_ids = piece[1:] # ignore the piece_id
            zero_els = side_ids.count(0) # count how many zeros are in the side_ids

            if zero_els == 0:
                middles.append(piece)
            elif zero_els == 1:
                sides.append(piece)
            elif zero_els == 2:
                corners.append(piece)
            else:
                raise ValueError("We have a piece with 3 edges - Invalid")

        return corners, sides, middles
