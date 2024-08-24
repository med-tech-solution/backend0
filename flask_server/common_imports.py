# from typing import Annotated
# from langchain_experimental.utilities import PythonREPL
# from langchain_core.tools import tool
# from langchain_openai import ChatOpenAI
# from langchain_core.messages import HumanMessage, SystemMessage,ToolMessage
# from langchain_core.pydantic_v1 import BaseModel, Field
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_community.document_loaders.generic import GenericLoader
# from langchain_community.document_loaders.parsers import LanguageParser
# from langchain_text_splitters import Language
# # from langchain_together import ChatTogether,Together
# from together import Together as Together
# from langchain_community.chat_models.ollama import ChatOllama
# from langgraph.graph import StateGraph, END
# from typing import TypedDict, Literal, List, Union


import ast
import os
import re
import glob
import flask
from flask_cors import CORS
from flask import request, jsonify
import subprocess
from time import sleep
import psutil
import time
import csv
import threading
from datetime import datetime
import shutil
from pathlib import Path
import os
import zipfile
import io
import uuid


from IPython.display import Image, display
from dotenv import load_dotenv
from together import Together



def list_all_files(root_folder):
    # List all python files in the folder
    file_paths = []
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            relative_path = os.path.join(dirpath, filename)
            # Should end with .py
            # does not conatin __MACOSX / .DS_Store / .git / .ipynb_checkpoints
            if relative_path.endswith(".py") and "__MACOSX" not in relative_path and ".DS_Store" not in relative_path and ".git" not in relative_path and ".ipynb_checkpoints" not in relative_path:
                file_paths.append(relative_path)
    return file_paths

def copy_directory_contents(src_dir, dest_dir):
    src_path = Path(src_dir)
    dest_path = Path(dest_dir)
    
    if not src_path.is_dir():
        raise ValueError(f"Source directory '{src_dir}' does not exist or is not a directory.")
    
    # Create the destination directory if it doesn't exist
    if not dest_path.exists():
        dest_path.mkdir(parents=True, exist_ok=True)

    # Iterate over the contents of the source directory
    for item in src_path.iterdir():
        dest_item = dest_path / item.name
        if item.is_dir():
            # Recursively copy directories
            shutil.copytree(item, dest_item)
        else:
            # Copy files
            shutil.copy2(item, dest_item)