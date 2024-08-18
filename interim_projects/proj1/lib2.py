import logging
logging.basicConfig(filename='../function_logs/proj1.log', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
import numpy as np

# Bubble Sort Algorithm

def bubble_sort(arr):
    logging.info('<START13634>')
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    logging.info('<END13634>')
    return arr

# selection_sort Algorithm

def selection_sort(arr):
    logging.info('<START19055>')
    n = len(arr)
    for i in range(n):
        min_index = i
        for j in range(i+1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
    logging.info('<END19055>')
    return arr

# Python inbuilt sort for numpy array

def python_sort(arr):
    logging.info('<START4247>')
    arr.sort()
    logging.info('<END4247>')
    return arr

# Generate a random list

def generate_random_list(power_of_ten):
    logging.info('<START9412>')
    arr =  np.random.randint(1, 100000, 10**power_of_ten)
    logging.info('<END9412>')
    return arr
