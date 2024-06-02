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
def liveDrawVisit(screen, start, visit):
    
    for row, col in visit:
        color = VISIT
        pygame.draw.rect(screen, color, (col * CELL + 1, row * CELL + 1, CELL - 2, CELL - 2))
        if (row, col) == start:  
            font = pygame.font.Font(None, 18)
            text = font.render("S", True, BLACK) 
            textRect = text.get_rect(center=((col + 0.5) * CELL, (row + 0.5) * CELL))
            screen.blit(text, textRect)

def liveDrawOpen(screen, start, visit):
    for row, col in visit:
        color = OPEN
        pygame.draw.rect(screen, color, (col * CELL + 1, row * CELL + 1, CELL - 2, CELL - 2))
        if (row, col) == start:  
            font = pygame.font.Font(None, 18)
            text = font.render("S", True, BLACK) 
            textRect = text.get_rect(center=((col + 0.5) * CELL, (row + 0.5) * CELL))
            screen.blit(text, textRect)
   
    pygame.display.flip()

class Node:
    def __init__(self, parent=None, pos=None):
        self.parent = parent
        self.pos = pos
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.pos == other.pos

    def __lt__(self, other):
        # tie breaking 적용
        if self.f == other.f:
            return self.h < other.h
        return self.f < other.f

def Manhattan(node, goal):  # 맨해튼 거리
    dx = abs(node.pos[0] - goal.pos[0])
    dy = abs(node.pos[1] - goal.pos[1])
    return (dx + dy)

def Euclidean(node, goal):  # 유클리드 거리
    dx = abs(node.pos[0] - goal.pos[0])
    dy = abs(node.pos[1] - goal.pos[1])
    return (dx * dx + dy * dy) ** 0.5

def aStar(grid, start, end, heuristic, screen):
    # 초기화
    M = len(grid) - 1 
    N = len(grid[0]) - 1 
    move = [(0, 1), (0, -1), (1, 0), (-1, 0)] 
    #move = [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, 1), (-1, -1), (1, 1), (1, -1)]
    startNode = Node(None, start)
    endNode = Node(None, end)
    openList = PriorityQueue()
    openSet = set()
    closeSet = set()
    minFnode = Node(startNode, start)
    minFnode.f = 99999999999
    explored = 0

    openList.put((startNode.f, startNode))
    openSet.add(startNode.pos)

    while not openList.empty():
        # 현재 노드 지정
        curNode = openList.get()[1]
        openSet.remove(curNode.pos)
        closeSet.add(curNode.pos)
        liveDrawVisit(screen, start, closeSet)
        explored += 1
        # 목적지를 찾으면 경로 반환
        if curNode == endNode:
            path = []
            print("search!!")
            while curNode is not None:
                path.append(curNode.pos)
                curNode = curNode.parent
            print("total explored nodes: ", explored)
            return path, closeSet

        # 대각선 비허용
        for newPos in move:
            curPos = (curNode.pos[0] + newPos[0], curNode.pos[1] + newPos[1])
             #grid 범위 만족
            if curPos[0] > M or curPos[0] < 0 or curPos[1] > N or curPos[1] < 0:
                continue
            # 장애물이면 넘어가기
            if grid[curPos[0]][curPos[1]] != 0:
                continue
            newNode = Node(curNode, curPos)
            # 이미 방문한 노드면 넘어가기
            if newNode.pos in closeSet:
                continue
            # f, g, h값 업데이트
            if heuristic == 1 or heuristic == None:
                newNode.h = Manhattan(newNode, endNode)
                newNode.g = curNode.g + 1
            else:
                newNode.h = Euclidean(newNode, endNode)
                #정수 g가 f에 영향을 많이 끼쳐서 줄임
                newNode.g = curNode.g + 0.625
            newNode.f = newNode.g + newNode.h
           
            if newNode.pos in openSet:
                for node in openList.queue:
                    if node[1] == newNode and node[1].g > newNode.g:
                        node[1].g = newNode.g
                        node[1].f = newNode.f
                        node[1].parent = newNode.parent
                        break
            else:
                openList.put((newNode.f, newNode))
                openSet.add(newNode.pos)
                #print(newNode.pos, newNode.g, newNode.h, newNode.f)
                liveDrawOpen(screen, start, openSet)

        if curNode.f != 0 and curNode.f <= minFnode.f and curNode.g >= minFnode.g:
            minFnode = curNode
            #print("min 갱신" ,minFnode.pos, minFnode.f)
            
    # f(n) 값이 가장 낮은 노드부터 시작점까지의 경로 출력
    print("경로를 찾을 수 없습니다.")
    path = []
    curNode = minFnode
    while curNode != startNode:
        path.append(curNode.pos)
        curNode = curNode.parent

    path.append(curNode.pos)
    #print(path)
    print("total explored nodes: ", explored)
    return path, closeSet

