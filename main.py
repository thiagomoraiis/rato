import pygame
import time
import argparse
from maze import Maze
from cell import Cell
import os

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (160, 160, 160)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
MOUSE_COLOR = (150, 75, 0)
GREEN = (0, 255, 0)


CELL_SIZE = 40
FPS = 15
STEP_DELAY = 0.7 

class MazeGame:
    def __init__(self, maze_data):
        pygame.init()
        self.maze = Maze(maze_data)
        self.width = self.maze.cols * CELL_SIZE
        self.height = self.maze.rows * CELL_SIZE
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Trapped Mouse")
        self.clock = pygame.time.Clock()
        self.running = True
        self.found_exit = None

    def draw_maze(self):
        for i in range(self.maze.rows):
            for j in range(self.maze.cols):
                x = j * CELL_SIZE
                y = i * CELL_SIZE
                cell = self.maze.maze[i][j]

                color_map = {
                    self.maze.wall: BLACK,
                    self.maze.passage: WHITE,
                    self.maze.entryMarker: MOUSE_COLOR,
                    self.maze.exitMarker: RED,
                    self.maze.visited: GRAY,
                    self.maze.backtracked: YELLOW,
                }

                color = color_map.get(cell, WHITE)

                pygame.draw.rect(self.screen, color, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(self.screen, (200, 200, 200), (x, y, CELL_SIZE, CELL_SIZE), 1)

        cur = self.maze.currentCell
        pygame.draw.circle(
            self.screen,
            MOUSE_COLOR,
            (cur.y * CELL_SIZE + CELL_SIZE // 2, cur.x * CELL_SIZE + CELL_SIZE // 2),
            CELL_SIZE // 3
        )
    
    def draw_best_path(self):
        print('Melhor caminho: ', self.maze.mazeStack.items)
        for cell in self.maze.mazeStack.items:
            x = cell.y * CELL_SIZE
            y = cell.x * CELL_SIZE
            pygame.draw.rect(self.screen, GREEN, (x, y, CELL_SIZE, CELL_SIZE))

        cur = self.maze.currentCell
        pygame.draw.circle(
            self.screen,
            MOUSE_COLOR,
            (cur.y * CELL_SIZE + CELL_SIZE // 2, cur.x * CELL_SIZE + CELL_SIZE // 2),
            CELL_SIZE // 3
        )

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
                time.sleep(STEP_DELAY)
                self.clock.tick(FPS)
                if result is not None:
                    self.found_exit = result
                    time.sleep(0.5)
            else:
                font = pygame.font.Font(None, 50)
                if self.found_exit:
                    text = font.render("🎉 O rato encontrou a saída!", True, (0, 180, 0))
                    self.draw_best_path()
                else:
                    text = font.render("O rato ficou preso!", True, (200, 0, 0))
                self.screen.blit(text, (30, self.height // 2 - 20))
                pygame.display.flip()
                pygame.time.wait(3000)
                self.running = False


def carregar_labirinto_txt(caminho_arquivo):
    linhas = []
    with open(caminho_arquivo, "r") as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if linha != "":
                linhas.append(linha)
    return linhas


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script para executar o jogo do labirinto em Pygame.')
    parser.add_argument('file', help='Nome do arquivo do labirinto')
    args = parser.parse_args()

    caminho = args.file
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
