import pygame
import time
from collections import deque
import random
import pickle
import heapq

pygame.init()

pixel_color = [[255,255,255], [211, 211, 211], [255, 231, 199]]

class Node:
    def __init__(self, name, color, x, y, visited,visiting, Wall, weight):
        self.name = name
        self.color = color
        self.x = x
        self.y = y
        self.visited = visited
        self.Wall = Wall
        self.visiting = visiting
        self.neighbors = []
        self.f_score = float('inf')

    def __lt__(self, other):
        return self.f_score < other.f_score

square_size = 10
rows = 80
columns = 80
defualt_color = (0, 0, 0)
keys = (127,0,255)
key1 = (255,255,255)
search_color = (153,0,0)
wall_color = (255, 77, 0)
BUTTON_COLOR = (100, 100, 100)
BUTTON_SELECTED_COLOR = (200, 200, 200)
BUTTON_TEXT_COLOR = (255, 255, 255)

def generate_maze(nodes, square_surface, screen, start_x, start_y, end_x, end_y):
    visited = set()
    queue = deque([nodes[start_x][start_y]])
    while queue:
        current = queue.popleft()
        current.visited = True
        for neighbor in current.neighbors:
            if neighbor not in visited:
                neighbor.Wall = True
                neighbor.color = wall_color
                square_surface.fill(neighbor.color)
                screen.blit(square_surface, (neighbor.y, neighbor.x))
                pygame.draw.rect(screen, (0, 255, 0), (neighbor.y, neighbor.x, square_size, square_size), width=1)
                queue.append(neighbor)
                visited.add(neighbor)  # Add the neighbor to the visited set if it is not already visited
    nodes[end_x][end_y].Wall = False
    nodes[end_x][end_y].color = wall_color

def generate_random_walls(rows,screen, nodes, square_surface, columns, num_walls):
    for i in range(num_walls):
        wall_x = random.randint(0, rows - 1)
        wall_y = random.randint(0, columns - 1)
        current = nodes[wall_x][wall_y]
        current.Wall = True
        current.color = wall_color
        square_surface.fill(current.color)
        screen.blit(square_surface, (current.y, current.x))
        pygame.draw.rect(screen, (0, 255, 0), ( current.y, current.x, square_size, square_size), width = 1)
        pygame.display.update()

    
def heuristic(node, goal):
    # Manhattan distance heuristic
    return abs(node.x - goal.x) + abs(node.y - goal.y)

