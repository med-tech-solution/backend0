from common_imports import *
from utils import *
from profile_utils import *
from profile_anal import *

load_dotenv("../.env")

app = flask.Flask(__name__)
CORS(app)

# Maps session id to the 
#  - hash to line number mapping
#  - parser arguments
#  - project name
#  - folder path
sessions = {
    "sess1": {
        "project_path": "../target_projects/proj1",
    }
}


@app.route('/create_session', methods=['POST'])
def create_session_api():
    #  TODO: Create a new session and return the session id. Here project files should come from frontend
    return jsonify({"sessionId": "sess1"})

@app.route('/get_all_project_files', methods=['POST'])
def get_all_project_files_api():
    """
    It takes session id and returns a dictionary with the following:
    file_path -> content
    """
    data = request.json
    
    if "session_id" not in data:
        return "Session ID not provided"
    session_id = data["session_id"]
    if session_id not in sessions:
        return "No session found at backend"
    
    folderpath = sessions[session_id]["project_path"]
    # print(folderpath)
    # print(os.curdir)
    # print(os.listdir(folderpath))
    python_files = glob.glob(f"{folderpath}/*.py")
    # print(python_files)
    file_content = {}
    for file in python_files:
        with open(file, 'r') as f:
            file_content[file] = f.read()
    return jsonify(file_content)


# It takes session id and returns the hash to line number mapping and parser arguments
@app.route('/process_project_folder', methods=['POST'])
def process_project_folder_api():
    data = request.json
    
    if "session_id" not in data:
        return "Session ID not provided"
    session_id = data["session_id"]
    if session_id not in sessions:
        return "No session found at backend"
    
    folderpath = sessions[session_id]["project_path"]
    
    # TODO: Get this from the frontend. Requires more testing!! Currently considering it as False, as we mannually added the argparse code in the main block
    auto_gen_args = False 

    hash_to_lineno_fullproj, parse_args_fullproj = process_project_folder(folderpath,auto_gen_args=auto_gen_args)
    
    sessions[session_id] = {
        "project_path": folderpath,
        "hash_to_lineno_fullproj": hash_to_lineno_fullproj,
        "parse_args_fullproj": parse_args_fullproj
    }

    return jsonify({
        "hash_to_lineno_fullproj": hash_to_lineno_fullproj,
        "parse_args_fullproj": parse_args_fullproj
    })

@app.route('/get_hash_to_lineno_fullproj', methods=['POST'])
def get_hash_to_lineno_fullproj_api():
    data = request.json
    
    if "session_id" not in data:
        return "Session ID not provided"
    session_id = data["session_id"]
    if session_id not in sessions:
        return "No session found at backend"
    return jsonify(sessions[session_id]["hash_to_lineno_fullproj"])


@app.route('/start_profiling', methods=['POST'])
def start_profiling_api():
    data = request.json

    if "session_id" not in data:
        return "Session ID not provided"
    session_id = data["session_id"]
    if session_id not in sessions:
        return "No session found at backend"
    
    proj_name = sessions[session_id]["project_path"].split("/")[-1]
    profile_log_csv_path = f"../profile_logs/{proj_name}.csv"
    function_log_path = f"../function_logs/{proj_name}.log"

    # TODO: Get the caller metadata from the frontend
    caller_metadata = {
        "filepath": "../interim_projects/proj1/main.py",
        "args": {
            "cpu_power": 3,
            "memory_power": 3,
            "io_power": 3,
            "power_of_10":3
        }
    }

    if "hash_to_lineno_fullproj" not in sessions[session_id]:
        return "Intermediary data not found"

    process = start_profiling(caller_metadata, profile_log_csv_path, function_log_path)
    sessions[session_id]["process"] = process
    sessions[session_id]["profile_log_csv_path"] = profile_log_csv_path
    sessions[session_id]["function_log_path"] = function_log_path
    return jsonify({
        "process_pid": process.pid
    })

@app.route('/start_profiling2', methods=['POST'])
def start_profiling_api2():
    
    data = request.json

    if "session_id" not in data:
        return "Session ID not provided", 400

    session_id = data["session_id"]
    if session_id not in sessions:
        return "No session found at backend", 404

    if "caller_metadata" not in data:
        return "Caller metadata not provided", 400
    
    caller_metadata = data["caller_metadata"]
    print(data)
    proj_name = sessions[session_id]["project_path"].split("/")[-1]
    profile_log_csv_path = f"../profile_logs/{proj_name}.csv"
    function_log_path = f"../function_logs/{proj_name}.log"
    
    if "hash_to_lineno_fullproj" not in sessions[session_id]:
        return "Intermediary data not found", 404
    # print("here")
    process = start_profiling(caller_metadata, profile_log_csv_path, function_log_path)
    sessions[session_id]["process"] = process
    sessions[session_id]["profile_log_csv_path"] = profile_log_csv_path
    sessions[session_id]["function_log_path"] = function_log_path

    return jsonify({
        "process_pid": process.pid
    })

@app.route('/kill_process', methods=['POST'])
def kill_process_api():
    data = request.json

    if "session_id" not in data:
        return "Session ID not provided"
    session_id = data["session_id"]
    if session_id not in sessions:
        return "No session found at backend"
    
    if "process" not in sessions[session_id]:
        return "No process to kill"
    process = sessions[session_id]["process"]
    kill_process(process)
    return "Process killed"


@app.route('/analyze_profile', methods=['POST'])
def analyze_profile_api():
    data = request.json
    
    if "session_id" not in data:
        return "Session ID not provided",201
    session_id = data["session_id"]
    if session_id not in sessions:
        return "No session found at backend",202
    
    proj_name = sessions[session_id]["project_path"].split("/")[-1]

    if "process" not in sessions[session_id]:
        return "No process to analyze",300
    if check_alive(sessions[session_id]["process"].pid):
        return "Profiling Process is still running.",501
    
    profile_log_csv_path = sessions[session_id]["profile_log_csv_path"]
    function_log_path = sessions[session_id]["function_log_path"]
    function_profile_map, profiletime_to_function = map_function_to_profile_logs(function_log_path, profile_log_csv_path)
    sessions[session_id]["function_profile_map"] = function_profile_map
    sessions[session_id]["profiletime_to_function"] = profiletime_to_function

    return jsonify({
        "function_profile_map": function_profile_map,
        "profiletime_to_function": profiletime_to_function
    })






if __name__ == '__main__':
    app.run(port=8020,host='0.0.0.0')