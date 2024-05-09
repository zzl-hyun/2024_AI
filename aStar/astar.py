import argparse
import random
import pygame
from pygame.locals import *
from pgu import gui
import sys
from queue import PriorityQueue

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WALL = (169, 169, 169)
BUTTON = (47, 85, 151)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
OPEN = (152, 250, 152)
VISIT = (175, 238, 238)
CELL = 30  

# 방문노드 그리는 함수
def liveDrawVisit(screen, maze, start, end, visit):
    
    for row, col in visit:
        color = VISIT
        pygame.draw.rect(screen, color, (col * CELL + 1, row * CELL + 1, CELL - 2, CELL - 2))
        if (row, col) == start:  
            font = pygame.font.Font(None, 18)
            text = font.render("S", True, BLACK) 
            text_rect = text.get_rect(center=((col + 0.5) * CELL, (row + 0.5) * CELL))
            screen.blit(text, text_rect)

def liveDrawOpen(screen, maze, start, end, visit):
    for row, col in visit:
        color = OPEN
        pygame.draw.rect(screen, color, (col * CELL + 1, row * CELL + 1, CELL - 2, CELL - 2))
        if (row, col) == start:  
            font = pygame.font.Font(None, 18)
            text = font.render("S", True, BLACK) 
            text_rect = text.get_rect(center=((col + 0.5) * CELL, (row + 0.5) * CELL))
            screen.blit(text, text_rect)
   
    pygame.display.flip()

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
        # tie breaking 적용
        if self.f == other.f:
            return self.h < other.h
        return self.f < other.f

def Manhattan(node, goal):  # 맨해튼 거리
    dx = abs(node.position[0] - goal.position[0])
    dy = abs(node.position[1] - goal.position[1])
    return (dx + dy)

def Euclidean(node, goal):  # 유클리드 거리
    dx = abs(node.position[0] - goal.position[0])
    dy = abs(node.position[1] - goal.position[1])
    return (dx * dx + dy * dy) ** 0.5

def aStar(maze, start, end, heuristic, screen):
    # 초기화
    startNode = Node(None, start)
    endNode = Node(None, end)

    openList = PriorityQueue()
    openSet = set()
    closedSet = set()

    explored = 0
    min_f_node = Node(startNode, start)
    min_f_node.f = 99999999999

    openList.put((startNode.f, startNode))
    openSet.add(startNode.position)

    while not openList.empty():
        # 현재 노드 지정
        currentNode = openList.get()[1]
        openSet.remove(currentNode.position)
        closedSet.add(currentNode.position)
        liveDrawVisit(screen, maze, start, end, closedSet)

        # 현재 노드가 목적지면 current.position 추가하고
        # current의 부모로 이동
        if currentNode == endNode:
            path = []
            print("search!!")
            print("total explored nodes: ", explored)
            while currentNode is not None:
                path.append(currentNode.position)
                currentNode = currentNode.parent
            return path[::-1], closedSet

        # 인접한 xy좌표 전부, DFS
        for newPosition in [(0, -1), (0, 1), (-1, 0), (1, 0)] :#, (-1, -1), (-1, 1), (1, -1), (1, 1):
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
           

            if new_node.position in openSet:
                for node in openList.queue:
                    if node[1] == new_node and node[1].g > new_node.g:
                        node[1].g = new_node.g
                        node[1].f = new_node.f
                        node[1].parent = new_node.parent
                        break
            else:
                openList.put((new_node.f, new_node))
                openSet.add(new_node.position)
                #print(new_node.position, new_node.g, new_node.h, new_node.f)
                liveDrawOpen(screen, maze, start, end, openSet)

            if new_node.f <= min_f_node.f :
                min_f_node = new_node
                #print("min 갱신" + str(min_f_node.position))
            explored += 1

    # f(n) 값이 가장 낮은 노드부터 시작점까지의 경로 출력
    print("경로를 찾을 수 없습니다.")
    path = []
    current_node = min_f_node
    while current_node != startNode:
        path.append(current_node.position)
        current_node = current_node.parent

    path.append(current_node.position)
    #print(path)
    print("total explored nodes: ", explored)
    return path, closedSet

def initPoint(m, n) :
    # 디버깅
    #start = (1, 1)
    #end = (m - 1, n - 1)
    # 랜덤 생성
    start = (random.randint(0, m - 1), random.randint(0, n - 1))
    end = (random.randint(0, m - 1), random.randint(0, n - 1))
    path = [None]
    visit = [None]
    print(f"Start: {start}")
    print(f"End: {end}")
    return start, end, path, visit

