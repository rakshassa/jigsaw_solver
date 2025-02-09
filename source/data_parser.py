from sorter import Sorter
from file_handler import FileHandler

class DataParser:
    def __init__(self, verbose):
        self.verbose = verbose
        self.files = FileHandler()

        self.columns = None
        self.rows = None

        self.corners = None
        self.sides = None
        self.middles = None

    def parse_input(self, filename):
        """
        Reads and parses the input file to extract puzzle dimensions and pieces.
        """
        columns, rows, unsorted_pieces = self.files.read_file(filename)
        if self.verbose:
            print("====Data so far====")
            print(columns, rows, unsorted_pieces)

        self.columns = columns
        self.rows = rows
        self.sort_pieces(unsorted_pieces)

    def sort_pieces(self, unsorted_pieces):
        """
        Sorts the puzzle pieces into corners, sides, and middle pieces.
        """
        corners, sides, middles = Sorter().sort_pieces(unsorted_pieces)
        if self.verbose:
            print("====Sorted Pieces====")
            print(corners, sides, middles)

        self.corners = corners
        self.sides = sides
        self.middles = middles
