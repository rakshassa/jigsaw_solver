import copy
from file_handler import FileHandler
from permutations import Permutations
from side_placer import SidePlacer
from middle_placer import MiddlePlacer
from sorter import Sorter


class JigsawSolver(object):
    def __init__(self, filename, outfile, verbose=False):
        self.verbose = verbose
        self.filename = filename
        self.output_filename = outfile

        self.valid_borders = []
        self.valid_solutions = []

        self.sorter = Sorter() # organizes the pieces
        self.files = FileHandler()

    def parse_input(self):
        columns, rows, unsorted_pieces = self.files.read_file(filename);
        if self.verbose: print("====Data so far====")
        if self.verbose: print(columns, rows, unsorted_pieces)

        self.columns = columns
        self.rows = rows
        self.unsorted_pieces = unsorted_pieces

    def sort_pieces(self):
        corners, sides, middles = self.sorter.sort_pieces(self.unsorted_pieces) # sort into size, corners, edges, middles
        if self.verbose: print("====Sorted Pieces====")
        if self.verbose: print(corners, sides, middles)

        self.corners = corners
        self.sides = sides
        self.middles = middles

    def run(self):
        self.parse_input()
        self.sort_pieces()

        self.permutations = Permutations(self.columns, self.rows, self.corners) # calculates the next valid permutation
        self.place_corners()

    def place_corners(self):
        while(True):
            corner_placements = self.permutations.next_corner()
            if corner_placements == None:
                print("No more corner/side combinations.")
                break

            self.place_sides(corner_placements)

        # OPTIMIZE: if the valid_borders takes up too much memory, we
        # could put this inline with a valid_border to avoid caching the full list of valid borders
        self.place_middles()

        # OPTIMIZE: if valid_solutions is taking up too much memory, we could stream to a file instead of caching results
        self.files.write_solutions(self.valid_solutions, self.output_filename)

    def place_sides(self, corner_placements):
        side_placer = SidePlacer(self.columns, self.rows, self.sides)
        results = side_placer.place_sides(corner_placements)
        # print("Valid Results for this corner placement: %i" % (len(results)))
        if len(results) > 0:
            self.valid_borders = [*self.valid_borders, *results]

    def place_middles(self):
        print("Total Valid Borders: %i" % (len(self.valid_borders)))
        for border in self.valid_borders:
            middle_placer = MiddlePlacer(self.columns, self.rows, self.middles)
            results = middle_placer.place_middles(border)
            self.valid_solutions = [*self.valid_solutions, *results]


if __name__ == "__main__":
    filename = "../data/example1.txt"
    outfile = "../data/output.txt"
    solver = JigsawSolver(filename, outfile, verbose=True)
    solver.run()
