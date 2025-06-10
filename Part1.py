import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import heapq
from collections import deque

def asteroid_visualization(csv_file_path):
    df = pd.read_csv(csv_file_path)
    colx = df['X']
    coly = df['Y']
    colsize = df['Size']
    available_sector = []
    for limiti in range(0, 1000, 100):
        for limitj in range(0, 1000, 100):
            dotinrange = []
            for i in range(0, 300, 1):
                if colx[i] <= limiti and coly[i] <= limitj:
                    available_sector.append(str(limiti) + ", " + str(limitj))

    #Grid plotting definition
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.scatter(colx, coly, s=5, c='blue')
    ax.set_xlim([0, 1000])
    ax.set_ylim([0, 1000])
    ax.set_xticks(range(0, 1000 + 1, 100))
    ax.set_yticks(range(0, 1000 + 1, 100))
    plt.scatter(df['X'], df['Y'], s=df['Size'] * 10, alpha=0.6)
    plt.grid(True)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Asteroid Positions with Size Visualization')
    plt.show()


def group_asteroids_to_grid(csv_file_path, grid_size=100, field_size=1000):

    df = pd.read_csv(csv_file_path)
    num_cells = field_size // grid_size
    grid = [[0 for _ in range(num_cells)] for _ in range(num_cells)]
    df['grid_x'] = df['X'] // grid_size
    df['grid_y'] = df['Y'] // grid_size
    grouped = df.groupby(['grid_x', 'grid_y'])['Size'].sum().reset_index()

    for _, row in grouped.iterrows():
        x = int(row['grid_x'])
        y = int(row['grid_y'])
        size_sum = int(row['Size'])
        if 0 <= x < num_cells and 0 <= y < num_cells:
            grid[y][x] = size_sum

    return grid

def group_asteroids_to_grid(csv_file_path, grid_size=100, field_size=1000):
    df = pd.read_csv(csv_file_path)

    num_cells = field_size // grid_size
    grid = [[0 for _ in range(num_cells)] for _ in range(num_cells)]
    df['grid_x'] = df['X'] // grid_size
    df['grid_y'] = df['Y'] // grid_size
    grouped = df.groupby(['grid_x', 'grid_y'])['Size'].sum().reset_index()

    for _, row in grouped.iterrows():
        x = int(row['grid_x'])
        y = int(row['grid_y'])
        size_sum = int(row['Size'])
        if 0 <= x < num_cells and 0 <= y < num_cells:
            grid[y][x] = size_sum

    return grid

def group_asteroids_to_grid(csv_file_path, grid_size=100, field_size=1000):
    df = pd.read_csv(csv_file_path)

    num_cells = field_size // grid_size
    grid = [[0 for _ in range(num_cells)] for _ in range(num_cells)]

    df['grid_x'] = df['X'] // grid_size
    df['grid_y'] = df['Y'] // grid_size

    grouped = df.groupby(['grid_x', 'grid_y'])['Size'].sum().reset_index()

    for _, row in grouped.iterrows():
        x = int(row['grid_x'])
        y = int(row['grid_y'])
        size_sum = int(row['Size'])
        if 0 <= x < num_cells and 0 <= y < num_cells:
            grid[y][x] = size_sum

    return grid

def hexagonal_neighbors(x, y, max_x, max_y):
    neighbors = []
    #Up
    if y > 0:
        neighbors.append((x, y-1))
    #Down
    if y < max_y - 1:
        neighbors.append((x, y+1))
    #Left
    if x > 0:
        neighbors.append((x-1, y))
    #Right
    if x < max_x - 1:
        neighbors.append((x+1, y))
    #Up-Left
    if x > 0 and y > 0:
        neighbors.append((x-1, y-1))
    #Up-Right
    if x < max_x - 1 and y > 0:
        neighbors.append((x+1, y-1))
    #Down-Left
    if x > 0 and y < max_y - 1:
        neighbors.append((x-1, y+1))
    #Down-Right
    if x < max_x - 1 and y < max_y - 1:
        neighbors.append((x+1, y+1))

    return neighbors


def dijkstra_safest_path(grid, start=(0, 0)):
    max_y = len(grid)
    max_x = len(grid[0])

    distances = {}
    prev = {}

    for y in range(max_y):
        for x in range(max_x):
            distances[(x, y)] = float('inf')

    sx, sy = start
    if not (0 <= sx < max_x and 0 <= sy < max_y):
        raise ValueError(f"Start position {start} is outside the grid bounds.")

    if grid[sy][sx] > 30:
        return None, float('inf')

    distances[(sx, sy)] = grid[sy][sx]
    pq = [(grid[sy][sx], sx, sy)]
    prev[(sx, sy)] = None

    while pq:
        current_cost, x, y = heapq.heappop(pq)

        if current_cost > distances[(x, y)]:
            continue

        #Rightmost path reached, find the path that we visited just now
        if x == max_x - 1:
            path = []
            cur = (x, y)
            while cur is not None:
                path.append(cur)
                cur = prev[cur]
            path.reverse()
            return path, current_cost

        for nx, ny in hexagonal_neighbors(x, y, max_x, max_y):
            neighbor_danger = grid[ny][nx]
            #dense underbrush
            if neighbor_danger > 32:
                continue

            #Calculate new cost
            new_cost = current_cost + neighbor_danger

            #Only consider path if it's better than previously found path to (nx, ny)
            if new_cost < distances[(nx, ny)]:
                distances[(nx, ny)] = new_cost
                prev[(nx, ny)] = (x, y)
                #Push to priority queue
                heapq.heappush(pq, (new_cost, nx, ny))

    return None, float('inf')


def group_asteroids_to_3d_array(csv_file_path):
    df = pd.read_csv(csv_file_path)
    # Calculate grid cell indices by integer division
    df['grid_x'] = df['X'] // 100
    df['grid_y'] = df['Y'] // 100
    # Group by the grid cell coordinates and sum the sizes
    grouped = df.groupby(['grid_x', 'grid_y'])['Size'].sum().reset_index()
    # Convert to list of lists [grid_x, grid_y, total_size]
    result_array = grouped.values.tolist()
    return result_array

def find_average_size(array):
    total_size = 0
    for i in range(0, len(array), 1):
        total_size += array[i][2]
    average_size = int(total_size / len(array))
    return average_size

# Main
if __name__ == "__main__":
    file_path = (r'C:\Users\22002\OneDrive\Desktop\UM\Sem 4\Algorithm &\Assignment\Asteroid_Field_Data.csv')
    asteroid_visualization(file_path)
    array=group_asteroids_to_3d_array(file_path)
    average_size = find_average_size(array)
    print("Array with total size of each area : ")
    print(array)
    print()
    print("Average total size of asteroid of all area = ",average_size)
    print()

    grid = group_asteroids_to_grid(file_path)
    path, cost = dijkstra_safest_path(grid)

    if path is None:
        print("No path found to the right side of the field.")
    else:
        print(f"Safest path with dangerousity size ",cost, ":")
        for x, y in path:
            print(f"({x},{y}) with danger {grid[y][x]}")

