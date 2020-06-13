import sys
"""
Author: Abhay Vivek Kulkarni
Id: ak6277@rit.edu
Lab - 1
"""
import numpy as np
from PIL import Image


# ****************************************************************************************************
class Node:
    def __init__(self, coordinates):
        """
        F = G + H
        F cost is the final cost to traverse to this point
        :param coordinates: The coordinates of the current point
        :param H: The heuristic cost
        :param G: The path cost
        :param parent: The previous node/point
        """
        self.coordinates = coordinates
        self.H = float('inf')
        self.G = float('inf')
        self.parent = None

    def __lt__(self, other):
        """
        For F cost comparison between two nodes
        :param other: The node that is being compared with the current node
        :return: True if current position is better than the other
        """
        return (self.H + self.G) < (other.H + other.G)

    def __str__(self):
        """
        Print statement in the form:  [x_coordinate, y_coordinate] (total_cost)
        :return:
        """
        return "[" + str(self.coordinates[0]) + "," + \
               str(self.coordinates[1]) + "] (" + str(self.G + self.H) + ")"


# ****************************************************************************************************
"""
Dictionary for color-speed mapping
Assumptions of average speed on such terrains by humans
    key: (r, g, b)
    value: speed
"""
color_map = {
    (248, 148, 18): 6,  # openLand
    (255, 192, 0): 5.5,  # meadow
    (255, 255, 255): 4.5,  # easyForest
    (2, 208, 60): 4,  # slowRun
    (2, 136, 40): 3,  # walkForest
    (5, 73, 24): 0.05,  # impassableVeg
    (0, 0, 255): 1,  # water
    (71, 51, 3): 8,  # road
    (0, 0, 0): 7.5,  # footpath
    (205, 0, 101): 0.000000001,  # Pink/OutOfBound
    (0, 255, 255): 0.5,  # Ice
    (139, 69, 19): 0.4  # Mud
}


# ****************************************************************************************************
def get_everything():
    """
    For creating a 3D map from the current 2D image and the elevation text file
    each row has --> [x_coordinate, y_coordinate, [z_coordinate, color]]

    :return: [395 x 500 x 2] matrix assuming that's the size of the original map
    """
    everything = np.zeros([rgb.size[0], rgb.size[1], 2])
    for rows in range(rgb.size[0]):  # horizontal
        for columns in range(rgb.size[1]):  # vertical
            everything[rows, columns, 0] = elevations[rows, columns]
            everything[rows, columns, 1] = color_map[pixel[rows, columns]]
    return everything


# ****************************************************************************************************
def get_neighbours(this_node, a=1):
    """
    Returns the neighbours of a node; A square format is considered

     1  2  3  4  5  6
     7  8  9 10 11 12
    13 14 15 16 17 18
    19 20 21 22 23 24
    25 26 27 28 29 30

    In the above matrix; if a=1 and this_node=15
    neighbours will be [8, 9, 10, 14, 16, 20, 21, 22]

    :param this_node: Current node/ Parent node
    :param a: The depth of neighbour node;
    :return: An array of all the near-by nodes in the form [ [x1, y1], [x1, y2], ... ]
    """
    x, y = this_node[0], this_node[1]
    operations = range(-a, (a + 1))
    allX, allY = [], []
    for values_individual in operations:
        # Considering the edge cases
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
def winter_border_color(from_this, to_this):
    """
    Changes the border color (from_this) to other color (to_this)
    Here we use --> [Blue -> Cyan]
    Blue is water; Cyan is ice
    :param from_this: Original color on map
    :param to_this: New color to be displayed
    :return: None; changes are made in the global array - big_table
    """
    visited = set()
    for rr in range(rgb.size[0]):
        for cc in range(rgb.size[1]):
            if pixel[rr, cc] == from_this:
                sides = get_neighbours([rr, cc], 1)
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
        big_table[x, y, 1] = color_map[to_this]


# ****************************************************************************************************
def winter():
    """
    Helper function for winter_border_color()
    6-pixel depth for ice-formation
    :return:
    """
    for _ in range(6):
        winter_border_color((0, 0, 255), (0, 255, 255))


