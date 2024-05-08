import heapq
import math

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = None
        self.opened = False
        self.closed = False

class AStarFinder:
    def __init__(self, heuristic='manhattan', weight=1):
        self.heuristic = heuristic
        self.weight = weight

    def find_path(self, start_x, start_y, end_x, end_y, grid):
        open_list = []
        start_node = grid.get_node_at(start_x, start_y)
        end_node = grid.get_node_at(end_x, end_y)

        start_node.g = 0
        start_node.f = 0

        heapq.heappush(open_list, (start_node.f, start_node))
        start_node.opened = True

        while open_list:
            node = heapq.heappop(open_list)[1]
            node.closed = True

            if node == end_node:
                return self.backtrace(end_node)

            neighbors = grid.get_neighbors(node)
            for neighbor in neighbors:
                if neighbor.closed:
                    continue

                x = neighbor.x
                y = neighbor.y

                ng = node.g + 1  # 대각선 이동을 허용하지 않으므로 거리는 항상 1입니다.

                if not neighbor.opened or ng < neighbor.g:
                    neighbor.g = ng
                    neighbor.h = neighbor.h or self.weight * self.heuristic(abs(x - end_x), abs(y - end_y))
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.parent = node

                    if not neighbor.opened:
                        heapq.heappush(open_list, (neighbor.f, neighbor))
                        neighbor.opened = True
                    else:
                        open_list.remove((neighbor.f, neighbor))
                        heapq.heappush(open_list, (neighbor.f, neighbor))

        return []

    def backtrace(self, node):
        path = [(node.x, node.y)]
        while node.parent is not None:
            node = node.parent
            path.append((node.x, node.y))
        return path[::-1]