def generateMaze(m, n, start, end, inc_obstacle_ratio):
    # 모든 셀을 0으로 초기화
    maze = [[0 for _ in range(n)] for _ in range(m)]

    # ratio에 맞게 장애물 계산
    num_obstacles = int(m * n * inc_obstacle_ratio)
    #print(num_obstacles)

    # 장애물 랜덤 배치
    for _ in range(num_obstacles):
        while True:
            row = random.randint(0, m - 1)
            col = random.randint(0, n - 1)

            # 시작점과 종료점은 장애물 예외
            if (row, col) != start and (row, col) != end and maze[row][col] == 0:
                maze[row][col] = 1
                break
    return maze

def draw_maze(screen, maze, start, end, path, visit):

    for row in range(len(maze)):
        for col in range(len(maze[0])):
            # 격자
            pygame.draw.rect(screen, BLACK, (col * CELL, row * CELL, CELL, CELL), 1)

            # 벽            
            if maze[row][col] == 1:
                color = WALL 
            # 시작점
            elif (row, col) == start:
                color = GREEN
            # 목적지
            elif (row, col) == end:
                color = RED
            # 방문노드
            elif (row, col) in visit:
               color = VISIT           
            # 길
            else:
                color = WHITE
                
            pygame.draw.rect(screen, color, (col * CELL + 1, row * CELL + 1, CELL - 2, CELL - 2))
            
            if (row, col) == start:  
                    font = pygame.font.Font(None, 18)
                    text = font.render("S", True, BLACK) 
                    text_rect = text.get_rect(center=((col + 0.5) * CELL, (row + 0.5) * CELL))
                    screen.blit(text, text_rect)

            if (row, col) == end:  
                font = pygame.font.Font(None, 18)
                text = font.render("G", True, BLACK)  
                text_rect = text.get_rect(center=((col + 0.5) * CELL, (row + 0.5) * CELL))
                screen.blit(text, text_rect)
            
            # 경로 생성
            # 좌표가 최소 2개 있을 때
            if len(path) >= 2:  
                pygame.draw.lines(screen, YELLOW, False, [(p[1] * CELL + CELL/2, p[0] * CELL + CELL/2) for p in path], 5)

def initDraw(screen, maze, start, end):

    for row in range(len(maze)):
        for col in range(len(maze[0])):
            # 격자 생성
            pygame.draw.rect(screen, BLACK, (col * CELL, row * CELL, CELL, CELL), 1)

            # 벽 색
            if maze[row][col] == 1:
                color = WALL
            # 길 색  
            else:
                color = WHITE  
            pygame.draw.rect(screen, color, (col * CELL + 1, row * CELL + 1, CELL - 2, CELL - 2))
            
            # 시작점
            if (row, col) == start:  
                    font = pygame.font.Font(None, 18)
                    text = font.render("S", True, BLACK)  
                    text_rect = text.get_rect(center=((col + 0.5) * CELL, (row + 0.5) * CELL))
                    screen.blit(text, text_rect)
            # 목적지
            if (row, col) == end:  
                font = pygame.font.Font(None, 18)
                text = font.render("G", True, BLACK)  
                text_rect = text.get_rect(center=((col + 0.5) * CELL, (row + 0.5) * CELL))
                screen.blit(text, text_rect)

