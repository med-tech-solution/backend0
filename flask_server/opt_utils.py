from code_llama_utils import *
from common_imports import *

class CodeOptimizer:
    def __init__(self):
        self.code_llama_engine = CodeLLamaInstructEngine(
            systemPromptText="""
            You are a helpful coding assistant. 
            You are given a non-optimized code snippet. 
            You have to optimize the code snippet.
            Keep in mind the code should be CPU optimized , Memory optimized and should be easy to read and understand.
            Reduce time complexity and space complexity wherever possible. Tou can use alternate libraries or functions if it improves the code quality.
            """,paramcount=13)
        
    
    def generate_query_prompt(self, query):
        return f"""
        The original code snippet is given below:
        ```
        {query}
        ```

        You have to optimize the code snippet following the instructions given in the system prompt.
        """
    
    @staticmethod
    def extract_and_clean_code(s):
        # # Extract text between ``` and ```
        # pattern = r'```(.*?)```'
        # matches = re.findall(pattern, s, re.DOTALL)
        # s = matches[0]
        
        # s = '\n'.join([line.rstrip() for line in s.splitlines()])
        # s = '\n'.join([line for line in s.splitlines() if '__main__' not in line])
        
        return s
        
    def optimize(self, function_body):
        response_text = self.code_llama_engine.run(query=self.generate_query_prompt(function_body), extract_and_clean_code=CodeOptimizer.extract_and_clean_code)
        return response_text
    


def optimize_function(function_info):
    start, end, filepath = function_info

    # Read the file
    with open(filepath, "r") as f:
        content = f.read()

    # Extract the function code snippet
    function_code_snippet = "\n".join(content.splitlines()[start:end])

    # Optimize the function code snippet
    optimizer = CodeOptimizer()
    optimized_code_snippet = optimizer.optimize(function_code_snippet)

    return optimized_code_snippet
