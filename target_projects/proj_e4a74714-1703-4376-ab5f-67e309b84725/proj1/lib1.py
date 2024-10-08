import os
import time

# CPU Heavy Task

def cpu_bound(p):
    print("Starting CPU bound task")
    x = 0
    for i in range(10**p):
        x += i
        if i % 10**p == 0:
            print(f"CPU bound task: {i}")
            time.sleep(1)
    print("Exiting CPU bound task")
    return x

# Memory Heavy Task

def memory_bound(p):
    print("Starting memory bound task")
    x = []
    for i in range(10**p):
        x.append(i)
        if i % 10**(p-1) == 0:
            print(f"Memory bound task: {i}")
            time.sleep(1)
    print("Exiting memory bound task")
    return x

# I/O Heavy Task

def io_bound(p):
    # Generate a large file
    print("Starting I/O bound task")
    with open("large_file.txt", "w") as f:
        for i in range(10**p):
            f.write("Hello world!\n")
            if i % 10**(p-1) == 0:
                print(f"I/O bound task: {i}")
                time.sleep(1)

    # Now read the file
    with open("large_file.txt", "r") as f:
        lines = f.readlines()
        print(f"Number of lines in the file: {len(lines)}")

    # Remove the file
    os.remove("large_file.txt")
    print("Exiting I/O bound task")
    return len(lines)

# Power heavy task

def power_bound():
    print("Starting power bound task")
    x = 2**1000000
    print("Exiting power bound task")
    return x
