
from google.genai import types
from functions.check_path import Options, PathType, check_path


def write_file(working_directory, file_path, content):
    err, abs_target_path = check_path(working_directory, file_path, PathType.FILE, options=Options.WRITE_FILE)

    if err != None:
        return err

    with open(abs_target_path, "w") as f:
        f.write(content)

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes a specific content to a file specified by it's path",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that will be written to the file"
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path that the file exists in, relative to the working directory."
            )
        },
    ),
)