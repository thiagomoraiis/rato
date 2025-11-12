from cell import Cell

class Maze:
    def __init__(self, maze_lines):
        self.maze = []
        for line in maze_lines:
            line = line.strip()
            if line != "":
                self.maze.append(list(line))

        self.rows = len(self.maze)
        self.cols = len(self.maze[0])
        self.stack = []

        self.entry = self.find_marker('m')
        self.exit = self.find_marker('e')
        self.current = self.entry

    def find_marker(self, marker):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.maze[i][j] == marker:
                    return Cell(i, j)
        return None

    def get_neighbors(self, cell):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # direita, esquerda, baixo, cima
        neighbors = []
        for dx, dy in directions:
            nx = cell.x + dx
            ny = cell.y + dy
            if nx >= 0 and nx < self.rows and ny >= 0 and ny < self.cols:
                valor = self.maze[nx][ny]
                if valor == '0' or valor == 'e':
                    neighbors.append(Cell(nx, ny))
        return neighbors

    def step(self):
        """Executa um passo do algoritmo de backtracking"""
        if self.current == self.exit:
            return True

        # Marca posição atual como visitada
        if self.maze[self.current.x][self.current.y] != 'm':
            self.maze[self.current.x][self.current.y] = '.'

        neighbors = self.get_neighbors(self.current)

        if len(neighbors) > 0:
            self.stack.append(self.current)
            self.current = neighbors[0]
        elif len(self.stack) > 0:
            self.current = self.stack.pop()
        else:
            return False
        return None
