import os
from call_function import call_function
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file
from config import MODEL_NAME, SYSTEM_PROMPT, MAX_FILE_READ_CHARS

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("please input a valid prompt")
        sys.exit(1)
    
    prompt = sys.argv[1]
    verbose = "--verbose" in sys.argv
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]
    
    available_functions = types.Tool(
        function_declarations=[
            schema_get_file_content,
            schema_get_files_info,
            schema_run_python_file,
            schema_write_file
        ]
    )
    
    max_iterations = 20
    
    for iteration in range(max_iterations):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=SYSTEM_PROMPT
                ),
            )
            
            if verbose:
                print(f"Iteration {iteration + 1}/{max_iterations}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            
            messages.append(response.candidates[0].content)
            
            if response.function_calls:
                function_call = response.function_calls[0]                
                result = call_function(function_call, verbose)
                if not result:
                    raise Exception("fatal exception: no result found from function call")
                
                # Add function result to conversation - ensure proper format
                if hasattr(result, 'parts') and result.parts:
                    messages.append(types.Content(role="tool", parts=result.parts))
                else:
                    # Fallback: create proper function response part
                    messages.append(types.Content(
                        role="tool", 
                        parts=[types.Part(function_response=result)]
                    ))
                
                if verbose:
                    print(f"Function result: {result}")
                    if hasattr(result, 'parts') and result.parts:
                        print(f"Function response content: {result.parts[0].function_response.response}")
            
            # Check if we have a final text response (only when no function calls)
            elif response.text and not response.function_calls:
                print("Final response:")
                print(response.text)
                break
            
            # If neither function calls nor pure text response
            else:
                print("Warning: Unexpected response format")
                if verbose:
                    print(f"Response has text: {bool(response.text)}")
                    print(f"Response has function calls: {bool(response.function_calls)}")
                break
                
        except Exception as e:
            print(f"Error in iteration {iteration + 1}: {e}")
            if verbose:
                import traceback
                traceback.print_exc()
            break
    
    else:
        print(f"Maximum iterations ({max_iterations}) reached without final response")
    
    if verbose:
        print(f"User prompt: {prompt}")

if __name__ == "__main__":
    main()