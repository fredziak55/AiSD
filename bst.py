class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1
        
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