from common_imports import *

def get_functions_and_classes(filepath):
    """
    It takes a file path and returns the original source code of functions and code-snippets in the file
    Code snippets are the source code of functions and classes in the file
    """
    with open(filepath, "r") as file:
        file_content = file.read()
    
    # Parse the file content into an Abstract Syntax Tree (AST)
    tree = ast.parse(file_content)
    
    # List to store the source code of functions and classes
    code_snippets = {
        "classes": [],
        "functions": []
    }

    # Walk through the AST and find all functions and classes
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            start_line = node.lineno - 1
            end_line = node.end_lineno
            code_snippets["classes"].append("".join(file_content.splitlines(keepends=True)[start_line:end_line]))
        if isinstance(node, ast.FunctionDef):
            start_line = node.lineno - 1
            end_line = node.end_lineno
            code_snippets["functions"].append("".join(file_content.splitlines(keepends=True)[start_line:end_line]))
    return file_content , code_snippets



#  A function to read body inside if __name__ == '__main__': block

def read_main_block(filepath):
    with open(filepath, "r") as file:
        file_content = file.read()
    tree = ast.parse(file_content)
    main_block = ""
    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            if isinstance(node.test, ast.Compare):
                if isinstance(node.test.left, ast.Name) and isinstance(node.test.comparators[0], ast.Str):
                    if node.test.left.id == "__name__" and node.test.comparators[0].s == "__main__":
                        start_line = node.lineno - 1
                        end_line = node.end_lineno
                        main_block = "".join(file_content.splitlines(keepends=True)[start_line:end_line])
    return main_block

def retireve_all_parse_args(filepath):
    """
    It takes a file path and returns the arguments of the parser in the file
    returns: A List of dictionaries containing the arguments of the parser
    [
        {
            "name":"arg1",
            "type":"int",
            "default":None,
            "required":True,
            "help":"This is arg1"
        },
        ...
    ]
    """
    main_block = read_main_block(filepath)
    tree = ast.parse(main_block)
    parse_args = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                if isinstance(node.func.value, ast.Name) and node.func.value.id == "parser" and node.func.attr == "add_argument":
                    arg_name = node.args[0].s
                    arg_type = node.keywords[0].value.id
                    arg_default = None
                    arg_required = True
                    arg_help = None
                    for keyword in node.keywords:
                        if keyword.arg == "default":
                            arg_default = keyword.value.s
                        if keyword.arg == "required":
                            arg_required = keyword.value.value
                        if keyword.arg == "help":
                            arg_help = keyword.value.s
                    parse_args.append({
                        "name":arg_name.split("--")[1],
                        "type":arg_type,
                        "default":arg_default,
                        "required":arg_required,
                        "help":arg_help
                    })
    return parse_args