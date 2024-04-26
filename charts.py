import matplotlib.pyplot as plt
import os
import numpy as np

arrays = ['random_array', 'degenerate_array']
benchmarksTypes = ['makeTree', 'minMax', 'inOrder', 'rebalance']

CURRENT_DIR = os.path.dirname(__file__)

for array in arrays:
    for benchmark in benchmarksTypes:
        avl_file_path = os.path.join(CURRENT_DIR, f'result_AVL_{array}_{benchmark}.txt')
        bst_file_path = os.path.join(CURRENT_DIR, f'result_BST_{array}_{benchmark}.txt')
        avl_data = np.loadtxt(avl_file_path, usecols=2)
        bst_data = np.loadtxt(bst_file_path, usecols=2)
        data3 = np.loadtxt(bst_file_path, usecols=1)

        # Define your data
        bst_times = bst_data  # replace with your BST times
        avl_times = avl_data # replace with your AVL times
        x_values = data3  # replace with your x values (e.g., array sizes or method names)

        # Create a new figure and axes
        fig, ax = plt.subplots()

        # Plot the BST and AVL times
        ax.plot(x_values, bst_times, label='BST')
        ax.plot(x_values, avl_times, label='AVL')

        # Set the labels for the x-axis and y-axis
        ax.set_xlabel('Array Size / Method')
        ax.set_ylabel('Time')

        # Add a legend
        ax.legend()

        # Save the figure to an SVG file
        fig.savefig(os.path.join(CURRENT_DIR, f'charts/{array}_{benchmark}.svg'))