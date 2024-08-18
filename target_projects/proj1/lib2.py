import numpy as np

# Bubble Sort Algorithm
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# selection_sort Algorithm
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_index = i
        for j in range(i+1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr

# Python inbuilt sort for numpy array
def python_sort(arr):
    arr.sort()
    return arr

# Generate a random list
def generate_random_list(power_of_ten):
    arr =  np.random.randint(1, 100000, 10**power_of_ten)
    return arr