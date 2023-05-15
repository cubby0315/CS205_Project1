import heapq
import math
import time

goal = [[1,2,3],[4,5,6],[7,8,0]]
node_cnt = 0

def uniform_distance(node):
    distance = 0
    return distance

def manhattan_distance(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                row = (state[i][j] - 1) // 3
                col = (state[i][j] - 1) % 3
                distance += abs(i - row) + abs(j - col)
    return distance

def misplaced_distance(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                row = (state[i][j] - 1) // 3
                col = (state[i][j] - 1) % 3
                if i != row or j != col:
                    distance += 1
    return distance

class Node:
    def __init__(self, state, parent, g, h):
        self.state = state  
        self.parent = parent  
        self.g = g  
        self.h = h  

    def f(self):
        return self.g + self.h

    def __lt__(self, other):
        return self.f() < other.f()
    

def is_valid_move(i, j):
    return 0 <= i <= 2 and 0 <= j <= 2


def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def generate_next_states(nodes, current_node, num, que_size, node_cnt):
    next_states = nodes
    blank_i, blank_j = find_blank(current_node.state)
    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # 下、上、右、左

    for move in moves:
        next_i, next_j = blank_i + move[0], blank_j + move[1]
        if is_valid_move(next_i, next_j):
            # print(next_i, next_j)
            next_state = [row[:] for row in current_node.state]
            next_state[blank_i][blank_j], next_state[next_i][next_j] = next_state[next_i][next_j], next_state[blank_i][blank_j]
            if num == 1:
                next_node = Node(next_state, current_node, current_node.g + 1, manhattan_distance(next_state))
            if num == 2:
                next_node = Node(next_state, current_node, current_node.g + 1, misplaced_distance(next_state))
            if num == 3:
                next_node = Node(next_state, current_node, current_node.g + 1, 0)
            if check_equal(next_node.state,current_node.state) == False:    
                next_states.append(next_node)
                que_size += 1
                node_cnt += 1

    return next_states, que_size, node_cnt


def que_func(next_state):
    next_state.sort(key = lambda s: s.f())
    return next_state


def check_equal(state,state2):
    for i in range(3):
        for j in range(3):
            if state[i][j] != state2[i][j]:
                return False
    return True

def Astar(problem, num, que_size, node_cnt):
    max_que = 0
    nodes = []
    if num == 1: 
        nodes.append(Node(problem, None, 0, manhattan_distance(problem)))
    if num == 2:
        nodes.append(Node(problem, None, 0, misplaced_distance(problem)))
    if num == 3:
        nodes.append(Node(problem, None, 0, 0))
    que_size += 1
    node_cnt += 1
    max_que = max(que_size, max_que)
    while True:
        if len(nodes) == 0:
            return None,max_que, node_cnt
        node = nodes.pop(0)
        que_size -= 1
        # node_cnt -= 1
        if check_equal(node.state, goal):
            return node,max_que, node_cnt
        nodes, que_size, node_cnt = generate_next_states(nodes, node, num, que_size, node_cnt)
        if num != 3:
            nodes = que_func(nodes)
        max_que = max(que_size, max_que)


def main():
    number = input('choose different ways: 1 is Manhattan, 2 is Misplaced, 3 is Uniform: ')
    select = input('1 for default puzzle, 2 for creating a new one:')
    select = int(select)
    if select == 2:
        a,b,c,d,e,f,g,h,i = input('input initial state, split with ",":').split(",")
        start_state = [[int(a), int(b), int(c)],
                   [int(d), int(e), int(f)],
                   [int(g), int(h), int(i)]]
    else:
        start_state = [[0, 1, 6],
                    [5, 3, 7],
                    [4, 8, 2]]
        # start_state = [[7, 1, 2],
        #             [4, 8, 5],
        #             [6, 3, 0]]
    start = time.time()
    que_size = 0
    node_cnt = 0

    solution,que_size,node_cnt = Astar(start_state, int(number), que_size, node_cnt)
    # solution,que_size = Astar(start_state, int(number), que_size)
    end = time.time()
    if solution is None:
        print("No solution found.")
    else:
        print("Solution depth is:", solution.g)
        print("Number of nodes expanded:", node_cnt)
        print("Max que size is:", que_size)
        print('execution time:', end - start)
        

if __name__ == '__main__':
    main()
