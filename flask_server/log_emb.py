from common_imports import *
from code_llama_utils import *

def replace_code_in_file(file_content, old_code, new_code, handle_indentation=True):
    if not handle_indentation:
        return file_content.replace(old_code, new_code)
    
    # Count left side whitespaces in the old code
    left_spaces = len(old_code) - len(old_code.lstrip())
    # Add left spaces at the beginning of each line of the new code
    new_code = "\n".join([f"{' '*left_spaces}{line}" for line in new_code.splitlines()])
    # Replace old code with new code
    new_file_content = file_content.replace(old_code, new_code)
    return new_file_content

def read_code(filepath):
    with open(filepath, "r") as file:
        return file.read()
    

def write_code(filepath, content):
    with open(filepath, "w") as file:
        file.write(content)
    
def hash(s):
    return sum([ord(c) for c in s])




class LogEmbedderWorkflow:
    def __init__(self,paramcount:int=7):
        pass
    # def __init__(self,paramcount:int=7):
    #     self.embedder_code_llama_engine = CodeLLamaInstructEngine(
    #             systemPromptText="""
    #             You are an AI assistant. You will be given python function code snippet and a log message.
    #             Firstly you need to add logging at the beginning of the function body.
    #             Then you need to add logging BEFORE all 'return statements' in the function.
    #             If there is NO return statement, add logging at the end of the function.

    #             Don't add any logging after the return statement, always add BEFORE the return statement.
    #             Don't modify the function code snippet. Don't write 'import logging'. Just add logging.
    #             Also maintain the indentation of the code snippet.
    #             """,
    #             paramcount=paramcount
    #         )
    #     self.rectify_code_llama_engine = CodeLLamaInstructEngine(
    #             systemPromptText="""
    #             You are an AI assistant. You will be given python function code snippet with logging added.
                
    #             You have to check if there is any logging after return statement in the function that is unreachable.
    #             You have to rellocate such logging before each return statement in the function.

    #             Don't modify the rest of the function code snippet.
    #             """,
    #             paramcount=paramcount)

    # @DeprecationWarning 
    # def create_user_prompt(self, function_code_snippet, start_log_message, end_log_message):
    #     return f"""
    #     The function where the logging should be added is:
    #     ```
    #     {function_code_snippet}
    #     ```

    #     The log message to be added at beggining of the function body is:
    #     ```
    #     {start_log_message}
    #     ```

    #     The log message to be added before all return statements is (if there is no return statement, then add at the end of the function):
    #     ```
    #     {end_log_message}
    #     ```

    #     DON'T add any logging AFTER the return statement , always ADD BEFORE the return statement.
    #     """
    
    # @DeprecationWarning
    # def create_rectify_user_prompt(self, function_code_snippet):
    #     return f"""
    #     The function where the logging should be rectified is:
    #     ```
    #     {function_code_snippet}
    #     ```

    #     You have to check if there is any logging after return statement in the function that is unreachable.
    #     You have to rellocate such logging before each return statement in the function.
    #     """
    
    def add_logging_to_function(self,function_code_snippet, start_log_message_snippet, end_log_message_snippet):
        # Add logging at the beginning of the function body
        second_line = function_code_snippet.splitlines()[1]
        second_line_ws = len(second_line) - len(second_line.lstrip())
        intended_start_log_message_snippet = f"\n{' '*second_line_ws}{start_log_message_snippet}\n"
        function_code_snippet = function_code_snippet.splitlines()[0] + intended_start_log_message_snippet + "\n".join(function_code_snippet.splitlines()[1:])

        # Add logging before all return statements
        reconstructed_function_code_snippet = ""
        for line in function_code_snippet.splitlines():
            if line.strip().startswith("return"):
                ws = len(line) - len(line.lstrip())
                reconstructed_function_code_snippet += f"\n{' '*ws}{end_log_message_snippet}\n{line}\n"
            else:
                reconstructed_function_code_snippet += f"\n{line}"
            
        return reconstructed_function_code_snippet
    
    def modify_functions(self,function_code_snippets):
        old_and_new_code_snippets = {}
        hash_values = []
        for function in function_code_snippets:
            print(f"Log: Modifying function: {function.splitlines()[0]}")
            hash_value = hash(function)
            logging_start = f"logging.info('<START{hash_value}>')"
            logging_end = f"logging.info('<END{hash_value}>')"

            # # LLM INVOKATION START
            # user_prompt = self.create_user_prompt(function, logging_start, logging_end)
            # response = self.embedder_code_llama_engine.run(user_prompt)
            # # LLM INVOKATION END

            # Manually adding logging to the function
            response = self.add_logging_to_function(function, logging_start, logging_end)

            # print("----- Original Function -----")
            # print(function)
            # print("----- Modified Function -----")
            # print(response)

            old_and_new_code_snippets[function] = response
            hash_values.append(hash_value)

        return old_and_new_code_snippets,hash_values

    def hash_value_to_line_number(self, file_content, old_and_new_code_snippets, relative_filepath):
        hash_to_lineno = {}
        for old_code_snip, new_code_snip in old_and_new_code_snippets.items():
            hash_value = hash(old_code_snip)
            # Starting index where old_code_snip is present in the file_content
            start_index = file_content.find(old_code_snip)
            # Ending index where old_code_snip is present in the file_content
            end_index = start_index + len(old_code_snip)
            
            # Find the line number of the starting index
            start_index_lineno = file_content[:start_index].count("\n")
            # Find the line number of the ending index
            end_index_lineno = file_content[:end_index].count("\n")
            
            hash_to_lineno[hash_value] = [start_index_lineno, end_index_lineno, relative_filepath]
        return hash_to_lineno

    def run(self, read_filepath, write_filepath, logging_filepath):
        """
        read_filepath: str: The path of the original file to read
        write_filepath: str: The path of the file to write the modified content
        logging_filepath: str: The path of the logging file to write the logging content when the code is executed
        """
        # Read the content of the file
        logging_header = f"import logging\nlogging.basicConfig(filename='{logging_filepath}', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')"
        file_content, code_snippets = get_functions_and_classes(read_filepath)
        # Modify the functions
        old_and_new_code_snippets,hash_values = self.modify_functions(code_snippets["functions"])

        # Hash value to line number mapping
        hash_to_lineno = self.hash_value_to_line_number(file_content, old_and_new_code_snippets, read_filepath)

        # Add logging header to the file content
        file_content = f"{logging_header}\n{file_content}"
        # Replace the old code with the new code in the file content
        for old_code_snip, new_code_snip in old_and_new_code_snippets.items():
            hash_value = hash(old_code_snip)
            file_content = replace_code_in_file(file_content, old_code_snip, new_code_snip,handle_indentation=False) # handle_indentation is False because indentation is not altered in the modified code

        # Write the modified content to the file
        write_code(write_filepath, file_content)
        print("Log: Done")

        return old_and_new_code_snippets,hash_to_lineno