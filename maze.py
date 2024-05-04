import pygame
import sys
import random
import argparse
import astar
from astar import exploredList

# Initialize pygame
pygame.init()

# Constants
CELL_SIZE = 30  # Size of each cell in the maze
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (169, 169, 169)  # Grey color for walls
BLUE = (0, 0, 255)
WALL = (157, 195, 230)
BUTTON = (47, 85, 151)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
VISIT = (152, 250, 152)


def generate_maze(m, n, start, end):
    maze = [[1 if random.random() < 0.3 else 0 for _ in range(n)] for _ in range(m)]
    maze[start[0]][start[1]] = 0  
    maze[end[0]][end[1]] = 0
    return maze

def start_function(maze, start, end):
    # maze = [[random.randint(0, 1) for _ in range(m)] for _ in range(n)]

    path = astar.main(maze, start, end, 1)
    return path

def draw_maze(screen, maze, start, end, path, visit):

    for row in range(len(maze)):
        for col in range(len(maze[0])):
            # Draw cell border
            pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

            # Draw cell content
            
            if maze[row][col] == 1:
                color = WALL  # Wall color
            elif (row, col) in visit:
                color = VISIT
            else:
                color = WHITE  # Path color
                
            pygame.draw.rect(screen, color, (col * CELL_SIZE + 1, row * CELL_SIZE + 1, CELL_SIZE - 2, CELL_SIZE - 2))
            
            if (row, col) == start:  # Check if it's the start cell
                    font = pygame.font.Font(None, 18)
                    text = font.render("S", True, BLACK)  # White "S" for start cell
                    text_rect = text.get_rect(center=((col + 0.5) * CELL_SIZE, (row + 0.5) * CELL_SIZE))
                    screen.blit(text, text_rect)

            if (row, col) == end:  # Check if it's the start cell
                font = pygame.font.Font(None, 18)
                text = font.render("G", True, BLACK)  # White "G" for end cell
                text_rect = text.get_rect(center=((col + 0.5) * CELL_SIZE, (row + 0.5) * CELL_SIZE))
                screen.blit(text, text_rect)

            if len(path) >= 2:  # Make sure there are at least two points to draw a line
                pygame.draw.lines(screen, YELLOW, False, [(p[1] * CELL_SIZE + CELL_SIZE/2, p[0] * CELL_SIZE + CELL_SIZE/2) for p in path], 5)


def initPoint(m, n) :
    #start = (1, 1)
    #end = (m - 1, n - 1)
    start = (random.randint(0, n - 1), random.randint(0, m - 1))
    end = (random.randint(0, n - 1), random.randint(0, m - 1))
    path = [None]
    print(f"Start: {start}")
    print(f"End: {end}")
    visit = [None]
    return start, end, path, visit

def main(m, n):
    # Create the window
    WIDTH = n * CELL_SIZE  # Adjusted width to fit the button
    HEIGHT = m * CELL_SIZE + 120
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Visualization")

    start, end, path, visit = initPoint(m, n)

    # Generate the maze
    maze = generate_maze(m, n, start, end)

    # Create the start button
    start_button = pygame.Rect(10, (m * CELL_SIZE) + 10, 200, 100)

    # reset
    reset_button = pygame.Rect(start_button.right + 10 , start_button.top, 200, 100)

    #heuristic
    ratio_button = pygame.ratio

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 좌클릭
                    mouse_pos = pygame.mouse.get_pos()
                    
                    cell_col = mouse_pos[0] // CELL_SIZE
                    cell_row = mouse_pos[1] // CELL_SIZE
                    print(cell_col , "," , cell_row)
                    if start_button.collidepoint(mouse_pos):
                        path = start_function(maze, start, end)  # m x n 미로 생성
                        visit = exploredList

                    elif reset_button.collidepoint(mouse_pos):
                        start, end, path, visit = initPoint(m, n)
                        maze = generate_maze(m, n, start, end)

                    elif maze[cell_row][cell_col] == 0:  # 벽이 아닌 경우에만 벽으로 설정
                        maze[cell_row][cell_col] = 1
                    elif maze[cell_row][cell_col] == 1:  # 벽이 아닌 경우에만 벽으로 설정
                        maze[cell_row][cell_col] = 0
                        

        # 화면 업데이트
        
        screen.fill(WHITE)
        draw_maze(screen, maze, start, end, path, visit)  # 미로 그리기

        pygame.draw.rect(screen, BUTTON, start_button)  # 시작 버튼 그리기
        pygame.draw.rect(screen, BUTTON, reset_button)  # 시작 버튼 그리기

        # 시작 버튼에 텍스트 추가
        font = pygame.font.Font(None, 36)
        text = font.render("Start A* Search", True, WHITE)  # 흰색 텍스트 생성
        text_rect = text.get_rect(center=start_button.center)
        screen.blit(text, text_rect)

        text = font.render("Reset", True, WHITE)  # 초기화 버튼 텍스트 생성
        text_rect = text.get_rect(center=reset_button.center)
        screen.blit(text, text_rect)

        pygame.display.flip()

    # pygame 종료
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Set up a maze of size m x n.')
    parser.add_argument('--m', type=int, default=30, help='Number of rows in the grid')
    parser.add_argument('--n', type=int, default=30, help='Number of columns in the grid')
    args = parser.parse_args()
    main(args.m, args.n)
