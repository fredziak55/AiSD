import random
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

def generateRandomArrays():
    # Loop over the sizes from 2^5 to 2^10
    for i in range(5, 17):
        # Generate a random array of the current size
        arr = [random.randint(0, 10000) for _ in range(2**i)]
        # Convert the array to a string with space-separated numbers
        arr_str = ' '.join(map(str, arr))
        # Create a filename indicating the size of the array
        filename = f'random_array_{2**i}.txt'
        # Open the output file in write mode
        with open(os.path.join(DATA_DIR, filename), 'w') as f:
            # Write the string to the file
            f.write(arr_str)

def generateDegenarateArrays():
    for i in range(5, 17):
        # Generate a random array of the current size
        arr = list(range(2**i))
        # Convert the array to a string with space-separated numbers
        arr_str = ' '.join(map(str, arr))
        # Create a filename indicating the size of the array
        filename = f'degenarate_array_{2**i}.txt'
        # Open the output file in write mode
        with open(os.path.join(DATA_DIR, filename), 'w') as f:
            # Write the string to the file
            f.write(arr_str)

# Call the function
generateRandomArrays()