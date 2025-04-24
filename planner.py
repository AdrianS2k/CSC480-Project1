"""

Using the make_vacuum_world.py and random.txt file 
Usage:
    python3 planner.py unfiform-cost|depth-first textfile.txt

Example: 
    python3 planner.py uniform-cost random-5x7.txt

Parameters:
    - Search-Algorithm (string): the desired algorithm used for the world

"""

import sys
import heapq


def get_cardinal_neighbors(position):
    """Function to get the cardinal neighbors of a position on the grid"""
    return {
        'N': (position[0] - 1, position[1]), 
        'S': (position[0] + 1, position[1]),
        'W': (position[0], position[1] - 1),
        'E': (position[0], position[1] + 1), 
    }


def next_steps(position, dirty, blocked, rows, columns):
    """Getting the next steps excluding those that are blocked or out of bounds"""
    options = get_cardinal_neighbors(position)
    l = []
    for move, point in options.items():
        x, y = point
        if 0 <= x < rows and 0 <= y < columns:
            if point not in blocked:
                l.append((move, (point, frozenset(dirty))))
    if position in dirty:
        dirty2 = set(dirty)
        dirty2.remove(position)
        l.append(('V', (position, frozenset(dirty2))))

    
    return l


def depth_first_search(start_state, blocked, rows, columns):
    """Depth first search implementation"""
    stack = [(start_state, [])]
    nodes_generated = 0
    nodes_expanded = 0
    visited = set()

    while stack:
        curr, path = stack.pop()
        pos, dirty = curr

        if curr in visited:
            continue
        visited.add(curr)
        nodes_expanded += 1

        if len(dirty) == 0:
            return (path, nodes_generated, nodes_expanded)
        for move, next in next_steps(pos, dirty, blocked, rows, columns):
            if next not in visited:
                stack.append((next, path + [move]))
                nodes_generated += 1


    return [], nodes_generated, nodes_expanded

def uniform_cost_search(start_state, blocked, rows, columns):
    """
        Uniform cost search implementation which uses a priority queue 
        to explore paths and taking account costs of the path
    """
    priority_queue = []
    heapq.heappush(priority_queue, (0, start_state, []))
    visited = dict() # cost
    visited[start_state] = 0
    nodes_generated = 1
    nodes_expanded = 0

    while priority_queue:
        curr_cost, curr_state, curr_path = heapq.heappop(priority_queue)
        position, dirty_tiles = curr_state
        if not dirty_tiles:
            return curr_path, nodes_generated, nodes_expanded
        nodes_expanded += 1
        nodes = next_steps(position, dirty_tiles, blocked, rows, columns)
        for action, next_state in nodes:
            new_cost = curr_cost + 1
            if next_state not in visited or visited[next_state] > new_cost:
                visited[next_state] = new_cost
                heapq.heappush(priority_queue, (new_cost, next_state, curr_path + [action]))
                nodes_generated += 1




    return [], nodes_generated, nodes_expanded


def main():
    """My main function"""
    search_algorithm = (sys.argv[1])
    text_file = sys.argv[2]
    with open(text_file, "r") as file:
        columns = int(file.readline())
        rows = int(file.readline())
        grid = [list(file.readline().strip()) for _ in range(rows)]

    start_position = None
    dirty = set()
    blocked = set()
    for r in range(rows):
        for c in range(columns):
            if grid[r][c] == "@":
                start_position = (r, c)
            elif grid[r][c] == "*":
                dirty.add((r, c))
            elif grid[r][c] == "#":
                blocked.add((r,c))
    start_state = (start_position, frozenset(dirty))
    if search_algorithm == "depth-first":
        path, generated, expanded = depth_first_search(start_state, blocked, rows, columns)
        for action in path:
            print(action)
        print(f"{generated} nodes generated")
        print(f"{expanded} nodes expanded")
    
    if search_algorithm == "uniform-search":
        path, generated, expanded = uniform_cost_search(start_state, blocked, rows, columns)
        for action in path:
            print(action)
        print(f"{generated} nodes generated")
        print(f"{expanded} nodes expanded")

    
if __name__ == "__main__":
    main()
