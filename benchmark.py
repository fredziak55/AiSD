import time
import bst
import avl
import os

import sys

sys.setrecursionlimit(10000)  # Increase the recursion limit to 3000

avl_tree = avl.AVLTree()
bst_tree = bst.BST()
avl_root = None
bst_root = None

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
CURRENT_DIR = os.path.dirname(__file__)

def readFromFile(filename):
    with open(os.path.join(DATA_DIR, filename), 'r') as file:
        content = file.read()
        return content
        
def benchmark(func, num_runs=4):
    total_time = 0
    for _ in range(num_runs):
        start_time = time.time()
        func()
        end_time = time.time()
        elapsed_time = end_time - start_time
        total_time += elapsed_time
    average_time = total_time / num_runs
    average_time_str = "{:.10f}".format(average_time)
    return average_time_str

def benchmarkAfterInserting(func, tree, root, filename, num_runs=4):
    keys = list(map(int, readFromFile(filename).split()))
    for key in keys:
        root = tree.insert(root, key)
    total_time = 0
    for _ in range(num_runs):
        start_time = time.time()
        func(tree, root)
        end_time = time.time()
        elapsed_time = end_time - start_time
        total_time += elapsed_time
    average_time = total_time / num_runs
    average_time_str = "{:.10f}".format(average_time)
    return average_time_str
    
def makeTree(tree, root, filename):
    keys = list(map(int, readFromFile(filename).split()))
    for key in keys:
        root = tree.insert(root, key)
def minMax(tree, root, filename=None):
    tree.minValueNode(root).key
    tree.maxValueNode(root).key
def inOrder(tree, root, filename=None):
    tree.inOrder(root)
def rebalance(tree, root, filename=None):
    tree.rebalance(root)

def iterateBenchmark(array, tree_name, tree, root, func, func_name, benchmark_type):
    with open (os.path.join(CURRENT_DIR, f"result_{tree_name}_{array}_{func_name}.txt"), 'w') as f:
        for i in range(5, 14):
            filename = f'{array}_{2**i}.txt'
            if benchmark_type == benchmark:
                time = benchmark_type(lambda: func(tree, root, filename))
            else:
                time = benchmark_type(func, tree, root, filename)
            f.write(f"{tree_name} {2**i} {time} seconds\n")

def main():
    arrays = ['random_array', 'degenerate_array']
    benchmarksTypes = [makeTree, minMax, inOrder, rebalance]
     
    for array in arrays:
        for benchmarksType in benchmarksTypes:
            if benchmarksType == makeTree:
                iterateBenchmark(array, "BST", bst_tree, bst_root, benchmarksType, benchmarksType.__name__, benchmark)
                iterateBenchmark(array, "AVL", avl_tree, avl_root, benchmarksType, benchmarksType.__name__, benchmark)
            else:
                iterateBenchmark(array, "BST", bst_tree, bst_root, benchmarksType, benchmarksType.__name__, benchmarkAfterInserting)
                iterateBenchmark(array, "AVL", avl_tree, avl_root, benchmarksType, benchmarksType.__name__, benchmarkAfterInserting)
main()