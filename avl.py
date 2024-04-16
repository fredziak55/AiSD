class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1
        
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