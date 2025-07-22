import os

from config import MAX_FILE_READ_CHARS
from functions.path_helpers import check_path, get_abs_target_path, PathType

def get_file_content(working_directory, file_path):
    err = check_path(working_directory, file_path, PathType.FILE);

    if err != None:
        return err
    
    with open(get_abs_target_path(working_directory=working_directory, path=file_path), "r") as f:
        file_content_string = f.read(MAX_FILE_READ_CHARS)

    if len(file_content_string) == MAX_FILE_READ_CHARS:
        file_content_string += f'[...File "{file_path}" truncated at {MAX_FILE_READ_CHARS} characters]'

    return file_content_string