import logging
logging.basicConfig(filename='../function_logs/proj1.log', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
import os
import time

# CPU Heavy Task

def cpu_bound(p):
    logging.info('<START17049>')
    print("Starting CPU bound task")
    x = 0
    for i in range(10**p):
        x += i
        if i % 10**p == 0:
            print(f"CPU bound task: {i}")
            time.sleep(1)
    print("Exiting CPU bound task")
    logging.info('<END17049>')
    return x

# Memory Heavy Task

def memory_bound(p):
    logging.info('<START19555>')
    print("Starting memory bound task")
    x = []
    for i in range(10**p):
        x.append(i)
        if i % 10**(p-1) == 0:
            print(f"Memory bound task: {i}")
            time.sleep(1)
    print("Exiting memory bound task")
    logging.info('<END19555>')
    return x

# I/O Heavy Task

def io_bound(p):
    logging.info('<START41611>')
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
    logging.info('<END41611>')
    return len(lines)

# Power heavy task

def power_bound():
    logging.info('<START9996>')
    print("Starting power bound task")
    x = 2**1000000
    print("Exiting power bound task")
    logging.info('<END9996>')
    return x
