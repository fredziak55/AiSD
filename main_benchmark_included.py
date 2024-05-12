import os
import argparse
import numpy as np
import sys
import networkx as nx
import random
import matplotlib.pyplot as plt
import time
import glob

sys.setrecursionlimit(10000)

parser = argparse.ArgumentParser()
parser.add_argument("-generate", action="store_true", help="Generate a directed acyclic graph")
parser.add_argument("-user-provided", action="store_true", help="Create a graph from user-provided input")
args = parser.parse_args()

CURRENT_DIR = os.path.dirname(__file__)

def export_graph_to_tikz(graph, filename):
    if not filename.endswith('.tex'):
        filename += '.tex'
    G = nx.from_numpy_array(graph)
    num_nodes = len(G.nodes())
    if num_nodes > 75:
        scale = 10
    elif num_nodes > 50:
        scale = 5
    elif num_nodes > 20:
        scale = 3
    else:
        scale = 2
    pos = nx.spring_layout(G, seed=42, k=2, scale=scale)
    with open(filename, 'w') as f:
        f.write("\\documentclass{standalone}\n")
        f.write("\\usepackage{tikz}\n")
        f.write("\\usetikzlibrary{arrows.meta}\n")
        f.write("\\begin{document}\n")
        f.write("\\begin{tikzpicture}\n")
        f.write("\\begin{scope}[every node/.style={fill=red!60,circle,inner sep=1pt}]\n")
        scale_factor = 50
        for node, coordinates in pos.items():
            f.write(f"\\node[draw, circle] (v{node+1}) at ({coordinates[0]},{coordinates[1]}) {{{node+1}}};\n")
        f.write("\\end{scope}\n")
        f.write("\\begin{scope}[>={Stealth[black]}]\n")
        for i, j in G.edges():
            f.write(f"\\draw[->] (v{i+1}) -- (v{j+1});\n")
        f.write("\\end{scope}\n")
        f.write("\\end{tikzpicture}\n")
        f.write("\\end{document}\n")

def topological_sort_kahn(graph):
    in_degree = [0] * len(graph)
    for node in graph:
        for neighbor, edge_exists in enumerate(node):
            if edge_exists:
                in_degree[neighbor] += 1
    queue = [i+1 for i, degree in enumerate(in_degree) if degree == 0]
    topological_order = []
    while queue:
        node = queue.pop(0)
        topological_order.append(node)
        for i, edge_exists in enumerate(graph[node-1]):
            if edge_exists:
                in_degree[i] -= 1
                if in_degree[i] == 0:
                    queue.append(i+1)
    if len(topological_order) == len(graph):
        return topological_order
    else:
        return "The graph is not a DAG."
    
def topological_sort_tarjan(graph):
    visited = [False] * len(graph)
    stack = []
    for node in range(len(graph)):
        if not visited[node]:
            if not tarjan_dfs(graph, node, visited, stack):
                return "The graph is not a DAG."
    return stack[::-1]

def tarjan_dfs(graph, node, visited, stack):
    visited[node] = True
    for i, neighbor in enumerate(graph[node]):
        if neighbor and not visited[i]:
            if not tarjan_dfs(graph, i, visited, stack):
                return False
    stack.append(node+1)
    return True

def find_edge(graph):
    try:
        from_node = int(input("from> "))
        to_node = int(input("to> "))
        if from_node < 1 or to_node < 1 or from_node > len(graph) or to_node > len(graph):
            print("Error: Invalid node number.")
            return
    except ValueError:
        print("Error: Invalid input. Please enter a number.")
        return
    if graph[from_node-1, to_node-1]:
        print(f"True: edge ({from_node},{to_node}) exists in the graph :)")
    else:
        print(f"False: edge ({from_node},{to_node}) does not exist in the graph ):")

def bfs(graph, start_node):
    visited = [False] * len(graph)
    queue = [start_node]
    while True:
        while queue:
            node = queue.pop(0)
            if not visited[node-1]:
                print(node, end=" ")
                visited[node-1] = True
                neighbors = [i+1 for i, value in enumerate(graph[node-1]) if value and not visited[i]]
                for neighbor in neighbors:
                    queue.append(neighbor)
        if all(visited):
            break
        for i, node_visited in enumerate(visited):
            if not node_visited:
                queue.append(i+1)
                break
    print()

