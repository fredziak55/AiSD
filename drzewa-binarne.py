class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

def tikz_tree(node, level=0, pos=0):
    if node is None:
        return ""
    result = "\\node at ({},{}) {{{}}};\n".format(pos, -level, node.key)
    if node.left:
        result += "\\draw ({},{}) -- ({},{});\n".format(pos, -level, pos-1, -(level+1))
        result += tikz_tree(node.left, level+1, pos-1)
    if node.right:
        result += "\\draw ({},{}) -- ({},{});\n".format(pos, -level, pos+1, -(level+1))
        result += tikz_tree(node.right, level+1, pos+1)
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

class AVLTree:
    def storeBSTNodes(self, root, nodes):
        # Base case
        if not root:
            return

        # Store nodes of left subtree
        self.storeBSTNodes(root.left, nodes)

        # Store this node
        nodes.append(root)

        # Store nodes of right subtree
        self.storeBSTNodes(root.right, nodes)

    def buildTreeUtil(self, nodes, start, end):
        # base case
        if start > end:
            return None

        # Get the middle element and make it root
        mid = (start + end) // 2
        node = nodes[mid]

        # Using index in Inorder traversal, construct left and right subtress
        node.left = self.buildTreeUtil(nodes, start, mid - 1)
        node.right = self.buildTreeUtil(nodes, mid + 1, end)

        return node

    def rebalance(self, root):
        # Store nodes of given tree in sorted order
        nodes = []
        self.storeBSTNodes(root, nodes)

        # Constucts AVL Tree
        n = len(nodes)
        return self.buildTreeUtil(nodes, 0, n - 1)

    def insert(self, root, key):
        if not root:
            return Node(key)
        elif key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        balance = self.getBalance(root)

        if balance > 1 and key < root.left.key:
            return self.rightRotate(root)

        if balance < -1 and key > root.right.key:
            return self.leftRotate(root)

        if balance > 1 and key > root.left.key:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)

        if balance < -1 and key < root.right.key:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def minkeyueNode(self, root):
        current = root
        while current.left is not None:
            current = current.left
        return current

    def delete(self, root, key):
        if not root:
            return root
        elif key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            temp = self.minkeyueNode(root.right)
            root.key = temp.key
            root.right = self.delete(root.right, temp.key)
        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))
        balance = self.getBalance(root)
        if balance > 1 and self.getBalance(root.left) >= 0:
            return self.rightRotate(root)
        if balance < -1 and self.getBalance(root.right) <= 0:
            return self.leftRotate(root)
        if balance > 1 and self.getBalance(root.left) < 0:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)
        if balance < -1 and self.getBalance(root.right) > 0:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)
        return root

    def leftRotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.getHeight(z.left),
                           self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))
        return y

    def rightRotate(self, y):
        x = y.left
        T3 = x.right
        x.right = y
        y.left = T3
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))
        x.height = 1 + max(self.getHeight(x.left),
                           self.getHeight(x.right))
        return x

    def getHeight(self, root):
        if not root:
            return 0
        return root.height

    def getBalance(self, root):
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)

    def preOrder(self, root):
        if not root:
            return
        print("{0} ".format(root.key), end="")
        self.preOrder(root.left)
        self.preOrder(root.right)
    
    def minValueNode(self, root):
        current = root
        while current.left is not None:
            current = current.left
        return current

    def maxValueNode(self, root):
        current = root
        while current.right is not None:
            current = current.right
        return current
    
    def inOrder(self, root):
        if root:
            self.inOrder(root.left)
            print(root.key, end=" ")
            self.inOrder(root.right)

    def findMedian(self, root):
        if root is None:
            return None
        nodes = []
        self.inOrderToList(root, nodes)
        n = len(nodes)
        if n % 2 == 1:
            return nodes[n//2]
        else:
            return (nodes[n//2 - 1] + nodes[n//2]) / 2

    def inOrderToList(self, root, nodes=[]):
        if root:
            self.inOrderToList(root.left, nodes)
            nodes.append(root.key)
            self.inOrderToList(root.right, nodes)
    def postOrder(self, root):
        if root:
            self.postOrder(root.left)
            self.postOrder(root.right)
            print(root.key, end=" ")

    def preOrder(self, root):
        if root:
            print(root.key, end=" ")
            self.preOrder(root.left)
            self.preOrder(root.right)


class BST:
    def insert(self, node, key):
        if node is None:
            return Node(key)
        else:
            if node.key < key:
                node.right = self.insert(node.right, key)
            else:
                node.left = self.insert(node.left, key)
        return node

    def inorder(self, root):
        if root:
            self.inorder(root.left)
            print(root.key)
            self.inorder(root.right)

    def minkeyueNode(self, node):
        current = node
        while(current.left is not None):
            current = current.left
        return current

    def delete(self, root, key):
        if root is None:
            return root
        if key < root.key:
            root.left = self.delete(root.left, key)
        elif(key > root.key):
            root.right = self.delete(root.right, key)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            temp = self.minkeyueNode(root.right)
            root.key = temp.key
            root.right = self.delete(root.right, temp.key)
        return root
    def minValueNode(self, root):
        current = root
        while(current.left is not None):
            current = current.left
        return current

    def maxValueNode(self, root):
        current = root
        while(current.right is not None):
            current = current.right
        return current

    def inOrder(self, root):
        if root:
            self.inOrder(root.left)
            print(root.key, end=" ")
            self.inOrder(root.right)

    def findMedian(self, root):
        if root is None:
            return None
        nodes = []
        self.inOrderToList(root, nodes)
        n = len(nodes)
        if n % 2 == 1:
            return nodes[n//2]
        else:
            return (nodes[n//2 - 1] + nodes[n//2]) / 2

    def inOrderToList(self, root, nodes=[]):
        if root:
            self.inOrderToList(root.left, nodes)
            nodes.append(root.key)
            self.inOrderToList(root.right, nodes)

    def postOrder(self, root):
        if root:
            self.postOrder(root.left)
            self.postOrder(root.right)
            print(root.key, end=" ")

    def preOrder(self, root):
        if root:
            print(root.key, end=" ")
            self.preOrder(root.left)
            self.preOrder(root.right)
def main():
    avl_tree = AVLTree()
    bst_tree = BST()
    avl_root = None
    bst_root = None

    while True:
        command = input('command> ')
        if command == 'Help':
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
        if command == 'Exit':
            break
        elif command == 'Print':
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
        elif command == "Tickz":
            print("AVL tree has been saved to a txt file:")
            writeTikzToFile('tickzpictureAVL.txt', tikz_tree(avl_root))
            print("BST tree: has been saved to a txt file:")
            writeTikzToFile('tickzpictureBST.txt', tikz_tree(bst_root))
        elif command == 'Insert':
            num_nodes = int(input('nodes> '))
            keys = list(map(int, input('insert> ').split()))
            for key in keys:
                avl_root = avl_tree.insert(avl_root, key)
                bst_root = bst_tree.insert(bst_root, key)
        elif command == 'Delete':
            avl_root = None
            bst_root = None
            print("Trees have been cleared.")
        elif command == 'Rebalance':
            avl_root = avl_tree.rebalance(avl_root)
            print("AVL tree has been rebalanced.")
        elif command == 'Remove':
            keys = list(map(int, input('remove> ').split()))
            for key in keys:
                avl_root = avl_tree.delete(avl_root, key)
                bst_root = bst_tree.delete(bst_root, key)
        elif command == 'FindMinMax':
            avl_min = avl_tree.minValueNode(avl_root).key
            avl_max = avl_tree.maxValueNode(avl_root).key
            bst_min = bst_tree.minValueNode(bst_root).key
            bst_max = bst_tree.maxValueNode(bst_root).key
            print(f"AVL tree: Min = {avl_min}, Max = {avl_max}")
            print(f"BST tree: Min = {bst_min}, Max = {bst_max}")
        elif command == 'SortAndMedian':
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