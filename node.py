"""
Node class for path_finding
"""

class Node:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.H = float('inf')
        self.G = float('inf')
        self.parent = None

    def __lt__(self, other):
        return (self.H + self.G) < (other.H + other.G)

    def __str__(self):
        return "[" + str(self.coordinates[0]) + "," + \
               str(self.coordinates[1]) + "] (" + str(self.G + self.H) + ")"