def dfs(graph, start_node):
    visited = [False] * len(graph)
    stack = [start_node]
    while True:
        while stack:
            node = stack.pop()
            if not visited[node-1]:
                print(node, end=" ")
                visited[node-1] = True
                neighbors = [i+1 for i, value in enumerate(graph[node-1]) if value and not visited[i]]
                for neighbor in reversed(neighbors):
                    stack.append(neighbor)
        if all(visited):
            break
        for i, node_visited in enumerate(visited):
            if not node_visited:
                stack.append(i+1)
                break
    print()

def print_menu(graph):
    while True:
        print("Enter a command: ", end="")
        command = input()
        if command == 'help':
            print("--- Help ---")
            print("Commands:")
            print("Help - display this message")
            print("Quit - exit the program")
            print("Find - find an edge in the graph")
            print("BFS - perform a breadth-first search")
            print("DFS - perform a depth-first search")
            print("kahn - perform a topological sort using Kahn's algorithm")
            print("tarjan - perform a topological sort using Tarjan's algorithm")
            print("Tikz - save the graph to a LaTeX file")
            print("-------------")
            continue
        elif command == 'find':
            find_edge(graph)
        elif command in ['bfs', 'dfs']:
            try:
                start_node = int(input("Enter the start node for given search method: "))
                if start_node < 1 or start_node > len(graph):
                    print("Error: Invalid node number.")
                    continue
            except ValueError:
                print("Error: Invalid input. Please enter a number.")
                continue
            if command == 'bfs':
                bfs(graph, start_node)
            else:
                dfs(graph, start_node)
        elif command == 'kahn':
            result = topological_sort_kahn(graph)
            if isinstance(result, list):
                print("Topological order: ", end="")
                for node in result:
                    print(node, end=" ")
                print()
            else:
                print(result)
        elif command == 'tarjan':
            result = topological_sort_tarjan(graph)
            if isinstance(result, list):
                print("Topological order: ", end="")
                for node in result:
                    print(node, end=" ")
                print()
            else:
                print(result)
        elif command == 'tikz':
            filename = input("Enter the filename for the LaTeX file: ")
            export_graph_to_tikz(graph, filename)
        elif command == 'quit':
            break
        else:
            print("Invalid command. Enter 'help' for a list of commands.")

def generate_dag():
    try:
        nodes = int(input("Enter the number of nodes: "))
        if nodes < 1:
            print("Error: Number of nodes must be a positive integer.")
            return
        saturation = float(input("Enter the saturation (in percentage): "))
        if saturation < 0 or saturation > 100:
            print("Saturation must be between 0 and 100.")
            return
    except ValueError:
        print("Error: Invalid input. Please enter a number.")
        return
    saturation /= 100
    matrix = np.triu(np.random.choice([0, 1], size=(nodes, nodes), p=[1-saturation, saturation], replace=True))
    np.fill_diagonal(matrix, 0)
    return matrix

def print_graph_as_matrix(graph):
    print(graph)

def print_graph_as_list(graph):
    for i, row in enumerate(graph):
        print(f"Node {i+1} has edges to: ", end="")
        for j, value in enumerate(row):
            if value:
                print(j+1, end=" ")
        print()

def print_graph_as_table(graph):
    print("Source Node\tTarget Node")
    for i, row in enumerate(graph):
        for j, value in enumerate(row):
            if value:
                print(f"{i+1}\t\t{j+1}")

def user_provided_graph():
    try:
        nodes = int(input("Enter the number of nodes> "))
        if nodes < 1:
            print("Error: Number of nodes must be a positive integer.")
            return
    except ValueError:
        print("Error: Invalid input. Please enter a number.")
        return
    matrix = np.zeros((nodes, nodes))
    for i in range(nodes):
        successors = input(f"{i+1}> ").split()
        for successor in successors:
            if successor:
                try:
                    successor = int(successor)
                    if successor > nodes or successor < 1:
                        print(f"Error: Node {successor} does not exist.")
                        return
                    matrix[i, successor-1] = 1
                except ValueError:
                    print("Error: Invalid input. Please enter a number.")
                    return
    return matrix

representation = input("Enter how you want to view the graph (matrix, list, table): ")

if representation not in ['matrix', 'list', 'table', 'jailbreak']:
    print("Invalid representation. Please enter 'matrix', 'list', or 'table'.")
    sys.exit()

# -------------------------------------BENCHMARK--------------------------------------------

