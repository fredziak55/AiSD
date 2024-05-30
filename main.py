import os
import argparse
import numpy as np
import networkx as nx
import random
import matplotlib.pyplot as plt
import time

CURRENT_DIR = os.path.dirname(__file__)

# exporting graph to tikz
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

def create_graph(nodes, saturation):
    graph = np.zeros((nodes, nodes))
    for i in range(nodes):
        for j in range(i+1, nodes):
            if random.random() < saturation:
                graph[i][j] = graph[j][i] = 1
    return graph

def create_hamiltonian_cycle(graph, nodes):
    cycle = list(range(nodes))
    random.shuffle(cycle)
    for i in range(nodes):
        graph[cycle[i]][cycle[(i+1)%nodes]] = graph[cycle[(i+1)%nodes]][cycle[i]] = 1
    return graph

def create_non_hamiltonian_graph(nodes):
    return create_graph(nodes, 0.5)

def isolate_node(graph, node): # ensuring that the graph is not hamiltonian
    for i in range(len(graph)):
        graph[node][i] = 0
        graph[i][node] = 0
    return graph

def find_euler_cycle(graph): # finding eulerian cycle
    degrees = [sum(row) for row in graph]
    if any(degree % 2 != 0 for degree in degrees):
        return None 
    cycle = []
    stack = [0]
    while stack:
        vertex = stack[-1]
        if degrees[vertex]:
            for neighbor, edge in enumerate(graph[vertex]):
                if edge:
                    stack.append(neighbor)
                    graph[vertex][neighbor] = graph[neighbor][vertex] = 0
                    degrees[vertex] -= 1
                    degrees[neighbor] -= 1
                    break
            else:
                cycle.append(stack.pop())
        else:
            cycle.append(stack.pop())
    return cycle[::-1]

def is_valid(v, pos, path):
    if v >= len(graph):
        return False
    if graph[path[pos-1]][v] == 0 or v in path:
        return False
    return True
def hamilton_cycle_util(graph, path, pos):
    if pos == len(graph):
        return graph[path[pos-1]][path[0]] == 1
    for v in range(1, len(graph)):
        if pos < len(graph) and is_valid(v, pos, path):
            path[pos] = v
            if hamilton_cycle_util(graph, path, pos + 1):
                return True
            path[pos] = -1
    return False
def find_hamilton_cycle(graph): # finding hamiltonian cycle
    path = [-1] * len(graph)
    path[0] = 0
    if not hamilton_cycle_util(graph, path, 1):
        return None
    return path

def print_menu(graph):
    while True:
        print("Enter a command: ", end="")
        command = input()
        if command == 'help':
            print("--- Help ---")
            print("Commands:")
            print("Help - display this message")
            print("Quit - exit the program")
            print("Print - display the graph in matrix representation")
            print("Euler - find an Eulerian cycle in the graph")
            print("tikz - export the graph to a LaTeX file")
            print("-------------")
            continue
        elif command == 'quit':
            break
        elif command == 'print':
            print(graph)
        elif command == 'euler':
            cycle = find_euler_cycle(graph)
            if cycle is None:
                print("No Eulerian cycle exists.")
                break
            else:
                print("Eulerian cycle:", cycle)
                break
        elif command == 'hamilton':
            cycle = find_hamilton_cycle(graph)
            if cycle is None:
                print("No Hamiltonian cycle exists.")
                break
            else:
                print("Hamiltonian cycle:", cycle)
                break
        elif command == 'tikz':
            filename = input("Enter the filename for the LaTeX file: ")
            export_graph_to_tikz(graph, filename)
        else:
            print("Invalid command. Enter 'help' for a list of commands.")

def get_int_input(prompt): # security functions for input
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid number.")
def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")

# -------------------------------------BENCHMARK--------------------------------------------

def benchmark():
    hamilton_times = []
    non_hamilton_times = []

    # Create Hamiltonian graphs and measure times
    for nodes in range(10, 10001, 1000):
        graph = create_graph(nodes, 0.3)
        graph = create_hamiltonian_cycle(graph, nodes)
        start = time.time()
        find_euler_cycle(graph)
        find_hamilton_cycle(graph)
        end = time.time()
        hamilton_times.append(end - start)
        print(hamilton_times)

    # Create non-Hamiltonian graphs and measure times
    for nodes in range(20, 31):
        graph = create_graph(nodes, 0.5)
        graph = isolate_node(graph, 0)
        start = time.time()
        find_euler_cycle(graph)
        find_hamilton_cycle(graph)
        end = time.time()
        non_hamilton_times.append(end - start)
        print(non_hamilton_times)

    # Plot the results for Hamiltonian graphs
    plt.figure(figsize=(10, 6))
    plt.plot(range(10, 10001, 1000), hamilton_times, label='Hamiltonian')
    plt.xlabel('Number of nodes')
    plt.ylabel('Time (seconds)')
    plt.legend()
    plt.show()

    # Plot the results for non-Hamiltonian graphs
    plt.figure(figsize=(10, 6))
    plt.plot(range(20, 31), non_hamilton_times, label='Non-Hamiltonian')
    plt.xlabel('Number of nodes')
    plt.ylabel('Time (seconds)')
    plt.legend()
    plt.show()

# --------------------------------------------------------------------------------------------

parser = argparse.ArgumentParser() # graph choice
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--hamilton", action='store_true')
group.add_argument("--non-hamilton", action='store_true')
group.add_argument("--benchmark", action='store_true')
args = parser.parse_args()

graph = []

if args.hamilton:
    nodes = get_int_input("Enter the number of nodes for the Hamiltonian graph: ")
    while nodes < 10:
        print("The number of nodes must be at least 10.")
        nodes = get_int_input("Enter the number of nodes for the Hamiltonian graph: ")
    saturation = get_float_input("Enter the saturation for the Hamiltonian graph (30 or 70): ")
    while saturation not in [30, 70]:
        print("The saturation must be either 30% or 70%.")
        saturation = get_float_input("Enter the saturation for the Hamiltonian graph (30 or 70): ")
    saturation /= 100
    graph = create_graph(nodes, saturation)
    graph = create_hamiltonian_cycle(graph, nodes)
elif args.non_hamilton:
    nodes = get_int_input("Enter the number of nodes for the non-Hamiltonian graph: ")
    graph = create_non_hamiltonian_graph(nodes)
    isolate_node(graph, 0)
elif args.benchmark:
    benchmark()

print_menu(graph)