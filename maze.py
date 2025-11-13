from cell import Cell
from stack import Stack

class Maze:
    def __init__(self, maze_lines):
        self.exitMarker = 'e'
        self.entryMarker = 'm'
        self.visited = '.'
        self.backtracked = '*'
        self.passage = '0'
        self.wall = '1'

        self.initStack = Stack()
        for line in maze_lines:
            line = line.strip()
            if line != "":
                self.initStack.push(list(line))

        self.maze = []
        while not self.initStack.is_empty():
            self.maze.append(self.initStack.pop())
    
        self.maze.reverse()

        self.rows = len(self.maze)
        self.cols = len(self.maze[0])

        self.mazeStack = Stack()

        self.entryCell = self.find_marker(self.entryMarker)
        self.exitCell = self.find_marker(self.exitMarker)
        self.currentCell = self.entryCell

        self.backtracking = False

    def find_marker(self, marker):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.maze[i][j] == marker:
                    return Cell(i, j)
        return None

    def get_neighbors(self, cell):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        neighbors = []
        for direction_x, direction_y in directions:
            neighbor_x = cell.x + direction_x
            neighbor_y = cell.y + direction_y
            if neighbor_x >= 0 and neighbor_x < self.rows and neighbor_y >= 0 and neighbor_y < self.cols:
                valor = self.maze[neighbor_x][neighbor_y]
                if valor == self.passage or valor == self.exitMarker:
                    neighbors.append(Cell(neighbor_x, neighbor_y))
        return neighbors

    def step(self):
        if self.currentCell == self.exitCell:
            return True

        if self.maze[self.currentCell.x][self.currentCell.y] != self.entryMarker:
            if self.backtracking:
                self.maze[self.currentCell.x][self.currentCell.y] = self.backtracked
            else:
                self.maze[self.currentCell.x][self.currentCell.y] = self.visited

        neighbors = self.get_neighbors(self.currentCell)
        print(neighbors)

        if len(neighbors) > 0:
            self.mazeStack.push(self.currentCell)
            self.currentCell = neighbors[0]
            self.backtracking = False
        elif not self.mazeStack.is_empty():
            self.currentCell = self.mazeStack.pop()
            self.backtracking = True
        else:
            # Nenhum caminho, o rato está preso
            return False

        return None

    def exitMaze(self):
        while True:
            result = self.step()
            if result is not None:
                return result