def generateRandomDAG():
    DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
    # Create the directory if it doesn't exist
    os.makedirs(DATA_DIR, exist_ok=True)
    for i in range(5, 14):
        # Generate a list of nodes for the current size
        nodes = list(range(2**i))
        # Randomly shuffle the nodes
        random.shuffle(nodes)
        # Create a filename indicating the size of the graph
        filename = f'random_dag_{2**i}.txt'
        # Open the output file in write mode
        with open(os.path.join(DATA_DIR, filename), 'w') as f:
            # For each node, create an edge to a random node that has a lower value
            for j in range(1, len(nodes)):
                # Choose a random node from the nodes with lower values
                lower_node = random.choice(nodes[:j])
                # Write the edge to the file
                f.write(f'{nodes[j]} {lower_node}\n')

def benchmark():
    DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
    files = glob.glob(os.path.join(DATA_DIR, 'random_dag_*.txt'))

     # Extract the number of nodes from the filename and sort the files based on it
    files = sorted(files, key=lambda f: int(f.split('_')[-1].split('.')[0]))

    for file in files:
        # Extract the size of the graph from the filename
        size = int(file.split('_')[-1].split('.')[0])
        print(f'Processing file: {file}, size: {size}')  # Debug print

        # Load the graph data
        with open(file, 'r') as f:
            edges = [tuple(map(int, line.split())) for line in f]

        # Create the graph in each representation
        matrix_graph = [[0]*size for _ in range(size)]
        list_graph = [[] for _ in range(size)]
        table_graph = [[] for _ in range(size)]  # Always create a list for each node

        for edge in edges:
            # Matrix representation
            matrix_graph[edge[0]][edge[1]] = 1

            # List representation
            list_graph[edge[0]].append(edge[1])

            # Table representation
            table_graph[edge[0]].append(edge[1])

        # Perform each operation on each representation and measure the time
        for operation, function in [('find_edge', None), ('sort_kahn', topological_sort_kahn), ('sort_tarjan', topological_sort_tarjan)]:
            for representation, graph in [('matrix', matrix_graph), ('list', list_graph), ('table', table_graph)]:
                start_time = time.time()
                if operation == 'find_edge':
                    # Generate a random edge
                    edge = (random.randint(0, size-1), random.randint(0, size-1))
                    # Search for the edge in the graph
                    if representation == 'matrix':
                        exists = graph[edge[0]][edge[1]] == 1
                    elif representation == 'list':
                        exists = edge[1] in graph[edge[0]]
                    elif representation == 'table':
                        exists = graph[edge[0]] is not None and edge[1] in graph[edge[0]]
                else:
                    function(graph)
                elapsed_time = time.time() - start_time

                # Write the results to a file
                with open(f'{operation}_benchmark.txt', 'a') as f:
                    f.write(f'{operation}, {representation}, {size}, {elapsed_time}\n')

def generate_graphs():
    operations = ['find_edge', 'sort_kahn', 'sort_tarjan']
    representations = ['matrix', 'list', 'table']

    for operation in operations:
        plt.figure(figsize=(10, 6))

        for representation in representations:
            x_values = []
            y_values = []

            with open(f'{operation}_benchmark.txt', 'r') as f:
                for line in f:
                    op, rep, size, time = line.strip().split(', ')
                    if rep == representation:
                        x_values.append(int(size))
                        y_values.append(float(time))

            plt.plot(x_values, y_values, label=representation)

        plt.xlabel('Number of Nodes')
        plt.ylabel('Time (seconds)')
        plt.title(f'{operation} Operation Time')
        plt.legend()
        plt.savefig(f'{operation}_benchmark.svg')
        plt.close()

# --------------------------------------------------------------------------------------------

if args.generate:
    graph = generate_dag()
elif args.user_provided:
    graph = user_provided_graph()
elif representation == 'jailbreak':
    graph = 'whatever'
    print("You've broken the jail. Now you have access to 'Humane Labs and Research. est 2013 Los Santos' SECRET LAB operations. We are after your ass. * ", end="")
    secret = input()
    if secret == 'generate':
        generateRandomDAG()
        print("Random DAG generated. Be careful. * * ")
    elif secret == 'benchmark':
        benchmark()
        print("Benchmarking complete. Be scared. * * * * ")
    elif secret == 'graph':
        generate_graphs()
        print("Graphs generated. By now, you've seen too much. There's no coming back. * * * * * * ")
    else:
        print("You can still go back.")
else:
    print("Please specify either -generate or -user-provided.")
    sys.exit()

if graph is not None:
    if representation == 'matrix':
        print_graph_as_matrix(graph)
    elif representation == 'list':
        print_graph_as_list(graph)
    elif representation == 'table':
        print_graph_as_table(graph)
    elif graph == 'whatever':
        print("Don't you dare.")
        sys.exit()
    print_menu(graph)