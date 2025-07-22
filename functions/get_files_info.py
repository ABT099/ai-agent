import os

def get_files_info(working_directory, directory="."):
    def format_result_header(dir_name):
        if directory != ".":
            return f"Result for {dir_name} directory:\n"
        return "Result for current directory:\n"
    
    def traverse_dir_content(dir_path, depth=0):
        result = ""
        # indent = "  " * depth  # Uncomment for indented output when using recursion
        
        for entry_name in os.listdir(dir_path):
            entry_path = os.path.join(dir_path, entry_name)
            try:
                stat_info = os.stat(entry_path)
                is_dir = os.path.isdir(entry_path)
                result += f" - {entry_name}: file_size={stat_info.st_size} bytes, is_dir={is_dir}\n"
                # result += f"{indent} - {entry_name}: file_size={stat_info.st_size} bytes, is_dir={is_dir}\n"  # Use this line for indented output
                
                # Uncomment the lines below to enable recursive directory traversal with proper indentation
                # if is_dir:
                #     result += traverse_dir_content(entry_path, depth + 1)
            except (OSError, PermissionError) as e:
                result += f" - {entry_name}: Error accessing - {e}\n"
                # result += f"{indent} - {entry_name}: Error accessing - {e}\n"  # Use this line for indented output
       
        return result
    
    if directory == ".":
        target_path = working_directory
    else:
        target_path = os.path.join(working_directory, directory)
    
    abs_target_path = os.path.abspath(target_path)
    
    if not os.path.isdir(abs_target_path):
        return f'Error: "{directory}" is not a directory'
   
    abs_target_path = os.path.abspath(target_path)
    abs_working_dir = os.path.abspath(working_directory)
    if not abs_target_path.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    try:
        return format_result_header(directory) + traverse_dir_content(abs_target_path)
    except Exception as e:
        return f"Error: {e}"