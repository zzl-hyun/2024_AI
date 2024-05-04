import pygame
import sys
import random
import argparse
import astar

# Initialize pygame
pygame.init()

# Constants
CELL_SIZE = 20  # Size of each cell in the maze
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def generate_maze(m, n):
    maze = [[1 if random.random() < 0.3 else 0 for _ in range(n)] for _ in range(m)]
    return maze

def start_function(maze, m, n):
    #astar.main(maze, m, n)
    for row in maze:
        print(' '.join(map(str, row)))

def draw_maze(screen, maze):
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            color = WHITE if maze[row][col] == 1 else BLACK
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def main(m, n):
    # Create the window
    WIDTH = n * CELL_SIZE
    HEIGHT = m * CELL_SIZE
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Visualization")

    # Generate the maze
    maze = generate_maze(m, n)

    # Create the start button
    start_button = pygame.Rect(300, 250, 200, 100)

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 좌클릭
                    mouse_pos = pygame.mouse.get_pos()
                    if start_button.collidepoint(mouse_pos):
                        start_function(maze, m, n)  # m x n 미로 생성

        # 화면 업데이트
        screen.fill(WHITE)
        draw_maze(screen, maze)  # 미로 그리기
        pygame.draw.rect(screen, BLACK, start_button)  # 시작 버튼 그리기
        pygame.display.flip()

    # pygame 종료
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Set up a maze of size m x n.')
    parser.add_argument('m', type=int, default=10, help='Number of rows in the grid')
    parser.add_argument('n', type=int, default=10, help='Number of columns in the grid')
    args = parser.parse_args()
    main(args.m, args.n)
