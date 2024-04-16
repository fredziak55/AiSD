import bst
import avl
import os 

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
        file.write("\\begin{tikzpicture}[\n")
        file.write("level distance=1cm,\n")
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

def main():
    avl_tree = avl.AVLTree()
    bst_tree = bst.BST()
    avl_root = None
    bst_root = None

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
            print("-------------")
            continue
        if command == 'exit':
            break
        elif command == 'print':
            print("AVL tree:")
            print("In-order:", end=" ")
            avl_tree.inOrder(avl_root)
            print("\nPost-order:", end=" ")
            avl_tree.postOrder(avl_root)
            print("\nPre-order:", end=" ")
            avl_tree.preOrder(avl_root)

            print("\nBST tree:")
            print("In-order:", end=" ")
            bst_tree.inOrder(bst_root)
            print("\nPost-order:", end=" ")
            bst_tree.postOrder(bst_root)
            print("\nPre-order:", end=" ")
            bst_tree.preOrder(bst_root)
            print(" ")
        elif command == "tickz":
            print("AVL tree has been saved to a txt file:")
            writeTikzToFile(os.path.join(CURRENT_DIR, 'tickzpictureAVL.txt'), tikz_tree(avl_root))
            print("BST tree: has been saved to a txt file:")
            writeTikzToFile(os.path.join(CURRENT_DIR, 'tickzpictureBST.txt'), tikz_tree(bst_root))
        elif command == 'insert':
            # num_nodes = int(input('nodes> '))
            keys = list(map(int, input('insert> ').split()))
            for key in keys:
                avl_root = avl_tree.insert(avl_root, key)
                bst_root = bst_tree.insert(bst_root, key)
        elif command == 'delete':
            avl_root = None
            bst_root = None
            print("Trees have been cleared.")
        elif command == 'rebalance':
            avl_root = avl_tree.rebalance(avl_root)
            print("AVL tree has been rebalanced.")
        elif command == 'remove':
            keys = list(map(int, input('remove> ').split()))
            for key in keys:
                avl_root = avl_tree.delete(avl_root, key)
                bst_root = bst_tree.delete(bst_root, key)
        elif command == 'findMinMax':
            avl_min = avl_tree.minValueNode(avl_root).key
            avl_max = avl_tree.maxValueNode(avl_root).key
            bst_min = bst_tree.minValueNode(bst_root).key
            bst_max = bst_tree.maxValueNode(bst_root).key
            print(f"AVL tree: Min = {avl_min}, Max = {avl_max}")
            print(f"BST tree: Min = {bst_min}, Max = {bst_max}")
        elif command == 'sortAndMedian':
            print("AVL tree sorted:")
            avl_tree.inOrder(avl_root)
            print(f"\nMedian: {avl_tree.findMedian(avl_root)}")

            print("\nBST tree sorted:")
            bst_tree.inOrder(bst_root)
            print(f"\nMedian: {bst_tree.findMedian(bst_root)}")
        else:
            print("Unknown command. Please try again. Type help for more information.")

if __name__ == "__main__":
    main()