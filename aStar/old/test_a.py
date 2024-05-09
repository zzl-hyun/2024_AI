import heapq  # 우선순위 큐
import argparse
import random
import pygame
from pygame.locals import *
from pgu import gui
import sys
import math
from queue import PriorityQueue
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
OPEN = (152, 250, 152)
VISIT = (175, 238, 238)



def liveDrawVisit(screen, start, end, visit):
    # Draw visited cells
    for row, col in visit:
        color = VISIT
        pygame.draw.rect(screen, color, (col * CELL_SIZE + 1, row * CELL_SIZE + 1, CELL_SIZE - 2, CELL_SIZE - 2))
        if (row, col) == start:  # Check if it's the start cell
            font = pygame.font.Font(None, 18)
            text = font.render("S", True, BLACK)  # White "S" for start cell
            text_rect = text.get_rect(center=((col + 0.5) * CELL_SIZE, (row + 0.5) * CELL_SIZE))
            screen.blit(text, text_rect)
    # Apply changes to the screen
    pygame.display.flip()

    # Limit to 60 frames per second
    #pygame.time.Clock().tick(60)

def liveDrawOpen(screen, maze, start, end, visit):
    # Draw visited cells
    for node in visit:
        row, col = node.position
        color = OPEN
        pygame.draw.rect(screen, color, (col * CELL_SIZE + 1, row * CELL_SIZE + 1, CELL_SIZE - 2, CELL_SIZE - 2))
        if (row, col) == start:  # Check if it's the start cell
            font = pygame.font.Font(None, 18)
            text = font.render("S", True, BLACK)  # White "S" for start cell
            text_rect = text.get_rect(center=((col + 0.5) * CELL_SIZE, (row + 0.5) * CELL_SIZE))
            screen.blit(text, text_rect)
    # Apply changes to the screen
    pygame.display.flip()
    pygame.time.Clock().tick(60)


class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        # Tie breaking: smaller g values are preferred when f values are the same
        if self.f == other.f:
            return self.h < other.h
        return self.f < other.f


def Manhattan(node, goal, D =1):  # 대각선 이동이 없는 경우의 휴리스틱 함수
    dx = abs(node.position[0] - goal.position[0])
    dy = abs(node.position[1] - goal.position[1])
    return D * (dx + dy)

def Euclidean(node, goal, D= 1):  # 대각선 이동이 없는 경우의 휴리스틱 함수
    dx = abs(node.position[0] - goal.position[0])
    dy = abs(node.position[1] - goal.position[1])
    return D * (dx * dx + dy * dy) ** 0.5
            
