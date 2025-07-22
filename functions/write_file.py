
from functions.check_path import PathType, check_path


def write_file(working_directory, file_path, content):
    err, abs_target_path = check_path(working_directory, file_path, PathType.FILE)

    if err != None:
        return err

    with open(abs_target_path, "w") as f:
        f.write(content)

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'