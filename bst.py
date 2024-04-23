class Node:
    def __init__(self, key):
        # Initialize a new node with the given key
        self.key = key
        # Set the left and right children to None
        self.left = None
        self.right = None
        # Set the height of the node to 1
        self.height = 1
        
class BST:
    def insert(self, node, key):
        # If the tree is empty, create a new node with the given key
        if node is None:
            return Node(key)
        else:
            # If the given key is greater than the node's key, insert the key in the right subtree
            if node.key < key:
                node.right = self.insert(node.right, key)
            # Otherwise, insert the key in the left subtree
            else:
                node.left = self.insert(node.left, key)
        # Return the node
        return node

    def inorder(self, root):
        # If the tree is not empty
        if root:
            # Recursively call inorder on the left subtree
            self.inorder(root.left)
            # Print the root's key
            print(root.key)
            # Recursively call inorder on the right subtree
            self.inorder(root.right)

    def minkeyueNode(self, node):
        # Start at the given node
        current = node
        # Traverse the left subtree until the leftmost node is found
        while(current.left is not None):
            current = current.left
        # Return the leftmost node (which has the minimum key)
        return current

    def delete(self, root, key):
        # If the tree is empty, return None
        if root is None:
            return root
        # If the key to be deleted is smaller than the root's key, then it lies in left subtree
        if key < root.key:
            root.left = self.delete(root.left, key)
        # If the key to be deleted is greater than the root's key, then it lies in right subtree
        elif(key > root.key):
            root.right = self.delete(root.right, key)
        # If key is same as root's key, then this is the node to be deleted
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
            # Node with two children: Get the inorder successor (smallest in the right subtree)
            temp = self.minkeyueNode(root.right)
            # Copy the inorder successor's content to this node
            root.key = temp.key
            # Delete the inorder successor
            root.right = self.delete(root.right, temp.key)
        return root
    
    def minValueNode(self, root):
      # Start at the given root
      current = root
      # Traverse the left subtree until the leftmost node is found
      while(current.left is not None):
        current = current.left
      # Return the leftmost node (which has the minimum key)
      return current

    def maxValueNode(self, root):
        # Start at the given root
        current = root
        # Traverse the right subtree until the rightmost node is found
        while(current.right is not None):
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

    def to_sorted_array(self, root, arr=None):
        # If arr is None, initialize an empty array
        if arr is None:
            arr = []
        # If the tree is not empty
        if root:
            # Recursively call to_sorted_array on the left subtree
            self.to_sorted_array(root.left, arr)
            # Append the root's key to the array
            arr.append(root.key)
            # Recursively call to_sorted_array on the right subtree
            self.to_sorted_array(root.right, arr)
        # Return the array
        return arr

    def sorted_array_to_bst(self, arr):
        # Base case: if the array is empty, return None
        if not arr:
            return None
        # Find the middle element of the array
        mid = len(arr) // 2
        # Create a new node with the middle element
        root = Node(arr[mid])
        # Recursively construct the left subtree from the elements before the middle element
        root.left = self.sorted_array_to_bst(arr[:mid])
        # Recursively construct the right subtree from the elements after the middle element
        root.right = self.sorted_array_to_bst(arr[mid+1:])
        # Return the root of the constructed BST
        return root

    def rebalance(self, root):
        # Convert the BST to a sorted array
        sorted_array = self.to_sorted_array(root)
        # Convert the sorted array back to a balanced BST and return the root of the new BST
        return self.sorted_array_to_bst(sorted_array)