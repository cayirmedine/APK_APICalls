import re

with open("cg.txt") as file:
    lines = file.readlines()

class TreeNode:
    def __init__(self, data):   # constructor
        self.data = data
        self.children = []
        self.parent = None

    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent    # getting level from parent node
        return level

    def print_tree(self):
        spaces = ' ' * self.get_level() * 3     # spaces for show leaf's levels
        prefix = spaces + str(self.get_level())+" |" if self.parent else ""
        print(prefix + self.data)
        if self.children:
            for child in self.children:
                child.print_tree()

    def add_child(self, child):
        child.parent = self
        self.children.append(child)     # add child to the parent

def build_product_tree():
    #root = TreeNode("Entry")   # starting point of the tree/call graph
    text_arr = []
    node_arr = []
    text2_arr = []
    node2_arr = []
    root_arr = []

    for i in range(len(lines)):
        counter = 0
        if "Children of" in lines[i]:   # if a line contains "Children of" then it should be a node
            text = re.split('<|>', str(lines[i]))   # split from "<" and ">" for getting exact API call
            for j in range(len(lines)):
                if text[1] in lines[j]:
                    counter += 1
                    if counter == 2:
                        break

            if counter < 2:     # if a node mentioned in the callgraph file in once,
                                # then this node is nobody's child API, so should be a root
                text_arr.append(text[1])    # add node's value to an array, because we will search child nodes
                                            # using comparison with this array
                lvl1 = TreeNode(text[1])    # we use 1. index's value because, in this split operation
                                            # API call's name in index 1
                node_arr.append(lvl1)
                root_arr.append(lvl1)
                #root.add_child(lvl1)        # add node to an array, because we will search child nodes
                                            # with this array

    for x in range(30):
        for s in range(len(lines)):
            for y in range(len(text_arr)):
                if "Children of <"+text_arr[y] in lines[s]:     # if a node is in the array we previously
                                                                # created, we can look for children in the bottom rows
                    if (s+1) < len(lines):
                        z = s + 1
                    else:
                        break
                    while not("Children of" in lines[z]):       # if the line we're on doesn't include 'Children of',
                                                                # it's a child node
                        text2 = re.split('<|>', str(lines[z]))
                        text2_arr.append(text2[1])              # add this node to another array for next level
                        leaf = TreeNode(text2[1])
                        node2_arr.append(leaf)
                        node_arr[y].add_child(leaf)
                        if (z+1) < len(lines):
                            z += 1
                        else:
                            break

        node_arr = node2_arr        # exchange arrays for moving the next level
        node2_arr = []
        text_arr = text2_arr
        text2_arr = []

    for z in range(len(root_arr)):
        root_arr[z].print_tree()
        print("\n")

if __name__ == '__main__':
    build_product_tree()
