from common_imports import *
from log_emb import *

def process_project_folder(folderpath):
    """
    It takes a folder path and processes all the python files in the folder
    """
    # Extract project name from folder path
    project_name = folderpath.split("/")[2]
    # Creating a folder to store the modified files
    try:
        os.mkdir(f"../interim_projects/{project_name}")
    except FileExistsError:
        print("Interim folder already exists")

    # Creating log embedding workflow object
    log_embedder = LogEmbedderWorkflow(paramcount=7)
                                
    # Dictionary to store hash value to line number mapping for all the files in the project
    hash_to_lineno_fullproj = {}
    # Dictionary to store the arguments of the parser in all the files in the project
    parse_args_fullproj = {}
    
     # Get all the python files in the folder
    python_files = glob.glob(f"{folderpath}/*.py")
    for file in python_files:
        read_filepath = file
        write_filepath = f"../interim_projects/{project_name}/{file.split('/')[-1]}"
        logging_filepath = f"../function_logs/{project_name}.log"
        print(f"Read File: {read_filepath} | Write File: {write_filepath} | Logging File: {logging_filepath}")
        # Process the file
        old_and_new_code_snippets,hash_to_lineno = log_embedder.run(read_filepath, write_filepath, logging_filepath)
        hash_to_lineno_fullproj.update(hash_to_lineno)

        parse_args = retireve_all_parse_args(read_filepath)
        parse_args_fullproj[read_filepath] = parse_args

        print("Log: Done")
    
    return hash_to_lineno_fullproj,parse_args_fullproj