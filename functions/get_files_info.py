import os

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
    


# if u need to traverse all the contents of all the sub directories do this instead

# def traverse_dir_content(dir_path, depth=0):
#         result = ""
#         indent = "  " * depth 
        
#         for entry_name in os.listdir(dir_path):
#             entry_path = os.path.join(dir_path, entry_name)
#             try:
#                 stat_info = os.stat(entry_path)
#                 is_dir = os.path.isdir(entry_path)
#                 result += f"{indent} - {entry_name}: file_size={stat_info.st_size} bytes, is_dir={is_dir}\n"
                
#                 if is_dir:
#                     result += traverse_dir_content(entry_path, depth + 1)
#             except (OSError, PermissionError) as e:
#                 result += f"{indent} - {entry_name}: Error accessing - {e}\n"  # Use this line for indented output
       
#         return result