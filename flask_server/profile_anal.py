from common_imports import *

def map_function_to_profile_logs(function_log_path, profile_log_path):
    # Parsing function log to extract start and end times
    function_map = {}
    with open(function_log_path, 'r') as f_log:
        for line in f_log:
            timestamp_str, action = line.strip().split(" - ")
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            func_id = re.search(r'\d+', action).group()  # Extracting the function ID

            if action.startswith("<START"):
                if func_id not in function_map:
                    function_map[func_id] = {'start': timestamp, 'end': None}
                else:
                    function_map[func_id]['start'] = timestamp
            elif action.startswith("<END"):
                if func_id in function_map:
                    function_map[func_id]['end'] = timestamp

    # Filtering out functions that do not have an end time
    valid_functions = {k: v for k, v in function_map.items() if v['end'] is not None}

    # Mapping profile logs to valid functions
    function_profile_map = {func_id: [] for func_id in valid_functions}

    with open(profile_log_path, 'r') as p_log:
        reader = csv.DictReader(p_log)
        for row in reader:
            log_time = datetime.strptime(row['time'], "%Y-%m-%d %H:%M:%S")
            for func_id, times in valid_functions.items():
                if times['start'] <= log_time <= times['end']:
                    function_profile_map[func_id].append(row)


    # reverse the mapping from profile time to function
    profiletime_to_function = {}
    for func_id, profile_logs in function_profile_map.items():
        for log in profile_logs:
            profiletime_to_function[str(log['time'])]={"function_id": func_id, "profile_log": log}

    return function_profile_map, profiletime_to_function