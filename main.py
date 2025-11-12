import pygame
import time
from maze import Maze

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (160, 160, 160)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

CELL_SIZE = 40
FPS = 15

# Delay (segundos) entre cada passo do rato — aumente para ver os passos mais devagar
STEP_DELAY = 0.5


class MazeGame:
    def __init__(self, maze_data):
        pygame.init()
        self.maze = Maze(maze_data)
        self.width = self.maze.cols * CELL_SIZE
        self.height = self.maze.rows * CELL_SIZE
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("🐭 Trapped Mouse - Pygame Edition")
        self.clock = pygame.time.Clock()
        self.running = True
        self.found_exit = None

    def draw_maze(self):
        for i in range(self.maze.rows):
            for j in range(self.maze.cols):
                x = j * CELL_SIZE
                y = i * CELL_SIZE
                cell = self.maze.maze[i][j]

                # Determina a cor (sem operador ternário)
                if cell == '1':
                    color = BLACK
                elif cell == '0':
                    color = WHITE
                elif cell == 'm':
                    color = BLUE
                elif cell == 'e':
                    color = RED
                elif cell == '.':
                    color = GRAY
                else:
                    color = YELLOW

                pygame.draw.rect(self.screen, color, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(self.screen, (200, 200, 200), (x, y, CELL_SIZE, CELL_SIZE), 1)

    def update(self):
        self.draw_maze()
        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            if self.found_exit is None:
                result = self.maze.step()
                self.update()
                # Pausa para desacelerar a movimentação do rato
                time.sleep(STEP_DELAY)
                self.clock.tick(FPS)

                if result is not None:
                    self.found_exit = result
                    time.sleep(3)
            else:
                font = pygame.font.Font(None, 50)
                if self.found_exit:
                    text = font.render("🎉 O rato encontrou a saída!", True, (0, 180, 0))
                else:
                    text = font.render("💀 O rato ficou preso!", True, (200, 0, 0))
                self.screen.blit(text, (30, self.height // 2 - 20))
                pygame.display.flip()
                pygame.time.wait(3000)
                self.running = False


def carregar_labirinto_txt(caminho_arquivo):
    """Lê um arquivo .txt contendo o labirinto"""
    linhas = []
    with open(caminho_arquivo, "r") as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if linha != "":
                linhas.append(linha)
    return linhas


if __name__ == "__main__":
    caminho = "labirinto.txt"

    try:
        maze_data = carregar_labirinto_txt(caminho)
    except FileNotFoundError:
        print("Arquivo labirinto.txt não encontrado. Usando labirinto padrão.")
        maze_data = [
            "1111111",
            "1m00101",
            "1010011",
            "1000001",
            "11110e1",
            "1111111"
        ]

    game = MazeGame(maze_data)
    game.run()
    pygame.quit()