def initPoint(m, n) :
    # 고정
    #start = (0, 0)
    #end = (m - 1, n - 1)
    # 랜덤 생성
    start = (random.randint(0, m - 1), random.randint(0, n - 1))
    end = (random.randint(0, m - 1), random.randint(0, n - 1))
    path = [None]
    visit = [None]
    print("Start:", start)
    print("End: ", end)
    return start, end, path, visit

def generateGrid(m, n, start, end, inc_obstacle_ratio):
    # 모든 셀을 0으로 초기화
    grid = [[0 for _ in range(n)] for _ in range(m)]

    # ratio에 맞게 장애물 계산
    obstaclesNum = int(m * n * inc_obstacle_ratio)
    #print(obstaclesNum)

    # 장애물 랜덤 배치
    for _ in range(obstaclesNum):
        while True:
            row = random.randint(0, m - 1)
            col = random.randint(0, n - 1)

            # 시작점과 종료점은 장애물 예외
            if (row, col) != start and (row, col) != end and grid[row][col] == 0:
                grid[row][col] = 1
                break
    return grid

def drawGrid(screen, grid, start, end, path, visit):

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            # 격자
            pygame.draw.rect(screen, BLACK, (col * CELL, row * CELL, CELL, CELL), 1)
            # 벽            
            if grid[row][col] == 1:
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
                    textRect = text.get_rect(center=((col + 0.5) * CELL, (row + 0.5) * CELL))
                    screen.blit(text, textRect)

            if (row, col) == end:  
                font = pygame.font.Font(None, 18)
                text = font.render("G", True, BLACK)  
                textRect = text.get_rect(center=((col + 0.5) * CELL, (row + 0.5) * CELL))
                screen.blit(text, textRect)
            
            # 경로 생성
            # 좌표가 최소 2개 있을 때
            if len(path) >= 2:  
                pygame.draw.lines(screen, YELLOW, False, [(pos[1] * CELL + CELL/2, pos[0] * CELL + CELL/2) for pos in path], 5)

def initDraw(screen, grid, start, end):

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            # 격자 생성
            pygame.draw.rect(screen, BLACK, (col * CELL, row * CELL, CELL, CELL), 1)

            # 벽 색
            if grid[row][col] == 1:
                color = WALL
            # 길 색  
            else:
                color = WHITE  
            pygame.draw.rect(screen, color, (col * CELL + 1, row * CELL + 1, CELL - 2, CELL - 2))
            
            # 시작점
            if (row, col) == start:  
                    font = pygame.font.Font(None, 18)
                    text = font.render("S", True, BLACK)  
                    textRect = text.get_rect(center=((col + 0.5) * CELL, (row + 0.5) * CELL))
                    screen.blit(text, textRect)
            # 목적지
            if (row, col) == end:  
                font = pygame.font.Font(None, 18)
                text = font.render("G", True, BLACK)  
                textRect = text.get_rect(center=((col + 0.5) * CELL, (row + 0.5) * CELL))
                screen.blit(text, textRect)

