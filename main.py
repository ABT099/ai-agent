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

from config import MODEL_NAME, SYSTEM_PROMPT


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("please input a valid prompt")
        sys.exit(1)

    prompt = sys.argv[1]

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

    response = client.models.generate_content(
        model=MODEL_NAME, 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=SYSTEM_PROMPT
        ),
    )
    
    verbose = "--verbose" in sys.argv
     
    result = call_function(response.function_calls[0], verbose)

    if (not result):
        raise Exception("fatal exception: no result found from function call")
    
    if verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print(f"-> {result.parts[0].function_response.response}")


if __name__ == "__main__":
    main()