# ****************************************************************************************************
def mud_map():
    """
    Generated a Mud map for spring season
    Every point which has an elevation within 1 meter of water turns to mud within an 15-pixel square radius.
    Different ponds have different elevations, hence there's a variable water level, so a global
    change can't be made, and each water pixel has to be considered.

    :return: The big_table color codes are altered
    """
    color_this = set()
    water_set = get_water_border()
    for tup in water_set:
        r, c = tup[0], tup[1]
        if pixel[r, c] == (0, 0, 255):
            this_elevation = big_table[r, c, 0]
            fifteen_sides = get_neighbours([r, c], 15)
            for each_side in fifteen_sides:
                x1, y1 = each_side[0], each_side[1]
                if (x1, y1) not in color_this:
                    if (pixel[x1, y1] != (0, 0, 255)) and (
                            big_table[x1, y1, 0] < (this_elevation + 1)):
                        color_this.add((x1, y1))

    visited = list(color_this)
    for tup in visited:
        x, y = int(tup[0]), int(tup[1])
        if pixel[x, y] != (205, 0, 101):
            pixel[x, y] = (139, 69, 19)
        big_table[x, y, 1] = color_map[(139, 69, 19)]


# ****************************************************************************************************
def fall():
    """
    Generates a Fall-map; no color changes on the map are made
    The roads and pavements passing through the forest are not clearly visible during this season
    hence, careful traversing is required; the speed is reduced from (8, 7.5) to 6
    only for the paths near to forests

    :return: speeds of the paths are altered in the global big_table
    """
    visited = set()
    for rr in range(rgb.size[0]):
        for cc in range(rgb.size[1]):
            if (pixel[rr, cc] == (0, 0, 0)) or (pixel[rr, cc] == (71, 51, 3)):
                sides = get_neighbours([rr, cc], 1)
                forest = False
                for side in sides:
                    if pixel[side[0], side[1]] == (255, 255, 255):
                        forest = True
                if forest:
                    visited.add((rr, cc))
    visited = list(visited)
    for tup in visited:
        x, y = int(tup[0]), int(tup[1])
        big_table[x, y, 1] = 6


# ****************************************************************************************************
def get_water_border():
    """
    Searches the entire map for water and creates a set of points which
    correspond to water; As it's required for mud/winter
    :return:
    """
    visited = set()
    for rr in range(rgb.size[0]):
        for cc in range(rgb.size[1]):
            if pixel[rr, cc] == (0, 0, 255):
                sides = get_neighbours([rr, cc], 1)
                land = False
                for side in sides:
                    if pixel[side[0], side[1]] != (0, 0, 255):
                        land = True
                if land:
                    visited.add((rr, cc))
    return visited


# ****************************************************************************************************
def h(node):
    """
    Calculates the direct displacement between the start and end points on the map
    assuming an ideal path for consistency (monotonicity) where there's no difference
    of elevation between the points and there's a straight road between them.

    :param node: Current starting node
    :return: Heuristic Cost (h)
    """
    x2, y2 = end[0], end[1]  # End node
    x1, y1 = node[0], node[1]  # Start node
    z1 = big_table[x1, y1, 0]
    z2 = big_table[x2, y2, 0]
    answer = (((((x2 - x1) * X_DISTANCE) ** 2) + (((y2 - y1) * Y_DISTANCE) ** 2)) ** 0.5)
    height = abs(z2 - z1)
    total = ((answer ** 2) + (height ** 2)) ** 0.5
    # This color_map value is of a road.
    return total / color_map.get((71, 51, 3))


# ****************************************************************************************************
def g(parent, child):
    """
    The path cost between parent node to it's child

    Here we consider the difference in elevation, as walking up an incline will take more time
    and effort than walking on a level path.
    Similar to h() with an exception of angle_multiplier

    :param parent: Parent node
    :param child: the next node, child
    :return: the path cost
    """
    x1, y1 = parent[0], parent[1]
    z1, s1 = big_table[x1, y1, 0], big_table[x1, y1, 1]

    x2, y2 = child[0], child[1]
    z2, s2 = big_table[x2, y2, 0], big_table[x2, y2, 1]

    answer = (((((x2 - x1) * X_DISTANCE) ** 2) + (((y2 - y1) * Y_DISTANCE) ** 2)) ** 0.5)
    height = abs(z2 - z1)
    total = ((answer ** 2) + (height ** 2)) ** 0.5
    if total == 0:
        return 0
    angle_multiplier = answer / total
    avg_s = ((s1 + s2) / 2) * angle_multiplier

    return total / avg_s


# ****************************************************************************************************
def get_neighbours_nodes(this_node, a=1):
    """
    Same as get_neighbours; made some changes later for different form of input
    tuple instead of the previously used coordinates

    :param this_node: current node
    :param a: depth
    :return: an array of tuples [ (F_cost1, Node1), (F_cost2, Node2), ... ]
            F_costX is the total cost to travel
            NodeX is the neighbouring node

    """
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
            newNode.H = h([xx, yy])
            newNode.G = g(this_node.coordinates, [xx, yy])
            if not newNode.coordinates == this_node.coordinates:
                result.append(((newNode.H + newNode.G), newNode))
    return result


