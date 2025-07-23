import os
from google.genai import types

from functions.check_path import check_path

def get_files_info(working_directory, directory="."):
    def format_result_header(dir_name):
        if directory != ".":
            return f"Result for {dir_name} directory:\n"
        return "Result for current directory:\n"
    
    def traverse_dir_content(dir_path):
        result = ""
        
        for entry_name in os.listdir(dir_path):
            entry_path = os.path.join(dir_path, entry_name)
            try:
                stat_info = os.stat(entry_path)
                is_dir = os.path.isdir(entry_path)
                result += f" - {entry_name}: file_size={stat_info.st_size} bytes, is_dir={is_dir}\n"
            except (OSError, PermissionError) as e:
                result += f" - {entry_name}: Error accessing - {e}\n"
       
        return result
    
    err, abs_target_path = check_path(working_directory, directory);

    if err != None:
        return err

    try:
        return format_result_header(directory) + traverse_dir_content(abs_target_path)
    except Exception as e:
        return f"Error: {e}"
    

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)