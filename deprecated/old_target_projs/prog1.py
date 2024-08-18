import numpy as np
import math

def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

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
    # Factorial
    print("Factorial of 10:", factorial(10))
    print("Factorial of 20:", factorial(20))

    # Prime number check
    print("Is 29 prime?", is_prime(29))
    print("Is 104729 prime?", is_prime(104729))  # 10000th prime

    # Matrix multiplication with increasing size
    print("Matrix multiplication with size 100:")
    matrix_multiplication(100)
    print("Matrix multiplication with size 500:")
    matrix_multiplication(500)

    # Sorting large list with increasing size
    print("Sorting list of size 1000:")
    sort_large_list(1000)
    print("Sorting list of size 1000000:")
    sort_large_list(1000000)

    # Fibonacci with increasing depth
    print("Fibonacci number for n=10:", fibonacci(10))
    print("Fibonacci number for n=20:", fibonacci(20))

    # Trapezoidal integration
    def func(x):
        return x ** 2
    
    print("Numerical integration from 0 to 10 with 1000 intervals:")
    print(trapezoidal_integration(func, 0, 10, 1000))
    print("Numerical integration from 0 to 10 with 100000 intervals:")
    print(trapezoidal_integration(func, 0, 10, 100000))
