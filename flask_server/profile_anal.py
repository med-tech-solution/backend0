from common_imports import *


# Calculate Energy and CO2 Emissions
def calculate_energy_and_co2(profile_log, 
                             cpu_power_consumption=65,  # in watts
                             memory_power_consumption_per_byte=1e-9,  # in W/byte
                             emission_factor=0.5,       # in kg CO2/kWh
                             duration_hours=1.0):       # in hours
    # Extract necessary values from profile_log
    cpu_percent = float(profile_log['cpu_percent'])
    rss = int(profile_log['rss'])  # Resident Set Size (memory) in bytes
    vms = int(profile_log['vms'])  # Virtual Memory Size in bytes
    pfaults = int(profile_log['pfaults'])  # Page faults
    pageins = int(profile_log['pageins'])  # Page ins
    iteration = int(profile_log['iteration'])
    
    # Calculate CPU Energy Consumption
    energy_cpu = (cpu_percent / 100.0) * cpu_power_consumption * duration_hours / 1000  # kWh
    
    # Calculate Memory Energy Consumption (average of RSS and VMS)
    avg_memory_usage = (rss + vms) / 2
    energy_memory = avg_memory_usage * memory_power_consumption_per_byte * duration_hours / 1000  # kWh
    
    # Total Energy Consumption
    total_energy_consumption = energy_cpu + energy_memory
    
    # Calculate CO2 Emissions
    co2_emissions = total_energy_consumption * emission_factor  # kg CO2
    
    return {
        'energy_consumption_kwh': total_energy_consumption,
        'co2_emissions_kg': co2_emissions
    }


 
# Process function wise average energy and co2 emissions
def process_function_wise_energy_and_co2(function_profile_map):
    function_wise_energy_and_avg = {}
    for func_id, profile_logs in function_profile_map.items():
        total_stats = {
            'cpu_percent': 0,
            'rss': 0,
            'vms': 0,
            'pfaults': 0,
            'pageins': 0,
            'iteration': 0,
        }

        for log in profile_logs:
            total_stats['cpu_percent'] += float(log['cpu_percent'])
            total_stats['rss'] += int(log['rss'])
            total_stats['vms'] += int(log['vms'])
            total_stats['pfaults'] += int(log['pfaults'])
            total_stats['pageins'] += int(log['pageins'])
            total_stats['iteration'] += 1
        
        # Calculate avg stats
        for key in total_stats:
            try:
                total_stats[key] /= len(profile_logs)
            except ZeroDivisionError:
                total_stats[key] = 0

        elapsed_time_hrs = len(profile_logs)/3600 #seconds to hours

        energy_meta_data = calculate_energy_and_co2(
            total_stats, 
            duration_hours=elapsed_time_hrs, 
            cpu_power_consumption=65, 
            memory_power_consumption_per_byte=1e-9, 
            emission_factor=0.5
            )

        function_wise_energy_and_avg[func_id] = {
            'energy_consumption_kwh': energy_meta_data['energy_consumption_kwh'],
            'co2_emissions_kg': energy_meta_data['co2_emissions_kg'],
            'elapsed_time_secs': len(profile_logs),
            'avg_cpu_percent': total_stats['cpu_percent'],
            'avg_rss': total_stats['rss'],
            'avg_vms': total_stats['vms'],
            'avg_pfaults': total_stats['pfaults'],
            'avg_pageins': total_stats['pageins'],
        }
    
    all_function_avg = {
        'energy_consumption_kwh_all': 0,
        'co2_emissions_kg_all': 0,
        'elapsed_time_secs_all': 0,
        'avg_cpu_percent_all': 0,
        'avg_rss_all': 0,
        'avg_vms_all': 0,
        'avg_pfaults_all': 0,
        'avg_pageins_all': 0,
    }

    for func_id, stats in function_wise_energy_and_avg.items():
        all_function_avg['energy_consumption_kwh_all'] += stats['energy_consumption_kwh']
        all_function_avg['co2_emissions_kg_all'] += stats['co2_emissions_kg']
        all_function_avg['elapsed_time_secs_all'] += stats['elapsed_time_secs']
        all_function_avg['avg_cpu_percent_all'] += stats['avg_cpu_percent']
        all_function_avg['avg_rss_all'] += stats['avg_rss']
        all_function_avg['avg_vms_all'] += stats['avg_vms']
        all_function_avg['avg_pfaults_all'] += stats['avg_pfaults']
        all_function_avg['avg_pageins_all'] += stats['avg_pageins']


    for key in all_function_avg:
        try:
            all_function_avg[key] /= len(function_wise_energy_and_avg)
        except ZeroDivisionError:
            all_function_avg[key] = 0


    return function_wise_energy_and_avg,all_function_avg


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

    function_wise_energy_and_avg,all_function_avg = process_function_wise_energy_and_co2(function_profile_map)

    return function_profile_map, profiletime_to_function, function_wise_energy_and_avg,all_function_avg