def a_star(graph, screen, square_surface, start, goal):
    parent = {start: None}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph}
    f_score[start] = heuristic(start, goal)
    open_set = []
    heapq.heappush(open_set, (f_score[start], start))

    while open_set:
        current = heapq.heappop(open_set)[1]
        current.visited = True

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = parent[current]
            return path[::-1]

        for neighbor in graph[current]:
            tentative_g_score = g_score[current] + 1  # Assuming all edges have a weight of 1

            if tentative_g_score < g_score[neighbor] and neighbor.Wall == False:
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                parent[neighbor] = current
                if neighbor.Wall == False:
                    neighbor.color = (pixel_color[1])
                    square_surface.fill(neighbor.color)
                    screen.blit(square_surface, (neighbor.y, neighbor.x))
                    pygame.draw.rect(screen, (0, 255, 0) , ( neighbor.y, neighbor.x, square_size, square_size), width = 1)
                    pygame.display.update()
                    time.sleep(0.0025)

                if neighbor not in [node[1] for node in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
            
def bfs(graph, screen, square_surface, start, goal):
    parent = {start: None}
    queue = deque([start])
    start.visited = True
    while queue:
        current = queue.popleft()
        if current not in graph:  # check if current node is in graph
            continue
        if (current.distance < 30):
            square_surface.fill(pixel_color[0])
        elif current.distance < 60:
            square_surface.fill(pixel_color[1])
        else :
            square_surface.fill(pixel_color[2])
        
        screen.blit(square_surface, (current.y, current.x))
        pygame.draw.rect(screen, (0, 255, 0), ( current.y, current.x, square_size, square_size), width = 1)
        pygame.display.update()
        time.sleep(0.0025)
        pygame.display.update()
        if current == goal:
            path = []
            while parent[current]:
                path.append(current)
                current = parent[current]
            path.append(start)
            return path[::-1]
        for i in graph[current]:
            if i.visited == False and i.Wall == False:
                i.distance += current.distance
                parent[i] = current
                queue.append(i)
                i.visited = True

def dfs(graph, screen, square_surface, start, goal):
    parent = {start: None}
    stack = [start]
    start.visited = True
    while stack:
        current = stack.pop()
        current.color = key1
        square_surface.fill(current.color)
        screen.blit(square_surface, (current.y, current.x))
        pygame.draw.rect(screen, (0, 255, 0), ( current.y, current.x, square_size, square_size), width = 1)
        time.sleep(0.0025)
        pygame.display.update()
        if current == goal:
            path = []
            while parent[current]:
                path.append(current)
                current = parent[current]
            path.append(start)
            return path[::-1]
        for i in graph[current]:
            if i.visited == False and i.Wall == False:
                parent[i] = current
                stack.append(i)
                i.visited = True

def main():
    nodes = [[None for _ in range(columns)] for _ in range(rows)]
    screen = pygame.display.set_mode((1200, 800))

    grid_filename = "my_gridGraph.pickle"
    try:
        screen_a = pygame.image.load("mygrid.png")
        screen.blit(screen_a, (0,0))
        with open(grid_filename, 'rb') as f:
            nodes = pickle.load(f)
    except:
        for row in range(rows):
            for column in range(columns):
                x = column * square_size
                y = row * square_size
                name = f"Node {row},{column}"
                node = Node(name,defualt_color, x, y,False,False, False, 1)
                nodes[row][column] = node
                pygame.draw.rect(screen, (0, 255, 0), (x, y, square_size, square_size), width = 1)
                pygame.display.update()
        pygame.image.save(screen, "mygrid.png")

        
        with open(grid_filename, 'wb') as file:
            pickle.dump(nodes, file)
    pygame.display.update()
    square_surface = pygame.Surface((square_size, square_size))
    # Add text to the screen

    buttons = []
    # Add buttons to the screen
    y = 50
    try:
        font = pygame.font.SysFont("Arial", 16)
    except pygame.error:
        pygame.font.init()
        font = pygame.font.SysFont("Arial", 16)

    for text in ["Reset","Select Nodes", "BFS", "A*", "DFS"]:
        x = 820
        button = pygame.Rect(x, y, 140, 40)
        buttons.append(button)
        pygame.draw.rect(screen, (200, 100, 40), button)
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (x + 20, y + 10))
        y += 60
    pygame.display.update()


    default_x1 = 0
    default_y1 = 0
    default_x2 = 60
    default_y2 = 60
    square_surface.fill((0,255,255))

    pygame.display.update()
    edges = {}
    for row in range(rows):
        for column in range(columns):
            if column < columns - 1:
                edges.setdefault(nodes[row][column], {})[nodes[row][column +  1]] = 1
            if column > 0:
                edges.setdefault(nodes[row][column], {})[nodes[row][column -  1]] = 1
            if row < rows - 1:
                edges.setdefault(nodes[row][column], {})[nodes[row + 1][column]] = 1        
            if row > 0:
                edges.setdefault(nodes[row][column], {})[nodes[row - 1][column]] = 1
            #if row > 0 and column > 0 and row < rows - 1 and column < columns - 1:
                #G.add_edge(nodes[row][column], nodes[row - 1][column - 1])


    generate_random_walls(rows,screen, nodes, square_surface, columns,1000)
    #generate_maze(nodes, square_surface, screen, 0, 0, 79, 79)
    while True:
        #pygame.display.update()
        for event in pygame.event.get():  
            if event.type == pygame.MOUSEMOTION:
                x, y = pygame.mouse.get_pos()
                if x > 0 and  x < (columns * square_size) and y > 0 and y < (rows * square_size):
                    column = x // square_size
                    row = y // square_size
                    #print(f"selected: {nodes[row][column].name}")
                    if nodes[row][column].color == search_color:
                        print("search_color")
                    elif nodes[row][column].color != defualt_color:
                        nodes[row][column].color = defualt_color
                        nodes[column][row].visited = False
                        nodes[column][row].Wall = False
                    else:
                        nodes[row][column].color = wall_color
                        nodes[column][row].visited = True
                        nodes[column][row].Wall = True
                    square_surface.fill(nodes[row][column].color)
                    screen.blit(square_surface, (column * square_size, row * square_size))
                    pygame.draw.rect(screen, (0, 255, 0), ( column * square_size, row * square_size, square_size, square_size), width = 1)
                    pygame.display.update()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for button, text in zip(buttons, ["Reset","Select Nodes", "BFS", "A*", "DFS"]):
                    if button.collidepoint(pygame.mouse.get_pos()):
                        if text == "Reset":
                            pygame.quit()
                            screen = pygame.display.set_mode((1200, 800))
                            main()
                        elif text == "Select Nodes":
                            count = 2
                            while count > 0:
                                for event in pygame.event.get():
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        x, y = pygame.mouse.get_pos()
                                        column = x // square_size
                                        row = y // square_size
                                        print(f"selected nodes: {nodes[row][column].name}")
                                        temp = nodes[row][column]
                                        temp.color = search_color
                                        square_surface.fill(temp.color)
                                        screen.blit(square_surface, (temp.x, temp.y))
                                        pygame.draw.rect(screen, (0, 255, 0), ( temp.x, temp.y, square_size, square_size), width = 1)
                                        pygame.display.update()
                                        if (count == 2):
                                            default_y1 = temp.x // square_size
                                            default_x1 = temp.y // square_size
                                        else:
                                            default_y2 = temp.x // square_size
                                            default_x2 = temp.y // square_size
                                        count-= 1

                        else:
                            start_node = nodes[default_y1][default_x1]
                            end_node = nodes[default_y2][default_x2]
                            if text == "A*":
                                path = a_star(edges, screen, square_surface ,start_node, end_node)
                            elif text == "BFS":
                                path = bfs(edges,screen, square_surface ,start_node, end_node)
                            else:
                                path = dfs(edges,screen, square_surface ,start_node, end_node)
                            try:
                                first_last = [path[n] for n in (0, -1)]
                            except:
                                print("No path possible")
                                
                            for val in first_last:
                                val.color = search_color
                                square_surface.fill(val.color)
                                screen.blit(square_surface, (val.y, val.x))
                                pygame.draw.rect(screen, (0, 255, 0), ( val.y, val.x, square_size, square_size), width = 1)
                                pygame.display.update()
                            for val in path[1:-1]:
                                val.color = keys
                                square_surface.fill(val.color)
                                screen.blit(square_surface, (val.y, val.x))
                                pygame.draw.rect(screen, (0, 255, 0), ( val.y, val.x, square_size, square_size), width = 1)
                                pygame.display.update()
            #exit
            if event.type == pygame.QUIT:
                pygame.quit()

main()
