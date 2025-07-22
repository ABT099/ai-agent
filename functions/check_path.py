
import os
from enum import Enum, auto

class PathType(Enum):
    FILE = auto()
    DIRECTORY = auto()

def check_path(working_directory, path, path_type=PathType.DIRECTORY, exec_python=False):
    target_path = os.path.join(working_directory, path)
    abs_target_path = os.path.abspath(target_path)

    match path_type:
        case PathType.DIRECTORY:
            if not os.path.isdir(abs_target_path):
                return f'Error: "{path}" is not a directory', None
        case PathType.FILE:
            if exec_python and not path.endswith(".py"):
                return f'Error: "{path}" is not a Python file.', None
            if not os.path.isfile(abs_target_path):
                return f'Error: File "{path}" not found', None
        case _:
            raise Exception("unexpected path type")
            
    abs_working_dir = os.path.abspath(working_directory)
    if not abs_target_path.startswith(abs_working_dir):
        if exec_python:
            return f'Error: Cannot execute "{path}" as it is outside the permitted working directory', None
        return f'Error: Cannot list "{path}" as it is outside the permitted working directory', None
    
    return None, abs_target_path