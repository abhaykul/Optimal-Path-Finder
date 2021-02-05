import numpy as np
from PIL import Image

from color_map import color_map
from node import Node


# ****************************************************************************************************
# Returns EVERYTHING MATRIX:  m[x, y, [z, color_code]] -> shape(395,500,2)
def populate_matrix():
    result_matrix = np.zeros([height, width, 2])
    for rows in range(height):  # horizontal
        for columns in range(width):  # vertical
            result_matrix[rows, columns, 0] = elevations[rows, columns]  # elevation
            result_matrix[rows, columns, 1] = color_map[pixel[rows, columns]]  # speed
    return result_matrix


# ****************************************************************************************************
# Returns neighbours of the current pixel [ [x1, y1], [x1, y2], ... ]
def get_neighbors(this_node, a=1):  # [i,j]
    x, y = this_node[0], this_node[1]
    operations = range(-a, (a + 1))
    allX, allY = [], []
    for values_individual in operations:
        if -1 < (x + int(values_individual)) < 395:
            allX.append(x + int(values_individual))
        if -1 < (y + int(values_individual)) < 500:
            allY.append(y + int(values_individual))
    result = []
    for xx in allX:
        for yy in allY:
            result.append([xx, yy])
    return result


# ****************************************************************************************************
# Changes the border color(from_this) to other color (to_this) --> [Blue -> Cyan]
def winter_border_color(from_this, to_this):
    visited = set()
    for rr in range(height):
        for cc in range(width):
            if pixel[rr, cc] == from_this:
                sides = get_neighbors([rr, cc], 1)
                land = False
                for side in sides:
                    if pixel[side[0], side[1]] != from_this:
                        land = True
                if land:
                    visited.add((rr, cc))
    visited = list(visited)
    for tup in visited:
        x, y = int(tup[0]), int(tup[1])
        pixel[x, y] = to_this
        data_matrix[x, y, 1] = color_map[to_this]


# ****************************************************************************************************
# Winter map helper for border_color()
def winter():
    for _ in range(6):
        winter_border_color((0, 0, 255), (0, 255, 255))


# ****************************************************************************************************
# Mud map for spring season; 15 pixel wide with elevation < 1m to BROWN
def mud_map():
    color_this = set()
    water_set = get_water_border()
    for tup in water_set:
        r, c = tup[0], tup[1]
        if pixel[r, c] == (0, 0, 255):
            this_elevation = data_matrix[r, c, 0]
            fifteen_sides = get_neighbors([r, c], 15)
            for each_side in fifteen_sides:
                x1, y1 = each_side[0], each_side[1]
                if (x1, y1) not in color_this:
                    if (pixel[x1, y1] != (0, 0, 255)) and (
                            data_matrix[x1, y1, 0] < (this_elevation + 1)):
                        color_this.add((x1, y1))

    visited = list(color_this)
    for tup in visited:
        x, y = int(tup[0]), int(tup[1])
        if pixel[x, y] != (205, 0, 101):
            pixel[x, y] = (139, 69, 19)
        data_matrix[x, y, 1] = color_map[(139, 69, 19)]


# ****************************************************************************************************
# Fall map: speeds on (road, footpaths) is 6 from (8, 7.5)
#           if they are adjacent to a easy movement forest
def fall():
    visited = set()
    for rr in range(height):
        for cc in range(width):
            if (pixel[rr, cc] == (0, 0, 0)) or (pixel[rr, cc] == (71, 51, 3)):
                sides = get_neighbors([rr, cc], 1)
                forest = False
                for side in sides:
                    if pixel[side[0], side[1]] == (255, 255, 255):
                        forest = True
                if forest:
                    visited.add((rr, cc))
    visited = list(visited)
    for tup in visited:
        x, y = int(tup[0]), int(tup[1])
        data_matrix[x, y, 1] = 6


# ****************************************************************************************************
# Gets the water boundary
def get_water_border():
    visited = set()
    for rr in range(height):
        for cc in range(width):
            if pixel[rr, cc] == (0, 0, 255):
                sides = get_neighbors([rr, cc], 1)
                land = False
                for side in sides:
                    if pixel[side[0], side[1]] != (0, 0, 255):
                        land = True
                if land:
                    visited.add((rr, cc))
    return visited


# ****************************************************************************************************
# H cost: time take by displacement and a direct footpath
def heuristic(node):
    x2, y2 = end[0], end[1]  # End node
    x1, y1 = node[0], node[1]  # Start node
    z1 = data_matrix[x1, y1, 0]
    z2 = data_matrix[x2, y2, 0]
    answer = (((((x2 - x1) * 10.29) ** 2) + (((y2 - y1) * 7.55) ** 2)) ** 0.5)
    height = abs(z2 - z1)
    total = ((answer ** 2) + (height ** 2)) ** 0.5
    return total / 8


# ****************************************************************************************************
# G cost: time taken to travel between parent and child locations
def path_cost(parent, child):
    x1, y1 = parent[0], parent[1]
    z1, s1 = data_matrix[x1, y1, 0], data_matrix[x1, y1, 1]

    x2, y2 = child[0], child[1]
    z2, s2 = data_matrix[x2, y2, 0], data_matrix[x2, y2, 1]

    answer = (((((x2 - x1) * 10.29) ** 2) + (((y2 - y1) * 7.55) ** 2)) ** 0.5)
    height = abs(z2 - z1)
    total = ((answer ** 2) + (height ** 2)) ** 0.5
    if total == 0:
        return 0
    angle_multiplier = answer / total
    avg_s = ((s1 + s2) / 2) * angle_multiplier

    return total / avg_s


