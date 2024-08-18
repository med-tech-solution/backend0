from common_imports import *

def get_process_stats(pid,iteration):
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
            "pageins": pageins,
            "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "iteration": iteration
        }
    except psutil.NoSuchProcess:
        return {}

def store_stats_as_csv(stats_json_store, csv_filepath):
    # Column names are the keys of the first dictionary
    csv_columns = stats_json_store[0].keys()
    try:
        with open(csv_filepath, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in stats_json_store:
                if len(data.keys()) > 0:
                    writer.writerow(data)
    except IOError:
        print("I/O error")


def profile(process, profile_log_csv_path):
    print("Currently profiling the process with PID: ", process.pid)
    stats_json_store = []
    iteration = 0
    while process.poll() is None:
        cur_stats = get_process_stats(process.pid, iteration)
        stats_json_store.append(cur_stats)
        iteration += 1
        store_stats_as_csv(stats_json_store, profile_log_csv_path)
        print(f"Process stats: {cur_stats}")

    print(f"Process ended with return code: {process.returncode}")
    print("Exiting profiler...")

def montior(caller_metadata, profile_log_csv_path):
    # Parse the arguments
    """
    Target file: target_project/test0.py
    Args: arg1, arg2
    Value: 10 , 20
    """
    # Add permissions to the file
    # print("->>>>>>>> Adding permissions to the file", caller_metadata['filepath'])
    os.system(f"chmod -R 777 {'../interim_projects/'}")
    # print("->>>>>>>> Permissions added to the file", caller_metadata['filepath'])

    command = ["python3", caller_metadata["filepath"]]+[f"--{key}={value}" for key, value in caller_metadata["args"].items()]
    process = subprocess.Popen(command)
    pid = process.pid
    print(f"Started with PID: {pid}")

    # TODO : ought to be called in a separate thread 
    # profile(process, profile_log_csv_path)

    # Start a thread to monitor the process
    thread = threading.Thread(target=profile, args=(process, profile_log_csv_path))
    thread.start()
    return process

def kill_process(process):
    process.kill()

def check_if_process_exists(pid):
    try:
        process = psutil.Process(pid)
        return True
    except psutil.NoSuchProcess:
        return False
    
def check_alive(pid):
    try:
        process = psutil.Process(pid)
        return process.is_running()
    except psutil.NoSuchProcess:
        return False

def start_profiling(caller_metadata, profile_log_csv_path, function_log_path):
    # Remove the function logs
    try:
        print("Removing the function logs")
        os.remove(function_log_path)
    except:
        pass
    process = montior(caller_metadata, profile_log_csv_path)
    return process