def main(m, n, r):

    WIDTH = n * CELL + 150 
    HEIGHT = m * CELL + 120
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("A* Simulater")

    # 초기화
    start, end, path, visit = initPoint(m, n)

    # 미로 생성
    maze = generateMaze(m, n, start, end, r)

    # 콘솔 출력
    '''
    for row in maze:
        print(' '.join(map(str, row)))
    '''

    # start
    startButton = pygame.Rect(25, (m * CELL) + 25, 225, 75)
    # random walls
    randomButton = pygame.Rect(startButton.right + 25 , startButton.top, 225, 75)
    # reset
    resetButton = pygame.Rect(randomButton.right + 25 , startButton.top, 225, 75)


    # PGU 앱과 컨테이너
    app = gui.App()
    container = gui.Container(width=WIDTH, height=HEIGHT)

    # 라디오 버튼 그룹 
    radioButtons = gui.Group(value=1)
    
    # 라디오 버튼 
    radio1 = gui.Radio(radioButtons, value=1)
    label1 = gui.Label('Manhattan')  

    radio2 = gui.Radio(radioButtons, value=2)
    label2 = gui.Label('Euclidean') 

    # 라디오 버튼을 컨테이너에 추가
    container.add(radio1, WIDTH - 140, 100)
    container.add(label1, WIDTH - 120, 100)

    container.add(radio2, WIDTH - 140, 150)
    container.add(label2, WIDTH - 120, 150)
    # 앱에 컨테이너 연결
    app.init(container)

 
    dragging = False
    selectedCell = None
    

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                app.event(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 좌클릭
                        pos = pygame.mouse.get_pos()

                        col = pos[0] // CELL
                        row = pos[1] // CELL
                        # 클릭한 좌표
                        #print(col , "," , row)

                        # maze 범위 안에 있어야 함
                        if row < 0 or row >= len(maze) or col < 0 or col >= len(maze[0]):
                            pass
                        # 드래그
                        elif (row,col) == start or (row,col) == end:
                            dragging = True
                            selectedCell = (row, col)
                        # 벽으로 설정
                        elif maze[row][col] == 0:  
                            maze[row][col] = 1
                        # 길로 설정
                        elif maze[row][col] == 1:  
                            maze[row][col] = 0

                        #start
                        if startButton.collidepoint(pos):
                            if radioButtons.value is None:
                                print("Set Defalt")
                                radioButtons.value = 1
                            print("\nStart\n")
                            path = [None]
                            visit = [None]
                            initDraw(screen, maze, start, end)
                            # A* 알고리즘 실행
                            path, visit = aStar(maze, start, end, radioButtons.value, screen)  
                        #random walls
                        if randomButton.collidepoint(pos):
                            start, end, path, visit = initPoint(m, n)
                            app.init(container)
                            maze = generateMaze(m, n, start, end, r)  
                        #reset
                        if resetButton.collidepoint(pos):
                            initDraw(screen, maze, start, end)
                            path = [None]
                            visit = [None]
                            screen.blit(text, text_rect)
                            pygame.display.flip()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        # 마우스 왼쪽 버튼을 놓으면 드래그 종료
                        dragging = False
                        if selectedCell:
                            if selectedCell == start:
                                start = (row, col)
                            elif selectedCell == end:
                                end = (row, col)
                        selectedCell = None
                elif event.type == pygame.MOUSEMOTION:
                    # 마우스를 이동하면 선택된 셀을 이동
                    if dragging and selectedCell:
                        pos = pygame.mouse.get_pos()
                        col = pos[0] // CELL
                        row = pos[1] // CELL
                        if row < 0 or row >= len(maze) or col < 0 or col >= len(maze[0]):
                            dragging = False
                            continue
                        if maze[row][col] == 0:
                           maze[selectedCell[0]][selectedCell[1]] = 0  # 이전 위치를 비움
                           maze[row][col] = 0  # 새 위치에 셀 배치
                           if selectedCell == start:  # 시작점을 이동
                               start = (row, col)
                           elif selectedCell == end:  # 종료점을 이동
                               end = (row, col)
                           selectedCell = (row, col)


        # 화면 업데이트
        screen.fill(WHITE)

        draw_maze(screen, maze, start, end, path, visit)  # 미로 그리기
        pygame.draw.rect(screen, BUTTON, startButton)  # 시작 버튼 그리기
        pygame.draw.rect(screen, BUTTON, randomButton)  # 시작 버튼 그리기
        pygame.draw.rect(screen, BUTTON, resetButton)  # 리셋 버튼 그리기

        #버튼에 텍스트 추가
        font = pygame.font.Font(None, 36)
        text = font.render("Start A* Search", True, WHITE)  # 흰색 텍스트 생성
        text_rect = text.get_rect(center=startButton.center)
        screen.blit(text, text_rect)
        text = font.render("Random walls", True, WHITE)  # 흰색 텍스트 생성
        text_rect = text.get_rect(center=randomButton.center)
        screen.blit(text, text_rect)
        text = font.render("Reset", True, WHITE)  # 초기화 버튼 텍스트 생성
        text_rect = text.get_rect(center=resetButton.center)
        app.paint(screen)
        screen.blit(text, text_rect)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='options: --m --n --r')
    parser.add_argument('--m', type=int, default=30, help='Set rows ')
    parser.add_argument('--n', type=int, default=30, help='Set columns')
    parser.add_argument('--r', type=float, default=0.2, help='Set inc obstacle ratio')
    args = parser.parse_args()
    main(args.m, args.n, args.r)
