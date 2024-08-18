import sys
import time
import os
import argparse


def print_helloworld():
    print("Hello world!")

def cpu_bound():
    print("Starting CPU bound task")
    x = 0
    for i in range(10**8):
        x += i
    print("Exiting CPU bound task")

def memory_bound():
    print("Starting memory bound task")
    x = []
    for i in range(10**6):
        x.append(i)
        if i % 10**5 == 0:
            print(f"Memory bound task: {i}")
            time.sleep(1)
    print("Exiting memory bound task")

def main():
    # Current process ID
    print(f"Current process ID: {os.getpid()}")
    parser = argparse.ArgumentParser(description="Process some arguments.")
    parser.add_argument('--arg1', type=int, help='An integer argument')
    parser.add_argument('--arg2', type=int, help='Another integer argument')
    
    args = parser.parse_args()
    
    print(f"Argument 1: {args.arg1}")
    time.sleep(5)
    print_helloworld()
    print(f"Argument 2: {args.arg2}")
    time.sleep(5)
    cpu_bound()
    memory_bound()
    print("Exiting...")


if __name__ == "__main__":
    main()
