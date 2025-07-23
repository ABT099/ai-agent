import subprocess
from google.genai import types
from functions.check_path import PathType, check_path
import sys

def run_python_file(working_directory, file_path, args=[]):
    err, abs_target_path = check_path(working_directory, file_path, PathType.FILE, exec_python=True)
    
    if err != None:
        return err
    
    try:
        completed_process = subprocess.run(
            [sys.executable, abs_target_path, *args],
            capture_output=True,
            text=True,
            cwd=working_directory,
            timeout=30
        )

        if not completed_process.stdout.strip() and not completed_process.stderr.strip():
            return "No output produced."

        output = ""
        if completed_process.stdout:
            output += f"STDOUT:\n{completed_process.stdout}"
        if completed_process.stderr:
            output += f"\nSTDERR:\n{completed_process.stderr}"
        
        exist_code = completed_process.returncode

        if exist_code != 0:
            output += f"Process exited with code {exist_code}"

        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs python files that ends with .py, and execute them",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path that the file exists in, relative to the working directory."
            ),
        },
    ),
)