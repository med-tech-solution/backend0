from common_imports import *
from utils import *
from profile_utils import *
from profile_anal import *
from opt_utils import *

app = flask.Flask(__name__)
CORS(app)

# Directory for storing uploaded projects
UPLOAD_FOLDER = '../target_projects'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Maps session id to project data
sessions = {
    "sess1": {
        "project_path": "../target_projects/proj_sess1",
    }
}

@app.route('/create_session', methods=['POST'])
def create_session_api():
    file = request.files.get('folder')
    filename=file.filename
    print(filename)
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    # Generate a new session ID
    session_id = "sess1"#str(uuid.uuid4())
    project_folder_name = f"proj_{session_id}"
    project_folder_path = os.path.join(UPLOAD_FOLDER, project_folder_name)
    os.makedirs(project_folder_path, exist_ok=True)

    # Save the uploaded file and extract it
    try:
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(project_folder_path)
    except zipfile.BadZipFile:
        return jsonify({"error": "Invalid ZIP file"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    print("Project uploaded and extracted successfully: ", project_folder_path)
    # Store the session data
    sessions[session_id] = {
        "project_path": project_folder_path#+"/"+filename.split(".")[0]
    }

    print("~~~~~~ Session created: ", sessions[session_id])

    return jsonify({"sessionId": session_id})

@app.route('/get_all_project_files', methods=['POST'])
def get_all_project_files_api():
    data = request.json
    session_id = data.get("session_id")
    
    if not session_id or session_id not in sessions:
        return jsonify({"error": "Session ID not provided or invalid"}), 400
    
    folderpath = sessions[session_id]["project_path"]
    print(folderpath)
    # python_files = glob.glob(f"{folderpath}/*.py")
    python_files = list_all_files(folderpath)

    print("-"*50)
    print(python_files)
    print("-"*50)

    file_content = {}
    
    for file in python_files:
        try:
            with open(file, 'r') as f:
                file_content[file] = f.read()
        except IOError:
            return jsonify({"error": f"Unable to read file: {file}"}), 500
    
    return jsonify(file_content)

@app.route('/process_project_folder', methods=['POST'])
def process_project_folder_api():
    data = request.json
    session_id = data.get("session_id")
    
    if not session_id or session_id not in sessions:
        return jsonify({"error": "Session ID not provided or invalid"}), 400
    
    folderpath = sessions[session_id]["project_path"]
    auto_gen_args = False

    # Replace with actual processing logic
    try:
        hash_to_lineno_fullproj, parse_args_fullproj = process_project_folder(folderpath, auto_gen_args=auto_gen_args)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    sessions[session_id].update({
        "hash_to_lineno_fullproj": hash_to_lineno_fullproj,
        "parse_args_fullproj": parse_args_fullproj,
        "interim_project_path": f"../interim_projects/{os.path.basename(folderpath)}"
    })

    return jsonify({
        "hash_to_lineno_fullproj": hash_to_lineno_fullproj,
        "parse_args_fullproj": parse_args_fullproj
    })

@app.route('/start_profiling', methods=['POST'])
def start_profiling_api():
    data = request.json
    print("------------> Data: ", data)
    session_id = data.get("session_id")
    
    if not session_id or session_id not in sessions:
        return jsonify({"error": "Session ID not provided or invalid"}), 400
    
    if "interim_project_path" not in sessions[session_id]:
        return jsonify({"error": "Interim project path not found"}), 400
    
    proj_name = os.path.basename(sessions[session_id]["project_path"])
    profile_log_csv_path = f"../profile_logs/{proj_name}.csv"
    function_log_path = f"../function_logs/{proj_name}.log"
    
    if "caller_metadata" not in data:
        return jsonify({"error": "Caller metadata not provided"}), 400

    caller_metadata = data.get("caller_metadata")
    # replace 'target_projects' in caller_metadata['filepath'] with 'interim_projects'
    caller_metadata['filepath'] = caller_metadata['filepath'].replace('target_projects', 'interim_projects')
    print("------------> Caller Metadata: ", caller_metadata)

    # caller_metadata = {
    #     "filepath": "../interim_projects/proj1/main.py",
    #     "args": {
    #         "cpu_power": 3,
    #         "memory_power": 3,
    #         "io_power": 3,
    #         "power_of_10": 3
    #     }
    # }

    if "hash_to_lineno_fullproj" not in sessions[session_id]:
        return jsonify({"error": "Intermediary data not found"}), 400
    
    try:
        process = start_profiling(caller_metadata, profile_log_csv_path, function_log_path)
        sessions[session_id].update({
            "process": process,
            "profile_log_csv_path": profile_log_csv_path,
            "function_log_path": function_log_path
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    return jsonify({"process_pid": process.pid})

@app.route('/kill_process', methods=['POST'])
def kill_process_api():
    data = request.json
    session_id = data.get("session_id")
    
    if not session_id or session_id not in sessions:
        return jsonify({"error": "Session ID not provided or invalid"}), 400
    
    if "process" not in sessions[session_id]:
        return jsonify({"error": "No process to kill"}), 400
    
    process = sessions[session_id]["process"]
    try:
        kill_process(process)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    return "Process killed"

@app.route('/analyze_profile', methods=['POST'])
def analyze_profile_api():
    data = request.json
    session_id = data.get("session_id")
    
    if not session_id or session_id not in sessions:
        return jsonify({"error": "Session ID not provided or invalid"}), 400
    
    if "process" not in sessions[session_id]:
        return jsonify({"error": "No process to analyze"}), 300
    
    if check_alive(sessions[session_id]["process"].pid):
        return jsonify({"error": "Profiling Process is still running."}), 501
    
    profile_log_csv_path = sessions[session_id]["profile_log_csv_path"]
    function_log_path = sessions[session_id]["function_log_path"]
    
    try:
        function_profile_map, profiletime_to_function = map_function_to_profile_logs(function_log_path, profile_log_csv_path)
        sessions[session_id].update({
            "function_profile_map": function_profile_map,
            "profiletime_to_function": profiletime_to_function
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "function_profile_map": function_profile_map,
        "profiletime_to_function": profiletime_to_function
    })


# Optimize fucntion
@app.route('/optimize', methods=['POST'])
def optimize_api():
    data = request.json
    session_id = data.get("session_id")
    funcion_id = int(data.get("function_id"))
    
    if not session_id or session_id not in sessions:
        return jsonify({"error": "Session ID not provided or invalid"}), 400
    
    if "hash_to_lineno_fullproj" not in sessions[session_id]:
        return jsonify({"error": "Intermediary data not found"}), 400
    
    print("Function ID: ", funcion_id)
    print("Hash to Line No: ", sessions[session_id]["hash_to_lineno_fullproj"])
    if funcion_id not in sessions[session_id]["hash_to_lineno_fullproj"]:
        return jsonify({"error": "Function ID not found"}), 400
    
    function_info = sessions[session_id]["hash_to_lineno_fullproj"][funcion_id]

    optimized_code = optimize_function(function_info)

    return jsonify({"optimized_code": optimized_code})

# Get all session details 
@app.route('/get_session_details', methods=['POST'])
def get_session_details_api():
    data = request.json
    session_id = data.get("session_id")
    
    if not session_id or session_id not in sessions:
        return jsonify({"error": "Session ID not provided or invalid"}), 400
    
    return jsonify(sessions[session_id])

# Reset the target projects folder, interim projects folder, profile logs folder, and sessions
# Dont delete the root folder just delete its contents
@app.route('/reset', methods=['POST'])
def reset_api():
    for folder in [UPLOAD_FOLDER, '../interim_projects', '../profile_logs']:
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                return jsonify({"error": str(e)}), 500

    sessions.clear()
    return "Reset successful"

if __name__ == '__main__':
    app.run(port=8020, host='0.0.0.0')