import multiprocessing as mp
import os
import time
import subprocess
import csv
import psutil
import pyRAPL
import json

"""
Utils for profiling a single function:

    - psutil is used to get the process stats 
    - pyRAPL is used to get the power stats (Intel only)
    - pynvml is used to get the GPU stats (NVdia only)
"""

# def get_process_stats(pid):
#     """
#     It returns the process stats for a given pid
#     It returns a dictionary with the following keys:
#     - pid: process id
#     - command: command name
#     - cpu: cpu usage
#     - idlew: idle wakeups
#     - power: power usage
#     - mem: memory usage
#     """
#     command = [
#         "top", "-l", "1", "-pid", str(pid),
#         "-stats", "pid,command,cpu,idlew,power,mem", "-o", "power"
#     ]
    
#     try:
#         process_stats_output = subprocess.check_output(command, text=True)
#         stats = {}
#         keys = process_stats_output.split("\n")[-3].split()
#         values = process_stats_output.split("\n")[-2].split()
#         for i in range(len(keys)):
#             stats[keys[i]] = values[i]
#         return stats        
#     except subprocess.CalledProcessError as e:
#         print(f"An error occurred: {e}")
#     return None


def get_process_stats(pid):
    try:
        process = psutil.Process(pid)
        # memory_full_info = process.memory_full_info()
        cpu_percent = process.cpu_percent(interval=1)
        memory_info = process.memory_info()
        rss = memory_info.rss  # Resident Set Size: physical memory usage
        vms = memory_info.vms  # Virtual Memory Size
        pfaults = memory_info.pfaults  # Page Fault
        pageins = memory_info.pageins  # Page Ins
        return {
            "cpu_percent": cpu_percent,
            "rss": rss,
            "vms": vms,
            "pfaults": pfaults,
            "pageins": pageins
        }
    except psutil.NoSuchProcess:
        return {}


def target_function_1(**kwargs):
    loop_count = kwargs.get("loop_count", 10)
    a = 10
    for i in range(loop_count):
        a+=1
        print(f"Loop count: {i}")
    print(f'Final value of a: {a}')
    print("Exiting... 1")


def profile_wrapper_function(kwargs,semaphore,function, profile_power=False, profile_gpu=False):
    semaphore.acquire()
    function(**kwargs)
    semaphore.release()

def profile_single_function(function, args, kwargs, max_profile_iterations):
    semaphore = mp.Semaphore(0)
    process = mp.Process(target=profile_wrapper_function, args=(kwargs, semaphore, function))
    process.start()
    start = time.time()
    print(f"Parent Process {os.getpid()}")
    print(f"Child Process {process.pid} started")
    input("Press enter to start the process")
    
    semaphore.release() # increment the semaphore to start the process

    # store the stats
    stats_json_store = []

    # profile the process
    # for i in range(max_profile_iterations):
    i = 0
    while True:
        stats = get_process_stats(process.pid)
        print(f"Process stats: {stats}")

        print(f'Keys: {list(stats.keys())}')
        print(f'Values: {list(stats.values())}')
        # store the stats
        if len(list(stats.values()))>0:
            stats['iteration'] = i
            stats['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            stats_json_store.append(stats)
        else:
            break
        i += 1

    process.join()
    end = time.time()
    print(f"Process {process.pid} ended")
    print(f"Total time taken: {end - start} seconds")
    return stats_json_store

if __name__ == '__main__':
    stats_json_store = profile_single_function(target_function_1, (), {"loop_count": 1000000}, max_profile_iterations=20)

    # write the stats to a json file
    with open("stats.json", "w") as f:
        json.dump(stats_json_store, f, indent=4)

    print("Stats written to stats.json")
    
