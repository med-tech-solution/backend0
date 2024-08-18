import logging
logging.basicConfig(filename='./hello_world.log', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
import numpy as np
import math


def factorial(n):
    logging.info('<START7080>')
    if n == 0 or n == 1:
        logging.info('<END7080>')
        return 1

    else:
        logging.info('<END7080>')
        return n * factorial(n - 1)


def is_prime(n):
    logging.info('<START17096>')
    if n <= 1:
        logging.info('<END17096>')
        return False

    if n == 2 or n == 3:
        logging.info('<END17096>')
        return True

    if n % 2 == 0 or n % 3 == 0:
        logging.info('<END17096>')
        return False

    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            logging.info('<END17096>')
            return False

        i += 6
    logging.info('<END17096>')
    return True


def matrix_multiplication(size):
    logging.info('<START12355>')
    A = np.random.rand(size, size)
    B = np.random.rand(size, size)
    result = np.matmul(A, B)
    logging.info('<END12355>')
    return result


def sort_large_list(size):
    logging.info('<START9464>')
    random_list = np.random.randint(1, 100000, size)
    logging.info('<END9464>')
    return sorted(random_list)


def fibonacci(n):
    logging.info('<START9445>')
    if n <= 0:
        logging.info('<END9445>')
        return 0

    elif n == 1:
        logging.info('<END9445>')
        return 1

    else:
        logging.info('<END9445>')
        return fibonacci(n-1) + fibonacci(n-2)

# Function 6: Numerical integration using the trapezoidal rule

def trapezoidal_integration(func, a, b, n):
    logging.info('<START13886>')
    h = (b - a) / n
    result = (func(a) + func(b)) / 2
    for i in range(1, n):
        result += func(a + i * h)
    result *= h
    logging.info('<END13886>')
    return result

class ExampleClass:

    def __init__(self, x, y):
        logging.info('<START4455>')
        self.x = x
        self.y = y

    def add(self):
        logging.info('<START11213>')
        if isinstance(self.x, int) and isinstance(self.y, int):
            logging.info('<END11213>')
            return self.x + self.y

        else:
            logging.info('<END11213>')
            return None


    def multiply(self):
        logging.info('<START4195>')
        logging.info('<END4195>')
        return self.x * self.y


    def divide(self):
        logging.info('<START3933>')
        logging.info('<END3933>')
        return self.x / self.y


    def power(self):
        logging.info('<START3898>')
        logging.info('<END3898>')
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
        logging.info('<START2448>')
        logging.info('<END2448>')
        return x ** 2
    
    print("Numerical integration from 0 to 10 with 1000 intervals:")
    print(trapezoidal_integration(func, 0, 10, 1000))
    print("Numerical integration from 0 to 10 with 100000 intervals:")
    print(trapezoidal_integration(func, 0, 10, 100000))
