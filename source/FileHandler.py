class FileHandler(object):
    def read_file(self, filename):
        lines = None

        with open(filename, 'r') as input_file:
            lines = input_file.readlines()

        columns, rows = self.parse_puzzle_size(lines[0])
        pieces = self.parse_pieces(lines[1:])

        return columns, rows, pieces

    def parse_puzzle_size(self, data):
        values = data.split(' ')
        return int(values[0]), int(values[1])

    # first item in each piece is the piece's unique Number
    # the next 4 items are the side_ids in clockwise order
    def parse_pieces(self, data):
        parsed = []
        for idx, piece in enumerate(data):
            side_ids = piece.split(' ')
            side_ids = [ int(x) for x in side_ids ]
            values = [idx+1, *side_ids]
            parsed.append(values)

        return parsed

    def write_solutions(self, valid_solutions, filename):
        # write solutions using piece IDs only (no edge values)

        # Example Solution
        # 5 7 15 11
        # 9 16 4 3
        # 13 1 8 10
        # 14 2 6 12

        with open(filename, 'w') as output_file:
            # The solutions are written using the piece numbers, separated by spaces, and one line per row.
            for solution in valid_solutions:
                # output_file.write("Solution: \n")
                print("\nSolution:\n")
                for row in solution:
                    # row_data = " ".join(map(str, row))
                    row_data = " ".join(str(item[0]) for item in row)
                    print(row_data)
                    output_file.write(row_data + "\n")
                # blank line between solutions
                output_file.write("\n")

        print("\nYou will find the answer in %s" % (filename))
