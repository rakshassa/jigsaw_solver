"""
Main Class to solve jigsaw puzzles
"""

from file_handler import FileHandler
from permutations import Permutations
from side_placer import SidePlacer
from middle_placer import MiddlePlacer
from data_parser import DataParser


class JigsawSolver:
    """
    A class to solve a jigsaw puzzle by sorting and placing pieces.
    """

    def __init__(self, infile, outfile, verbose=False):
        """
        Initializes the JigsawSolver with file input and output paths.

        :param filename: Path to the input file containing puzzle pieces.
        :param outfile: Path to the output file to store solutions.
        :param verbose: Boolean flag for verbose output.
        """
        self.verbose = verbose
        self.filename = infile
        self.output_filename = outfile

        self.valid_borders = []
        self.valid_solutions = []

        self.files = FileHandler()
        self.data = DataParser(verbose)

    def place_corners(self, permutations):
        """
        Attempts to place the corner pieces and subsequently place the sides and middle pieces.

        :param permutations: An instance of the Permutations class to generate corner placements.
        """
        while True:
            corner_placements = permutations.next_corner()
            if corner_placements is None:
                print("No more corner/side combinations.")
                break

            self.place_sides(corner_placements)

        self.place_middles()

        # Write the final solutions to the output file
        self.files.write_solutions(self.valid_solutions, self.output_filename)

    def place_sides(self, corner_placements):
        """
        Places the side pieces based on the given corner placements.

        :param corner_placements: List of possible corner placements.
        """
        side_placer = SidePlacer(self.data.columns, self.data.rows, self.data.sides)
        results = side_placer.place_sides(corner_placements)
        if len(results) > 0:
            self.valid_borders = [*self.valid_borders, *results]

    def place_middles(self):
        """
        Places the middle pieces within valid border placements.
        """
        print(f"Total Valid Borders: {len(self.valid_borders)}")
        for border in self.valid_borders:
            middle_placer = MiddlePlacer(self.data.columns, self.data.rows, self.data.middles)
            results = middle_placer.place_middles(border)
            self.valid_solutions = [*self.valid_solutions, *results]

    def run(self):
        """
        Executes the jigsaw solving process by parsing input, sorting pieces, and placing them.
        """
        self.data.parse_input(self.filename)

        permutations = Permutations(self.data.columns, self.data.rows, self.data.corners)
        self.place_corners(permutations)


if __name__ == "__main__":
    FILENAME = "../data/example1.txt"
    OUTFILENAME = "../data/output.txt"
    solver = JigsawSolver(FILENAME, OUTFILENAME, verbose=True)
    solver.run()
