from itertools import combinations
import os
import time
import glob
import matplotlib.pyplot as plt
import glob
import time

def knapsack_brute_force(values, weights, capacity):
    best_value = 0
    best_combination = None

    # Generate all possible combinations of items
    for i in range(len(values) + 1):
        for combination in combinations(range(len(values)), i):
            # Calculate the total weight and value of this combination
            total_weight = sum(weights[j] for j in combination)
            total_value = sum(values[j] for j in combination)

            # If the total weight is within the capacity and the value is better than the best so far, update the best
            if total_weight <= capacity and total_value > best_value:
                best_value = total_value
                best_combination = combination

    return best_combination

def knapsack_dynamic_programming(values, weights, capacity):
    n = len(values)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(n + 1):
        for w in range(capacity + 1):
            if i == 0 or w == 0:
                dp[i][w] = 0
            elif weights[i-1] <= w:
                dp[i][w] = max(values[i-1] + dp[i-1][w-weights[i-1]], dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]

    # Backtrack to find the items included
    included = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            included.append(i-1)
            w -= weights[i-1]

    return included

def read_knapsack_file(filename):
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Join the current directory with the filename
    file_path = os.path.join(current_dir, filename)

    with open(file_path, 'r') as f:
        lines = f.readlines()

    capacity = int(lines[0].strip())
    num_items = int(lines[1].strip())

    values = []
    weights = []
    for line in lines[2:]:
        value, weight = map(int, line.split(','))
        values.append(value)
        weights.append(weight)

    return capacity, values, weights

def run_knapsack_algorithms(filename):
    capacity, values, weights = read_knapsack_file(filename)

    # Measure the time of the brute force algorithm
    start_time = time.time()
    brute_force_result = knapsack_brute_force(values, weights, capacity)
    end_time = time.time()
    brute_force_time = round(end_time - start_time, 50)
    # print(f"Brute force time: {round(end_time - start_time, 10)} seconds")

    # Measure the time of the dynamic programming algorithm
    start_time = time.time()
    dynamic_programming_result = knapsack_dynamic_programming(values, weights, capacity)
    end_time = time.time()
    # print(f"Dynamic programming time: {round(end_time - start_time, 10)} seconds")
    dynamic_programming_time = round(end_time - start_time, 50)

    return brute_force_time, dynamic_programming_time



def benchmark():
    # Get all .txt files in the current directory
    files = glob.glob('*.txt')
    print(f"Files found: {files}")
    
    # Run the algorithms on each file
    for file in files:
        print(f"Running algorithms on {file}...")
        brute_force_result, dynamic_programming_result = run_knapsack_algorithms(file)
        # print(f"Brute force result: {brute_force_result}")
        # print(f"Dynamic programming result: {dynamic_programming_result}")



def benchmark():
    # Get all .txt files in the current directory
    files = glob.glob('*.txt')

    # Lists to store the results
    constant_items_times_dynamic = []
    constant_capacity_times_dynamic = []
    constant_items_times_brute = []
    constant_capacity_times_brute = []

    # Run the algorithms on each file
    for file in files:
        brute_force_time, dynamic_programming_time = run_knapsack_algorithms(file)
        if 'capacity' in file:
            constant_items_times_dynamic.append(dynamic_programming_time)
            constant_items_times_brute.append(brute_force_time)
        elif 'items' in file:
            constant_capacity_times_dynamic.append(dynamic_programming_time)
            constant_capacity_times_brute.append(brute_force_time)
    print(constant_items_times_dynamic)
    print(constant_items_times_brute)
    print(constant_capacity_times_dynamic)
    print(constant_capacity_times_brute)
    
    # Create the graphs
    x_values = range(1, 27, 5)
    plt.figure()
    plt.plot(x_values, constant_items_times_dynamic)
    plt.title('Dynamic Programming Time with Constant Number of Items')
    plt.xlabel('Capacity')
    plt.ylabel('Time (seconds)')
    plt.savefig('constant_items_dynamic.png')

    plt.figure()
    plt.plot(x_values, constant_items_times_brute)
    plt.title('Brute Force Time with Constant Number of Items')
    plt.xlabel('Capacity')
    plt.ylabel('Time (seconds)')
    plt.savefig('constant_items_brute.png')

    plt.figure()
    plt.plot(x_values, constant_capacity_times_dynamic)
    plt.title('Dynamic Programming Time with Constant Capacity')
    plt.xlabel('Number of Items')
    plt.ylabel('Time (seconds)')
    plt.savefig('constant_capacity_dynamic.png')

    plt.figure()
    plt.plot(x_values, constant_capacity_times_brute)
    plt.title('Brute Force Time with Constant Capacity')
    plt.xlabel('Number of Items')
    plt.ylabel('Time (seconds)')
    plt.savefig('constant_capacity_brute.png')

# Run the benchmark
benchmark()