def aStar(maze, start, end, heuristic, screen):
    # startNode와 endNode 초기화
    startNode = Node(None, start)
    endNode = Node(None, end)

    # openList, closedList 초기화
    openList = []
    closedSet = set()

    explored = 0
    min_f_node = Node(startNode, start)
    min_f_node.f = 99999999999

    heapq.heappush(openList, startNode)

    while openList:
        # 현재 노드 지정
        currentNode = heapq.heappop(openList)
        closedSet.add(currentNode.position)
        liveDrawVisit(screen, start, end, closedSet)

        # 현재 노드가 목적지면 current.position 추가하고
        # current의 부모로 이동
        if currentNode == endNode:
            path = []
            while currentNode is not None:
                path.append(currentNode.position)
                currentNode = currentNode.parent
            return path[::-1], closedSet

        # 인접한 xy좌표 전부, DFS
        for newPosition in (0, -1), (0, 1), (-1, 0), (1, 0) :#, (-1, -1), (-1, 1), (1, -1), (1, 1):
            # 노드 위치 업데이트
            nodePosition = (currentNode.position[0] + newPosition[0], currentNode.position[1] + newPosition[1])

             # 미로 maze index 범위 안에 있어야함
            if nodePosition[0] > len(maze) - 1 or nodePosition[0] < 0 or nodePosition[1] > len(maze[0]) - 1 or nodePosition[1] < 0:
                continue

            # 장애물이 있으면 다른 위치 불러오기
            if maze[nodePosition[0]][nodePosition[1]] != 0:
                continue

            new_node = Node(currentNode, nodePosition)
            # 자식이 closedList에 있으면 continue
            if new_node.position in closedSet:
                continue
            
            # f, g, h값 업데이트
            new_node.g = currentNode.g + 1

            if heuristic == 1 or heuristic == None:
                new_node.h = Manhattan(new_node, endNode)
            else:
                new_node.h = Euclidean(new_node, endNode)

            new_node.f = new_node.g + new_node.h
            print(new_node.position, new_node.g, new_node.h, new_node.f)

            # 자식이 openList에 있으고, g값이 더 크면 continue
            if any(child for child in openList if new_node.position == child.position and new_node.g > child.g):
                continue

            heapq.heappush(openList, new_node)
            liveDrawOpen(screen, maze, start, end, openList)
            explored += 1
            
            #print(exploredList)
            if new_node.f <= min_f_node.f :
                min_f_node = new_node
                #print("min 갱신" + str(min_f_node.position))
                

    print("경로를 찾을 수 없습니다.")

    # 방문한 노드 중에서 f(n) 값이 가장 낮은 노드를 찾습니다.
    # f(n) 값이 가장 낮은 노드부터 시작점까지의 경로를 출력합니다.
    path = []
    current_node = min_f_node
    while current_node != startNode:
        path.append(current_node.position)
        current_node = current_node.parent

    path.append(current_node.position)
    print(path)
    return path, closedSet

def initPoint(m, n) :
    start = (0, 0)
    end = (m - 1, n - 1)
    #start = (random.randint(0, m - 1), random.randint(0, n - 1))
    #end = (random.randint(0, m - 1), random.randint(0, n - 1))
    path = [None]
    visit = [None]
    print(f"Start: {start}")
    print(f"End: {end}")
    return start, end, path, visit

def generate_maze(m, n, start, end, inc_obstacle_ratio):
    # 먼저 모든 셀을 비어있는 상태로 초기화합니다.
    maze = [[0 for _ in range(n)] for _ in range(m)]

    # 장애물의 총 수를 계산합니다.
    num_obstacles = int(m * n * inc_obstacle_ratio)
    print(num_obstacles)
    # 장애물을 랜덤하게 배치합니다.
    for _ in range(num_obstacles):
        while True:
            row = random.randint(0, m - 1)
            col = random.randint(0, n - 1)

            # 시작점과 종료점은 장애물로 설정하지 않습니다.
            if (row, col) != start and (row, col) != end and maze[row][col] == 0:
                maze[row][col] = 1

                break

    return maze

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


