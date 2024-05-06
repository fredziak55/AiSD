import bst
import avl
import os 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-avl", action="store_true", help="Work on AVL tree")
parser.add_argument("-bst", action="store_true", help="Work on BST tree")
args = parser.parse_args()

CURRENT_DIR = os.path.dirname(__file__)

positions = {}

def tikz_tree_helper(node, level=0, pos=0):
    global positions
    if node is None:
        return "", pos
    # Check if the position is already occupied
    while (pos, -level) in positions:
        # If it is, shift the position to the right
        pos += 1
    # Record the position of the current node
    positions[(pos, -level)] = node.key
    result = "\\node at ({},{}) {{{}}};\n".format(pos, -level, node.key)
    if node.left:
        left_result, left_pos = tikz_tree_helper(node.left, level+1, pos-1)
        result += left_result
        result += "\\draw ({},{}) -- ({},{});\n".format(pos, -level, left_pos, -(level+1))
    if node.right:
        right_result, right_pos = tikz_tree_helper(node.right, level+1, pos+1)
        result += right_result
        result += "\\draw ({},{}) -- ({},{});\n".format(pos, -level, right_pos, -(level+1))
    return result, pos

def tikz_tree(node):
    result, _ = tikz_tree_helper(node)
    return result

def writeTikzToFile(filename, text):
    with open(filename, 'w') as file:
        file.write("\\documentclass{standalone}\n")
        file.write("\\usepackage{tikz}\n")
        file.write("\\begin{document}\n")
        file.write("\\begin{tikzpicture}\n")
        file.write("[level distance=10mm,\n")
        file.write("every node/.style={fill=red!60,circle,inner sep=1pt, minimum size=6mm},")
        file.write("level 1/.style={sibling distance=3cm},\n")
        file.write("level 2/.style={sibling distance=1.5cm},\n")
        file.write("level 3/.style={sibling distance=1cm}\n")
        file.write("]\n")
    file.close()
    with open(filename, 'a') as file:
        file.write(text)
    file.close()
    with open(filename, 'a') as file:
        file.write("\\end{tikzpicture}\n")
        file.write("\\end{document}\n")

def chosenTree(treeName, tree, root):
    treeName = treeName.upper()
    while True:
        command = input('command> ').lower()
        if command == 'help':
            print("--- Help ---")
            print("Commands:")
            print("Help - display this message")
            print("Exit - exit the program")
            print("Print - print the trees")
            print("Insert - insert a node into the trees")
            print("Delete - delete all nodes from the trees")
            print("Rebalance - rebalance the AVL tree")
            print("Remove - remove a node from the trees")
            print("FindMinMax - find the minimum and maximum values in the trees")
            print("SortAndMedian - sort the trees and find the median")
            print("Tickz - save the tree to a txt file")
            print("-------------")
            continue
        if command == 'exit':
            break
        if command == "print":
            print(treeName, " tree:")
            print("In-order:", end=" ")
            tree.inOrder(root)
            print("\nPost-order:", end=" ")
            tree.postOrder(root)
            print("\nPre-order:", end=" ")
            tree.preOrder(root)
            print("")
        elif command == "tickz":
                print(f"{treeName} tree has been saved to a txt file:")
                writeTikzToFile(os.path.join(CURRENT_DIR, f"tickzpicture{treeName}.txt"), tikz_tree(root))
        elif command == 'insert':
            num_nodes = int(input('nodes> '))
            keys = list(map(int, input('insert> ').split()))
            for key in keys:
                root = tree.insert(root, key)
        elif command == 'delete':
                root = None
                print(f"All nodes have been deleted from the {treeName} tree.")
        elif command == 'rebalance':
            root = tree.rebalance(root)
            print(f"{treeName} tree has been balanced.")
        elif command == 'remove':
            keys = list(map(int, input('remove> ').split()))
            for key in keys:
                root = tree.delete(root, key)
        elif command == 'findminmax':
            minTree = tree.minValueNode(root).key
            maxTree = tree.maxValueNode(root).key
            print(f"{treeName} tree: Min = {minTree}, Max = {maxTree}")
        elif command == 'sortandmedian':
            print(f"{treeName} tree sorted:")
            tree.inOrder(root)
            print(f"\nMedian: {tree.findMedian(root)}")
        else:
            print("Unknown command. Please try again. Type help for more information.")

def main():
    avl_tree = avl.AVLTree()
    bst_tree = bst.BST()
    avl_root = None
    bst_root = None

    if args.avl:
        chosenTree("AVL", avl_tree, avl_root)
    if args.bst:
        chosenTree("BST", bst_tree, bst_root)

if __name__ == "__main__":
    main()