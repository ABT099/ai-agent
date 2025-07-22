import os

from config import MAX_FILE_READ_CHARS
from functions.check_path import check_path, PathType

def get_file_content(working_directory, file_path):
    err, abs_target_path = check_path(working_directory, file_path, PathType.FILE);

    if err != None:
        return err
    
    with open(abs_target_path, "r") as f:
        file_content_string = f.read(MAX_FILE_READ_CHARS)

    if len(file_content_string) == MAX_FILE_READ_CHARS:
        file_content_string += f'[...File "{file_path}" truncated at {MAX_FILE_READ_CHARS} characters]'

    return file_content_string