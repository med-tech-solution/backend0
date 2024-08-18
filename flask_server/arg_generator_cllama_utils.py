from code_llama_utils import *
from code_ast import *
from common_imports import *

class MainFunctionCurator:
    def __init__(self):
        self.code_llama_engine = CodeLLamaInstructEngine(
            systemPromptText="""
            You are a helpful coding assistant. 
            You are given a not so well written code snippet. The user inputs are not well managed.
            You have to rewrite handling the user inputs using python's argparse library inside the __main__ block.
            Carefully read the code snippet and understand each possible user input and their types.
            JUST WRITE THE CODE INSIDE THE __main__ BLOCK. DO NOT WRITE ANY THING ELSE. ASSUME THAT ALL THE FUNCTIONS USED IN THE CODE ARE DEFINED SOMEWHERE ELSE.
            MAKE SURE YOU COMPLETE THE CODE INSIDE THE __main__ BLOCK.
            """,paramcount=13)
        
    
    def generate_query_prompt(self, query):
        return f"""
        The original code snippet is given below:
        ```
        {query}
        ```

        You have to rewrite the code snippet handling the user inputs using python's argparse library inside the __main__ block. Follow the instructions given in the system prompt.
        JUST WRITE THE CODE INSIDE THE __main__ BLOCK. DO NOT WRITE ANY THING ELSE. ASSUME THAT ALL THE FUNCTIONS USED IN THE CODE ARE DEFINED SOMEWHERE ELSE.
        MAKE SURE YOU COMPLETE THE CODE INSIDE THE __main__ BLOCK.
        """
    
    @staticmethod
    def extract_and_clean_code(s):
        # Extract text between ``` and ```
        pattern = r'```(.*?)```'
        matches = re.findall(pattern, s, re.DOTALL)
        s = matches[0]
        
        s = '\n'.join([line.rstrip() for line in s.splitlines()])
        s = '\n'.join([line for line in s.splitlines() if '__main__' not in line])
        
        return s
        
    def curate_main_block(self, filepath):
        content,_ = get_functions_and_classes(filepath)
        main_block = read_main_block(filepath)

        if main_block == "":
            print(f"No main block found in {filepath}")
            return content

        main_block_body = '\n'.join(main_block.split('\n')[1:])
        response_text = self.code_llama_engine.run(query=self.generate_query_prompt(main_block), extract_and_clean_code=MainFunctionCurator.extract_and_clean_code)
        # Replace the original main block with the curated main block
        content = content.replace(main_block_body, response_text)
        return content