from common_imports import *
from code_ast import *

def code_llama_prompt_formatter(query: str, system_prompt: str=None):
    B_INST, E_INST = "[INST]", "[/INST]"
    B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"

    if system_prompt is None:
        SYSTEM_PROMPT = """You are helpful coding assistant. User is asking you to write a function or class for a specific task. 
        Write the function or class in the programming language specified in the query."""
    else:
        SYSTEM_PROMPT = system_prompt

    USER_INSTRUCTION = f"User: {query}"
    
    SYSTEM_PROMPT = B_SYS + SYSTEM_PROMPT + E_SYS
    PROMPT = B_INST + SYSTEM_PROMPT + USER_INSTRUCTION + E_INST
    return PROMPT

def extract_and_clean_code(s):
    # Extract text between ``` and ```
    pattern = r'```(.*?)```'
    matches = re.findall(pattern, s, re.DOTALL)
    
    # Remove "import logging" from each extracted code block
    cleaned_matches = [re.sub(r'\bimport logging\b', '', match).strip() for match in matches]
    
    return cleaned_matches[0]

# Create Code LLama Instruct Engine
class CodeLLamaInstructEngine:
    def __init__(self, systemPromptText: str=None, paramcount: int=7):
        self.AVL_PARAMS = [7,13,34]
        if paramcount not in self.AVL_PARAMS:
            raise ValueError(f"Invalid paramcount. Choose from {self.AVL_PARAMS}")
        self.paramcount = paramcount
        self.client = Together(api_key=os.environ.get('TOGETHER_API_KEY'))
        self.model = f"codellama/CodeLlama-{self.paramcount}b-Instruct-hf"
        if systemPromptText is None:
            self.systemPromptText = """
            You are an AI assistant. You are helping a user with a task. The user is asking you to write a function or class for a specific task.
            """
        else:
            self.systemPromptText = systemPromptText
        
    def run(self, query: str, clean_code: bool=True):
        PROMPT = code_llama_prompt_formatter(
            system_prompt=self.systemPromptText,
            query=query
        )
        response = self.client.completions.create(model=self.model, prompt=PROMPT)
        response_text = response.choices[0].text
        if clean_code:
            return extract_and_clean_code(response_text)
        else:
            return response_text