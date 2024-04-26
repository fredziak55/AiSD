class Node:
    def __init__(self, key):
        # Initialize a new node with the given key
        self.key = key
        # Set the left and right children to None
        self.left = None
        self.right = None
        # Set the height of the node to 1
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

    # Function to insert a key in the AVL tree
    def insert(self, root, key):
        # If the tree is empty, return a new node
        if not root:
            return Node(key)
        # If the key to be inserted is smaller than the root's key, then it goes to the left of the tree
        elif key < root.key:
            root.left = self.insert(root.left, key)
        # If the key to be inserted is greater than the root's key, then it goes to the right of the tree
        else:
            root.right = self.insert(root.right, key)

        # Update the height of the ancestor node
        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))

        # Get the balance factor to check whether this node became unbalanced
        balance = self.getBalance(root)

        # If the node is unbalanced, then there are 4 cases to handle

        # Case 1 - Left Left
        if balance > 1 and key < root.left.key:
            return self.rightRotate(root)

        # Case 2 - Right Right
        if balance < -1 and key > root.right.key:
            return self.leftRotate(root)

        # Case 3 - Left Right
        if balance > 1 and key > root.left.key:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)

        # Case 4 - Right Left
        if balance < -1 and key < root.right.key:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

     # Function to find the node with minimum key value, its always located at leftmost leaf
    def minkeyueNode(self, root):
        current = root
        # Loop down to find the leftmost leaf
        while current.left is not None:
            current = current.left
        return current

    # Function to delete a key from the tree
    def delete(self, root, key):
        # If the tree is empty, return it
        if not root:
            return root
        # If the key to be deleted is smaller than the root's key, then it lies in left subtree
        elif key < root.key:
            root.left = self.delete(root.left, key)
        # If the key to be deleted is greater than the root's key, then it lies in right subtree
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            # Node with only one child or no child
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            # Node with two children, get the inorder successor (smallest in the right subtree)
            temp = self.minkeyueNode(root.right)
            # Copy the inorder successor's content to this node
            root.key = temp.key
            # Delete the inorder successor
            root.right = self.delete(root.right, temp.key)

        # Update the height of the ancestor node
        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))

        # Get the balance factor to check whether this node became unbalanced
        balance = self.getBalance(root)

        # If the node is unbalanced, then there are 4 cases to handle

        # Case 1 - Left Left
        if balance > 1 and self.getBalance(root.left) >= 0:
            return self.rightRotate(root)

        # Case 2 - Right Right
        if balance < -1 and self.getBalance(root.right) <= 0:
            return self.leftRotate(root)

        # Case 3 - Left Right
        if balance > 1 and self.getBalance(root.left) < 0:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)

        # Case 4 - Right Left
        if balance < -1 and self.getBalance(root.right) > 0:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def leftRotate(self, x):
        if x is None:
            return None
        y = x.right
        T2 = y.left if y else None
        # Perform rotation
        if y:
            y.left = x
        x.right = T2
        # Update heights
        x.height = 1 + max(self.getHeight(x.left), self.getHeight(x.right))
        if y:
            y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))
        # Return the new root
        return y

    def rightRotate(self, y):
        if y is None:
            return None
        x = y.left
        T2 = x.right if x else None
        # Perform rotation
        if x:
            x.right = y
        y.left = T2
        # Update heights
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))
        if x:
            x.height = 1 + max(self.getHeight(x.left), self.getHeight(x.right))
        # Return the new root
        return x

    def getHeight(self, root):
        # If the tree is empty, return 0
        if not root:
            return 0

        # Otherwise, return the height of the root
        return root.height

    def getBalance(self, root):
        # If the tree is empty, return 0
        if not root:
            return 0

        # Otherwise, return the difference between the heights of the left and right subtrees
        return self.getHeight(root.left) - self.getHeight(root.right)

    def preOrder(self, root):
        # If the tree is not empty
        if not root:
            return
        # Print the root's key
        print("{0} ".format(root.key), end="")
        # Recursively call preOrder on the left subtree
        self.preOrder(root.left)
        # Recursively call preOrder on the right subtree
        self.preOrder(root.right)
    
    def minValueNode(self, root):
        # Start at the given root
        current = root
        # Traverse the left subtree until the leftmost node is found
        while current.left is not None:
            current = current.left
        # Return the leftmost node (which has the minimum key)
        return current

    def maxValueNode(self, root):
        # Start at the given root
        current = root
        # Traverse the right subtree until the rightmost node is found
        while current.right is not None:
            current = current.right
        # Return the rightmost node (which has the maximum key)
        return current
    
    def inOrder(self, root):
        # If the tree is not empty
        if root:
            # Recursively call inOrder on the left subtree
            self.inOrder(root.left)
            # Print the root's key
            print(root.key, end=" ")
            # Recursively call inOrder on the right subtree
            self.inOrder(root.right)

    def findMedian(self, root):
        # If the tree is empty, return None
        if root is None:
            return None
        # Initialize an empty list to store the nodes
        nodes = []
        # Fill the list with the keys of the nodes in in-order traversal
        self.inOrderToList(root, nodes)
        # Find the number of nodes
        n = len(nodes)
        # If the number of nodes is odd, return the middle node
        if n % 2 == 1:
            return nodes[n//2]
        # If the number of nodes is even, return the average of the two middle nodes
        else:
            return (nodes[n//2 - 1] + nodes[n//2]) / 2

    def inOrderToList(self, root, nodes=[]):
        # If the tree is not empty
        if root:
            # Recursively call inOrderToList on the left subtree
            self.inOrderToList(root.left, nodes)
            # Add the root's key to the list
            nodes.append(root.key)
            # Recursively call inOrderToList on the right subtree
            self.inOrderToList(root.right, nodes)

    def postOrder(self, root):
        # If the tree is not empty
        if root:
            # Recursively call postOrder on the left subtree
            self.postOrder(root.left)
            # Recursively call postOrder on the right subtree
            self.postOrder(root.right)
            # Print the root's key
            print("{0} ".format(root.key), end="")

    def preOrder(self, root):
        # If the tree is not empty
        if root:
            # Print the root's key
            print("{0} ".format(root.key), end="")
            # Recursively call preOrder on the left subtree
            self.preOrder(root.left)
            # Recursively call preOrder on the right subtree
            self.preOrder(root.right)