# ****************************************************************************************************
def get_lowest(some_list):
    """
    Finds the node with the lowest F cost from the list
    :param some_list: A list of nodes
    :return: Node with lowest cost
    """
    minimum = float('inf')
    key = some_list[0]
    for some_node in some_list:
        if (some_node[1].H + some_node[1].G) < minimum:
            minimum = some_node[1].H + some_node[1].G
            key = some_node
    return key


# ****************************************************************************************************
def get_distance_for_printing(a, b):
    """
    Considers the elevation difference
    :param a: Point_1
    :param b: Point_2
    :return: Distance between Point_1 and Point_2
    """
    if a is None:
        return 0
    if b is None:
        return 0

    x1, y1 = a.coordinates[0], a.coordinates[1]
    z1 = big_table[x1, y1, 0]

    x2, y2 = b.coordinates[0], b.coordinates[1]
    z2 = big_table[x2, y2, 0]

    answer = (((((x2 - x1) * X_DISTANCE) ** 2) + (((y2 - y1) * Y_DISTANCE) ** 2)) ** 0.5)
    height = abs(z2 - z1)
    total = ((answer ** 2) + (height ** 2)) ** 0.5
    return total


# ****************************************************************************************************
def get_path(some_node):
    """
    Gets the final distance travelled if the recommended path is chosen
    Marks the recommended path on the map
    :param some_node: Parent
    :return: Total distance to be travelled
    """
    total = 0
    p = some_node.parent
    this_distance = get_distance_for_printing(p, some_node)
    total += this_distance

    while p is not None:
        children = get_neighbours(p.coordinates, 1)
        total += get_distance_for_printing(p, p.parent)
        for child in children:
            pixel[child[0], child[1]] = (55, 0, 25)
            # Comment this out
            final_path.append(child)
        p = p.parent
    return total


# ****************************************************************************************************
def set_compare(n, open_set):
    """
    To make sure there are no duplicate nodes
    Ideally it is unnecessary, but in case there's any Node with same coordinates but different values

    :param n: Node
    :param open_set: Set of nodes
    :return: True if the node_N and any node of the set has same coordinates
    """
    for child in open_set:
        if n[1].coordinates == child[1].coordinates:
            return True
    return False


# ****************************************************************************************************
def delete_node(n, open_set):
    """
    To make sure there are no duplicate nodes
    Ideally it is unnecessary, but in case there's any Node with same coordinates but different values
    the duplicate is removed.

    :param n: Node
    :param open_set: Set of nodes
    :return: open_set without the duplicate
    """
    for child in open_set:
        if n[1].coordinates == child[1].coordinates:
            open_set.remove(child)
    return open_set


# ****************************************************************************************************
def do_a_star():
    """
    A-star Algorithm
    Basically a best-first-search with a path cost and a heuristic cost
    :return:
    """
    start_node = Node(start)
    start_node.G = 0
    start_node.H = h(start_node.coordinates)
    open_set = [((start_node.G + start_node.H), start_node)]  # has (fCost, Node)

    end_node = Node(end)
    end_node.H = 0

    closed_set = set()  # has (x,y)
    while len(open_set) != 0:
        current_tup = get_lowest(open_set)
        open_set.remove(current_tup)
        # Comment this out
        ALL_THE_POINTS.append(current_tup)
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

img_file = sys.argv[1]
elev_file = sys.argv[2]
node_file = sys.argv[3]
season = sys.argv[4]
op_img_file = sys.argv[5]

X_DISTANCE = 10.29 # Real-world inter-pixel distance on X-axis in meters
Y_DISTANCE = 7.55 # Real-world inter-pixel distance on Y-axis in meters

# Comment this out
ALL_THE_POINTS = []

elevations = np.loadtxt(elev_file)
elevations = elevations.transpose()
img = Image.open(img_file)
nodes = np.loadtxt(node_file)

rgb = img.convert('RGB')
pixel = rgb.load()
big_table = get_everything()

if season == "winter":
    print()
    winter()
elif season == "spring":
    print()
    mud_map()
elif season == "fall":
    print()
    fall()
elif season == "summer":
    print()

total_distance = 0
"""
for i in range(len(nodes) - 1):
    start = [int(nodes[i][0]), int(nodes[i][1])]
    end = [int(nodes[i + 1][0]), int(nodes[i + 1][1])]
    total_distance += do_a_star()

    # All the points that are "looked at" in red
    # for pt in ALL_THE_POINTS:
        # c = pt[1].coordinates
        # pixel[c[0], c[1]] = (255, 0, 0)

    # All the stops that are to be made in pink
    for point in [start, end]:
        all_point = get_neighbours(point, 3)
        for k in all_point:
            pixel[k[0], k[1]] = (76, 0, 153)
"""


print("Total distance is: ", total_distance)
rgb.save(op_img_file + ".jpg")
