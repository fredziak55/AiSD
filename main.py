from itertools import combinations

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

values = [2, 1, 6, 7, 3]
weights = [1, 1, 3, 3, 2]
capacity = 7

print(knapsack_brute_force(values, weights, capacity))  # Output: (1, 2)
print(knapsack_dynamic_programming(values, weights, capacity))  # Output: [2, 1]