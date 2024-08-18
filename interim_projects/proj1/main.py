import logging
logging.basicConfig(filename='../function_logs/proj1.log', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
from lib1 import *
from lib2 import *
import argparse


if __name__ == '__main__':
    # Current process ID
    print(f"Current process ID: {os.getpid()}")
    parser = argparse.ArgumentParser(description="Process some arguments.")
    parser.add_argument('--cpu_power', type=int, help='Power of CPU bound task')
    parser.add_argument('--memory_power', type=int, help='Power of memory bound task')
    parser.add_argument('--io_power', type=int, help='Power of I/O bound task')
    parser.add_argument('--power_of_10', type=int, help='Power of 10 for sorting list')
    
    args = parser.parse_args()

    if args.cpu_power:
        cpu_bound(args.cpu_power)

    if args.memory_power:
        memory_bound(args.memory_power)

    if args.io_power:
        io_bound(args.io_power)

    power_bound()

    if args.power_of_10:
        arr = generate_random_list(args.power_of_10)
        print("Running bubble sort ...")
        arr = bubble_sort(arr)
        print("Running selection sort ...")
        arr = selection_sort(arr)
        print("Running inbuilt sort ...")
        arr = python_sort(arr)

    print("Exiting...")