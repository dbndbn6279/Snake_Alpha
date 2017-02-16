from operator import *

class Node:
    def __init__(self, coordinate):
        #Node Parameters:
        self.coordinate = coordinate    #[x,y]
        self.disToTarget = 0

    def Cal_Distance(self, target):
        #Calculate the dfference in Coordinate between Target and Node
        if isinstance(target, Node):
            difference = map(sub, self.coordinate, target.coordinate)
        elif isinstance(target, list):
            difference = map(sub, self.coordinate, target)
        #Set Node's distance to target
        self.disToTarget = abs(difference[0]) + abs(difference[1])

def node(coordinate, target = False):
    #Convert a list to a Node
    if target == False:
        return Node(coordinate)
    #Convert a coordinate to Node and Calculate the Distance to Target
    else:
        node = Node(coordinate)
        node.Cal_Distance(target)
        return node
