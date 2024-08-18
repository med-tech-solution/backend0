import numpy as np
import math
import argparse

def is_prime(n):
    if n <= 1:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def matrix_multiplication(size):
    A = np.random.rand(size, size)
    B = np.random.rand(size, size)
    result = np.matmul(A, B)
    return result

def sort_large_list(size):
    random_list = np.random.randint(1, 100000, size)
    return sorted(random_list)

def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

# Function 6: Numerical integration using the trapezoidal rule
def trapezoidal_integration(func, a, b, n):
    h = (b - a) / n
    result = (func(a) + func(b)) / 2
    for i in range(1, n):
        result += func(a + i * h)
    result *= h
    return result

class ExampleClass:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self):
        if isinstance(self.x, int) and isinstance(self.y, int):
            return self.x + self.y
        else:
            return None

    def multiply(self):
        return self.x * self.y

    def divide(self):
        return self.x / self.y

    def power(self):
        return self.x ** self.y

# Example usage of functions with increasing complexity
if __name__ == "__main__":
    # Retrieve all user parameters from command line
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--factorial', type=int, help='Factorial of n')
    parser.add_argument('--prime', type=int, help='Check if n is prime')
    parser.add_argument('--matrix', type=int, help='Size of matrix')
    parser.add_argument('--sort', type=int, help='Size of list to sort')
    parser.add_argument('--fibonacci', type=int, help='Calculate nth Fibonacci number')
    parser.add_argument('--integral', type=int, help='Number of intervals for trapezoidal integration')
    parser.add_argument('--example_param1', type=int, help='Example parameter 1')
    parser.add_argument('--example_param2', type=int, help='Example parameter 2')

    args = parser.parse_args()

    if args.factorial:
        print("Factorial of {}:".format(args.factorial), math.factorial(args.factorial))
    if args.prime:
        print("Is {} prime?".format(args.prime), is_prime(args.prime))

    if args.matrix:
        print("Matrix multiplication with size {}:".format(args.matrix))
        print(matrix_multiplication(args.matrix))

    if args.sort:
        print("Sorting list of size {}:".format(args.sort))
        print(sort_large_list(args.sort))

    if args.fibonacci:
        print("Fibonacci number for n={}".format(args.fibonacci), fibonacci(args.fibonacci))

    if args.integral:
        def func(x):
            return x ** 2
        print("Numerical integration from 0 to 10 with {} intervals:".format(args.integral))
        print(trapezoidal_integration(func, 0, 10, args.integral))

    # Example usage of ExampleClass

    # Create an instance of ExampleClass
    example_instance = ExampleClass(args.example_param1, args.example_param2)
    



# Sample usage:
# python prog1copy.py --factorial 10 --prime 29 --matrix 100 --sort 1000 --fibonacci 10 --integral 1000 --example_param1 5 --example_param2 10