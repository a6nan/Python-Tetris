import pygame
from colors import Colors

class Grid:
    def __init__(self):
        self.num_rows = 20
        self.num_cols = 10
        self.cell.size = 30
        self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]
        self.colors = Colors.get_cell_colors()

    def printGrid(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                print(self.grid[row][column], end=" ")
            print()

    def dalam(self, row, column):
        if 0 <= row < self.num_rows and 0 <= column < self.num_cols:
            return True
        return False

    def kosong(self, row, column):
        if self.grid[row][column] == 0:
            return True
        return False

    def tetris(self):


