import heapq  # 우선순위 큐
import argparse
import random
import time
closedSet = set()
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
        return self.f < other.f

def Manhattan(node, goal):  # 대각선 이동이 없는 경우의 휴리스틱 함수
    dx = abs(node.position[0] - goal.position[0])
    dy = abs(node.position[1] - goal.position[1])
    return (dx + dy)

def Euclidean(node, goal):  # 대각선 이동이 없는 경우의 휴리스틱 함수
    dx = abs(node.position[0] - goal.position[0])
    dy = abs(node.position[1] - goal.position[1])
    return (dx ** 2 + dy ** 2)



def aStar(maze, start, end, heuristic):
    # startNode와 endNode 초기화
    startNode = Node(None, start)
    endNode = Node(None, end)

    # openList, closedList 초기화
    openList = []

    explored = 0
    min_f_node = Node(startNode, start)
    min_f_node.f = 99999999999

    heapq.heappush(openList, startNode)

    while openList:
        # 현재 노드 지정
        currentNode = heapq.heappop(openList)
        closedSet.add(currentNode.position)

        # 현재 노드가 목적지면 current.position 추가하고
        # current의 부모로 이동
        if currentNode == endNode:
            path = []
            while currentNode is not None:
                path.append(currentNode.position)
                currentNode = currentNode.parent
            return path[::-1], explored

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


            # 자식이 openList에 있으고, g값이 더 크면 continue
            # new_node.g >= child.g 로 하면 openList 중복성을 줄일 수도 있습니다.
            # 하지만 이건 시나리오에 따라 다르고, 대부분 엄격히 더 낮은 g 값을 확인하면 충분할 수 있습니다.
            if any(child for child in openList if new_node == child and new_node.g > child.g):
                continue

            heapq.heappush(openList, new_node)
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
    return path, explored

def main(maze, start, end, heuristic):

    for row in maze:
        print(' '.join(map(str, row)))
    print(f"Start: {start}")
    print(f"End: {end}")
    if heuristic == 1 or heuristic == None:
        print("heuristic is Manhattan")
    else:
        print("heuristic is Euclidean")
    path, explored = aStar(maze, start, end, heuristic)
    print(path)
    print(explored)
    return path

if __name__ == '__main__':
    main()
