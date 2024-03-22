import sys
import random
#algorithms 
def insertionSort(tab):
    tempTab = []
    tempTab.append(tab[0])

    for i in range(1, len(tab)):
        tempNumber = tab[i] #wybrany element
        x = i - 1 #iteracje pod pozostałe elementy

        while(x >= 0 and tempNumber < tab[x]): #dopóki nie ma mniejszego miejsca od wybranego i nie jesteśmy na początku tablicy
            tab[x+1] = tab[x]
            x -= 1
        tab[x + 1] = tempNumber #zamiana elementu
    return tab

def selectionSort(tab):
    for i in range (len(tab)):
        for j in range(i, len(tab)):
            temp = tab.index(min(tab[i:len(tab)])) #sprawdzanie indexu od min dla danego zakresu
            tab[i], tab[temp] = tab[temp], tab[i] #zamiana
            break
    return tab

# def sadgewickShellSort(arr):
#     # Define Sedgewick's increment sequence
#   increments = [1, 8, 23, 77, 281, 1073, 4193, 16577]

#   # Iterate through each increment in the sequence
#   for gap in increments:
#     # For each element in the arr
#     for i in range(gap, len(arr)):
#       # Store the current element
#       temp = arr[i]
#       j = i

#       # Shift elements greater than the current element by the gap
#       while j >= gap and arr[j - gap] > temp:
#         arr[j] = arr[j - gap]
#         j -= gap

#       # Insert the current element in its correct position
#       arr[j] = temp

#   return arr

def sadgewickShellSort(arr):
    # Generate the gap sequence
    gaps = [1]
    k = 1
    while True:
        gap = 4**k + 3 * 2**(k-1) + 1
        if gap > len(arr):
            break
        if gap < len(arr):
            gaps.append(gap)
        k += 1
    gaps.sort()
    print(gaps)

    # Perform the shell sort
    for gap in reversed(gaps):
        for i in range(gap, len(arr)):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp

    return arr

sys.setrecursionlimit(15000000)
# def quickSortLeft(arr):
#     # Base case: Empty or single element list
#     if len(arr) <= 1:
#         return arr

#     # Choose the first element (leftmost) as the pivot
#     pivot = arr[0]

#     # Initialize empty lists for elements less, equal and greater than the pivot
#     left = []
#     equal = []
#     right = []

#     # Partition the arr
#     for element in arr:
#         if element < pivot:
#             left.append(element)
#         elif element == pivot:
#             equal.append(element)
#         else:
#             right.append(element)

#     # Recursively sort the left and right subarrays
#     return quickSortLeft(left) + equal + quickSortLeft(right)

def quickSortLeft(arr):
    # Create an auxiliary stack
    size = len(arr)
    stack = [0] * (size)

    # Initialize top of stack
    top = -1

    # Push initial values in the stack
    top += 1
    stack[top] = 0
    top += 1
    stack[top] = size - 1

    # Keep popping elements until stack is not empty
    while top >= 0:

        # Pop high and low
        high = stack[top]
        top -= 1
        low = stack[top]
        top -= 1

        # Set pivot element at its correct position in sorted array
        pivot = arr[low]
        i = low - 1
        j = high + 1

        while True:
            i += 1
            while arr[i] < pivot:
                i += 1
            j -= 1
            while arr[j] > pivot:
                j -= 1
            if i >= j:
                break
            arr[i], arr[j] = arr[j], arr[i]

        # If there are elements on the left side of pivot, then push left side to stack
        if j > low:
            top += 1
            stack[top] = low
            top += 1
            stack[top] = j

        # If there are elements on the right side of pivot, then push right side to stack
        if high > j + 1:
            top += 1
            stack[top] = j + 1
            top += 1
            stack[top] = high

    return arr

def quickSortRandom(arr):
     # Check if the list is empty or has only one element (already sorted)
  if len(arr) <= 1:
    return arr

  # Choose a random pivot element
  pivot_index = random.randrange(len(arr))
  pivot = arr[pivot_index]

  # Partition the arr around the pivot
  left, right = [], []
  for element in arr:
    if element < pivot:
      left.append(element)
    elif element > pivot:
      right.append(element)

  # Sort the left and right sub-arrays recursively
  sorted_left = quickSortRandom(left)
  sorted_right = quickSortRandom(right)

  # Combine the sorted sub-arrays with the pivot in the middle
  return sorted_left + [pivot] + sorted_right

def heapify(arr, n, i):
  """
  Max heapify a subtree rooted with node i which is
  assumed to be a min heap already
  """
  largest = i  # Initialize largest as root
  l = 2 * i + 1  # left = 2*i + 1
  r = 2 * i + 2  # right = 2*i + 2

  # See if left child is larger than root
  if l < n and arr[i] < arr[l]:
    largest = l

  # See if right child is larger than largest so far
  if r < n and arr[largest] < arr[r]:
    largest = r

  # If largest is not root
  if largest != i:
    arr[i], arr[largest] = arr[largest], arr[i]  # swap
    # Recursively heapify the affected sub-tree
    heapify(arr, n, largest)

def heapSort(arr):
    """
    In-place heap sort
    """
    n = len(arr)

    # Build a max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # One by one extract an element from heap
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # swap
        heapify(arr, i, 0)
    return arr

algorithmsNames = {
    1: "Insertion sort",
    2: "Sedgewick shell sort",
    3: "Selection sort",
    4: "Heap sort",
    5: "Quick sort (left pivot)",
    6: "Quick sort (random pivot)"
}

alogrithmsFuncs = {
    1: insertionSort,
    2: sadgewickShellSort,
    3: selectionSort,
    4: heapSort,
    5: quickSortLeft,
    6: quickSortRandom
}

def sort_using_algorithm(data, algorithm):
    # This function takes the algorithm identifier as input
    # However, it always uses the sorted function in Python
    sorted_data = alogrithmsFuncs[algorithm](data)
    return sorted_data

def main():
    # Command-line arguments: python script.py --algorithm <algorithm_number>
    if len(sys.argv) != 3 or sys.argv[1] != "--algorithm":
        print("Usage: python script.py --algorithm <algorithm_number>")
        sys.exit(1)

    algorithm_number = int(sys.argv[2])

    # Read input data from standard input until the end of file (EOF)
    input=sys.stdin.read().split()
    try:
        data = [int(x) for x in input[1:]]
    except EOFError:
        print("Error reading input.")

    # Perform sorting using the specified algorithm (ignored in this example)
    sorted_data = sort_using_algorithm(data, algorithm_number)

    # Print the sorted data
    print("Sorted data:", sorted_data)
    # print("Sorted using:", algorithmsNames[algorithm_number])

if __name__ == "__main__":
    main()
