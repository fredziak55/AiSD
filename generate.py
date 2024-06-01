import os
import random

def generate_knapsack_file(filename, num_items, capacity):
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Join the current directory with the filename
    file_path = os.path.join(current_dir, filename)

    with open(file_path, 'w') as f:
        f.write(f"{capacity}\n")
        f.write(f"{num_items}\n")
        for _ in range(num_items):
            value = random.randint(0, 100)
            weight = random.randint(0, 100)
            f.write(f"{value}, {weight}\n")

# Generate files with constant capacity and varying number of items
for num_items in range(1, 27, 5):
    filename = f'knapsack_{num_items}_items.txt'
    generate_knapsack_file(filename, num_items, 25)

# Generate files with constant number of items and varying capacity
for capacity in range(1, 27, 5):
    filename = f'knapsack_{capacity}_capacity.txt'
    generate_knapsack_file(filename, 25, capacity)