# ****************************************************************************************************
# Returns neighbours of the current node [ tup.Node1, tup.Node2,... ]
# FORM::  [ (fCost, Node), .... ]
def get_neighbours_nodes(this_node, a=1):  # [i,j]
    x, y = this_node.coordinates[0], this_node.coordinates[1]
    operations = range(-a, (a + 1))
    allX, allY = [], []
    for values_individual in operations:
        if -1 < (x + int(values_individual)) < 395:
            allX.append(x + int(values_individual))
        if -1 < (y + int(values_individual)) < 500:
            allY.append(y + int(values_individual))
    result = []
    for xx in allX:
        for yy in allY:
            newNode = Node([xx, yy])
            newNode.H = heuristic([xx, yy])
            newNode.G = path_cost(this_node.coordinates, [xx, yy])
            if not newNode.coordinates == this_node.coordinates:
                result.append(((newNode.H + newNode.G), newNode))

    return result


# ****************************************************************************************************
# Lowest F node
def get_lowest(some_list):
    minimum = float('inf')
    key = some_list[0]
    for some_node in some_list:
        if (some_node[1].H + some_node[1].G) < minimum:
            minimum = some_node[1].H + some_node[1].G
            key = some_node
    return key


# ****************************************************************************************************
def get_distance_for_printing(a, b):
    if a is None:
        return 0
    if b is None:
        return 0

    x1, y1 = a.coordinates[0], a.coordinates[1]
    z1 = data_matrix[x1, y1, 0]

    x2, y2 = b.coordinates[0], b.coordinates[1]
    z2 = data_matrix[x2, y2, 0]

    answer = (((((x2 - x1) * 10.29) ** 2) + (((y2 - y1) * 7.55) ** 2)) ** 0.5)
    H = abs(z2 - z1)
    total = ((answer ** 2) + (H ** 2)) ** 0.5
    return total


# ****************************************************************************************************
# Prints path on the path
def get_path(some_node):
    total = 0
    p = some_node.parent
    gg = get_distance_for_printing(p, some_node)
    total += gg

    while p is not None:
        all_neighbors = get_neighbors(p.coordinates, 1)
        total += get_distance_for_printing(p, p.parent)
        for neighbor in all_neighbors:
            pixel[neighbor[0], neighbor[1]] = (255, 105, 180)
        p = p.parent
    return total


# ****************************************************************************************************
# Checks if 2 Nodes have the same coordinates
def set_compare(n, open_set):
    for child in open_set:
        if n[1].coordinates == child[1].coordinates:
            return True
    return False


# ****************************************************************************************************
# Deletes the node with same coordinates as input from open_set
def delete_node(n, open_set):
    for child in open_set:
        if n[1].coordinates == child[1].coordinates:
            open_set.remove(child)
    return open_set


# ****************************************************************************************************
# Algorithm
def do_a_star_search():
    start_node = Node(start)
    start_node.G = 0
    start_node.H = heuristic(start_node.coordinates)
    open_set = [((start_node.G + start_node.H), start_node)]  # has (fCost, Node)

    end_node = Node(end)
    end_node.H = 0

    closed_set = set()  # has (x,y)
    while len(open_set) != 0:
        current_tup = get_lowest(open_set)
        open_set.remove(current_tup)

        current_node = current_tup[1]
        if current_node.coordinates == end_node.coordinates:
            distance = get_path(current_node)
            return distance
        temp_tuple = (current_node.coordinates[0], current_node.coordinates[1])
        closed_set.add(temp_tuple)
        neighbours = get_neighbours_nodes(current_node)
        for n in neighbours:
            if current_tup[1].coordinates == n[1].coordinates:
                neighbours.remove(n)
                continue
            cost = current_node.G + n[1].G
            if set_compare(n, open_set) and (cost < n[1].G):
                open_set = delete_node(n, open_set)

            if ((n[1].coordinates[0], n[1].coordinates[1]) in closed_set) and (cost < n[1].G):
                closed_set.remove((n[1].coordinates[0], n[1].coordinates[1]))

            if (not set_compare(n, open_set)) and ((n[1].coordinates[0], n[1].coordinates[1]) not in closed_set):
                n[1].G = cost
                n[1].parent = current_node
                open_set.append(n)


# ****************************************************************************************************
def alter_map(current_season):
    if current_season == "winter":
        winter()
    elif current_season == "spring":
        mud_map()
    elif current_season == "fall":
        fall()


# ****************************************************************************************************

def main():
    img_file = "terrain.png"  # sys.argv[1]
    elev_file = "elevations.txt"  # sys.argv[2]
    node_file = "check_points.txt"  # sys.argv[3]
    season = "spring"  # sys.argv[4]
    op_img_file = "result"  # sys.argv[5]
    global elevations
    elevations = np.loadtxt(elev_file).transpose()
    checkpoints = np.loadtxt(node_file)

    image_data = Image.open(img_file)
    image_rgb = image_data.convert('RGB')
    global height, width
    height, width = image_rgb.size[0], image_rgb.size[1]
    global pixel
    pixel = image_rgb.load()
    global data_matrix
    data_matrix = populate_matrix()
    alter_map(season)

    total_distance = 0
    for i in range(len(checkpoints) - 1):
        global start, end
        start = [int(checkpoints[i][0]), int(checkpoints[i][1])]
        end = [int(checkpoints[i + 1][0]), int(checkpoints[i + 1][1])]

        for point in [start, end]:
            all_point = get_neighbors(point, 2)
            for k in all_point:
                pixel[k[0], k[1]] = (75, 0, 130)
        total_distance += do_a_star_search()
    print("Total distance is: ", total_distance)
    image_rgb.save(op_img_file + ".jpg")


if __name__ == '__main__':
    main()