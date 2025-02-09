"""
Handles file operations related to reading and writing puzzle data.
"""

class FileHandler:
    """
    A class responsible for handling file operations related to reading and writing puzzle data.
    """

    def read_file(self, filename):
        """
        Reads the puzzle file and extracts the puzzle size and pieces.

        :param filename: Path to the input file.
        :return: Tuple containing number of columns, number of rows, and a list of pieces.
        """
        lines = None

        with open(filename, 'r', encoding="utf-8") as input_file:
            lines = input_file.readlines()

        columns, rows = self.parse_puzzle_size(lines[0])
        pieces = self.parse_pieces(lines[1:])

        return columns, rows, pieces

    def parse_puzzle_size(self, data):
        """
        Parses the puzzle size from the input data.

        :param data: A string containing the puzzle size.
        :return: Tuple of integers representing the number of columns and rows.
        """
        values = data.split(' ')
        return int(values[0]), int(values[1])

    def parse_pieces(self, data):
        """
        Parses the puzzle pieces from the input data.

        :param data: List of strings representing puzzle pieces.
        :return: List of parsed puzzle pieces with unique IDs and side values.
        """
        parsed = []
        for idx, piece in enumerate(data):
            side_ids = piece.split(' ')
            side_ids = [int(x) for x in side_ids]
            values = [idx+1, *side_ids]
            parsed.append(values)

        return parsed

    def write_solutions(self, valid_solutions, filename):
        """
        Writes the valid puzzle solutions to an output file.

        :param valid_solutions: List of valid puzzle solutions.
        :param filename: Path to the output file.
        """
        with open(filename, 'w', encoding="utf-8") as output_file:
            # The solutions are written using the piece numbers
            # separated by spaces, and one line per row.
            for solution in valid_solutions:
                print("\nSolution:\n")
                for row in solution:
                    row_data = " ".join(str(item[0]) for item in row)
                    print(row_data)
                    output_file.write(row_data + "\n")
                # Blank line between solutions
                output_file.write("\n")

        print(f"\nYou will find the answer in {filename}")