def main(m, n, r):
    print(f"grid: {m} x {n} \nratio: {r}")
    WIDTH = n * CELL + 150 
    HEIGHT = m * CELL + 120
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("A* Simulater")

    # 초기화
    start, end, path, visit = initPoint(m, n)

    # 미로 생성
    grid = generateGrid(m, n, start, end, r)

    # 콘솔 출력
    '''
    for row in grid:
        print(' '.join(map(str, row)))
    '''

    # start
    startButton = pygame.Rect(25, (m * CELL) + 25, WIDTH/4, 75)
    # random walls
    randomButton = pygame.Rect(startButton.right + 25 , startButton.top, WIDTH/4, 75)
    # reset
    resetButton = pygame.Rect(randomButton.right + 25 , startButton.top, WIDTH/4, 75)

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
    focusCell = None
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
                        #print(f"{col} , {row})

                        # grid 범위 안에 있어야 함
                        if row < 0 or row >= m or col < 0 or col >= n:
                            pass
                        # 드래그
                        elif (row,col) == start or (row,col) == end:
                            dragging = True
                            focusCell = (row, col)
                        # 벽으로 설정
                        elif grid[row][col] == 0:  
                            grid[row][col] = 1
                        # 길로 설정
                        elif grid[row][col] == 1:  
                            grid[row][col] = 0

                        #start
                        if startButton.collidepoint(pos):
                            if radioButtons.value is None:
                                print("Set Defalt")
                                radioButtons.value = 1
                            print("\nStart\n")
                            path = [None]
                            visit = [None]
                            initDraw(screen, grid, start, end)
                            # A* 알고리즘 실행
                            path, visit = aStar(grid, start, end, radioButtons.value, screen)  
                        #random walls
                        if randomButton.collidepoint(pos):
                            start, end, path, visit = initPoint(m, n)
                            app.init(container)
                            grid = generateGrid(m, n, start, end, r)  
                        #reset
                        if resetButton.collidepoint(pos):
                            initDraw(screen, grid, start, end)
                            path = [None]
                            visit = [None]
                            screen.blit(text, textRect)
                            pygame.display.flip()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        # 마우스 왼쪽 버튼을 놓으면 드래그 종료
                        dragging = False
                        if focusCell:
                            if focusCell == start:
                                start = (row, col)
                            elif focusCell == end:
                                end = (row, col)
                        focusCell = None
                elif event.type == pygame.MOUSEMOTION:
                    # 마우스를 이동하면 선택된 셀을 이동
                    if dragging and focusCell:
                        pos = pygame.mouse.get_pos()
                        col = pos[0] // CELL
                        row = pos[1] // CELL
                        if row < 0 or row >= m or col < 0 or col >= n:
                            dragging = False
                            continue
                        if grid[row][col] == 0:
                           grid[focusCell[0]][focusCell[1]] = 0  # 이전 위치를 비움
                           grid[row][col] = 0  # 새 위치에 셀 배치 
                           if focusCell == start:  # 시작점을 이동
                               start = (row, col)
                           elif focusCell == end:  # 종료점을 이동
                               end = (row, col)
                           focusCell = (row, col)


        # 화면 업데이트
        screen.fill(WHITE)

        drawGrid(screen, grid, start, end, path, visit)  # 미로 그리기
        pygame.draw.rect(screen, BUTTON, startButton)  # 시작 버튼 그리기
        pygame.draw.rect(screen, BUTTON, randomButton)  # 시작 버튼 그리기
        pygame.draw.rect(screen, BUTTON, resetButton)  # 리셋 버튼 그리기

        #버튼에 텍스트 추가
        font = pygame.font.Font(None, int(WIDTH/23))
        text = font.render("Start A* Search", True, WHITE)  # 흰색 텍스트 생성
        textRect = text.get_rect(center=startButton.center)
        screen.blit(text, textRect)
        text = font.render("Random walls", True, WHITE)  # 흰색 텍스트 생성
        textRect = text.get_rect(center=randomButton.center)
        screen.blit(text, textRect)
        text = font.render("Reset", True, WHITE)  # 초기화 버튼 텍스트 생성
        textRect = text.get_rect(center=resetButton.center)
        app.paint(screen)
        screen.blit(text, textRect)
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