def main(m, n, r):

    # Create the window
    WIDTH = n * CELL_SIZE + 150 # Adjusted width to fit the button
    HEIGHT = m * CELL_SIZE + 120

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Visualization")

    start, end, path, visit = initPoint(m, n)

    # Generate the maze
    maze = generate_maze(m, n, start, end, r)

    for row in maze:
        print(' '.join(map(str, row)))
    print(f"Start: {start}")
    print(f"End: {end}")
    print(path)

    # Create the start button
    start_button = pygame.Rect(10, (m * CELL_SIZE) + 10, 200, 100)

    # reset
    reset_button = pygame.Rect(start_button.right + 10 , start_button.top, 200, 100)

    # 라디오 버튼 그룹 생성

    # PGU 앱과 컨테이너 생성
    app = gui.App()
    container = gui.Container(width=WIDTH, height=HEIGHT)
    # 이벤트 처리 함수

    radioButtons = gui.Group(value=1)
    
    # 휴리스틱 옵션을 위한 라디오 버튼 추가
    manhattan_btn = gui.Radio(radioButtons, value=1)
    manhattann_label = gui.Label('Manhattan')  # 라디오 버튼에 대한 레이블 생성

    euclidean_btn = gui.Radio(radioButtons, value=2)
    euclidean_label = gui.Label('Euclidean')  # 라디오 버튼에 대한 레이블 생성

    # 라디오 버튼 이벤트 핸들러 등록
    #radioButtons.connect(gui.CLICK, handle_radio_change)

    # 라디오 버튼을 컨테이너에 추가
    container.add(manhattan_btn, WIDTH - 140, 100)
    container.add(manhattann_label, WIDTH - 120, 100)

    container.add(euclidean_btn, WIDTH - 140, 150)
    container.add(euclidean_label, WIDTH - 120, 150)
    # 앱에 컨테이너 연결
    
    app.init(container)


    # drag
    dragging = False
    selected_cell = None
    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                app.event(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 좌클릭
                        mouse_pos = pygame.mouse.get_pos()

                        cell_col = mouse_pos[0] // CELL_SIZE
                        cell_row = mouse_pos[1] // CELL_SIZE
                        print(cell_col , "," , cell_row)

                        if cell_row < 0 or cell_row >= len(maze) or cell_col < 0 or cell_col >= len(maze[0]):
                            pass
                        elif (cell_row,cell_col) == start or (cell_row,cell_col) == end:
                            dragging = True
                            selected_cell = (cell_row, cell_col)
                        elif maze[cell_row][cell_col] == 0:  # 벽이 아닌 경우에만 벽으로 설정
                            maze[cell_row][cell_col] = 1
                        elif maze[cell_row][cell_col] == 1:  # 길이 아닌 경우에만 길로 설정
                            maze[cell_row][cell_col] = 0

                        if manhattan_btn.collidepoint(mouse_pos):
                            print("set Manhattan", radioButtons.value)
                        if euclidean_btn.collidepoint(mouse_pos):
                            print("set Euclidean", radioButtons.value)


                        if start_button.collidepoint(mouse_pos):
                            if radioButtons.value is None:
                                print("Set Defalt")
                                radioButtons.value = 1

                            path, visit = aStar(maze, start, end, radioButtons.value, screen)  # m x n 미로 생성

                        if reset_button.collidepoint(mouse_pos):
                            start, end, path, visit = initPoint(m, n)
                            app.init(container)
                            maze = generate_maze(m, n, start, end, r)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        # 마우스 왼쪽 버튼을 놓으면 드래그 종료
                        dragging = False
                        if selected_cell:
                            if selected_cell == start:
                                start = (cell_y, cell_x)
                            elif selected_cell == end:
                                end = (cell_y, cell_x)
                        selected_cell = None
                elif event.type == pygame.MOUSEMOTION:
                    # 마우스를 이동하면 선택된 셀을 이동
                    if dragging and selected_cell:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        cell_x = mouse_x // CELL_SIZE
                        cell_y = mouse_y // CELL_SIZE
                        if cell_row < 0 or cell_row >= len(maze) or cell_col < 0 or cell_col >= len(maze[0]):
                            pass
                        if maze[cell_y][cell_x] == 0:
                           maze[selected_cell[0]][selected_cell[1]] = 0  # 이전 위치를 비움
                           maze[cell_y][cell_x] = 0  # 새 위치에 셀 배치
                           if selected_cell == start:  # 시작점을 이동
                               start = (cell_y, cell_x)
                           elif selected_cell == end:  # 종료점을 이동
                               end = (cell_y, cell_x)
                           selected_cell = (cell_y, cell_x)


        # 화면 업데이트
        
        screen.fill(WHITE)
                # 앱 그리기

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
        
    
        app.paint(screen)
        screen.blit(text, text_rect)



        pygame.display.flip()

    # pygame 종료
    pygame.quit()
    sys.exit()


 


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Set up a maze of size m x n.')
    parser.add_argument('--m', type=int, default=30, help='Number of rows in the grid')
    parser.add_argument('--n', type=int, default=30, help='Number of columns in the grid')
    parser.add_argument('--r', type=float, default=0.2, help='Set inc obstacle ratio')
    args = parser.parse_args()
    main(args.m, args.n, args.r)
