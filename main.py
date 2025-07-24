import os
import sys
from call_function import call_function
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file
from config import MODEL_NAME, SYSTEM_PROMPT, MAX_FILE_READ_CHARS
from ui import (
    console, print_header, print_thinking, print_function_call,
    print_iteration_info, print_final_response, print_error,
    print_warning, print_success, print_info, get_user_input
)

def process_query(client, prompt: str, verbose: bool):
    """Process a single query and return success status"""
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
    
    for iteration in range(1, max_iterations + 1):
        try:
            if verbose:
                print_iteration_info(iteration, max_iterations)
            print_thinking()
            
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=SYSTEM_PROMPT
                ),
            )
            
            if verbose:
                tokens_info = {
                    'prompt_token_count': response.usage_metadata.prompt_token_count,
                    'candidates_token_count': response.usage_metadata.candidates_token_count
                }
                print_iteration_info(iteration, max_iterations, tokens_info)
            
            messages.append(response.candidates[0].content)
            
            if response.function_calls:
                function_call = response.function_calls[0]
                print_function_call(function_call.name, verbose)
                
                result = call_function(function_call, verbose)
                if not result:
                    raise Exception("No result returned from function call")
                
                # Add function result to conversation
                if hasattr(result, 'parts') and result.parts:
                    messages.append(types.Content(role="tool", parts=result.parts))
                else:
                    messages.append(types.Content(
                        role="tool",
                        parts=[types.Part(function_response=result)]
                    ))
                
                if verbose:
                    print_success("Function completed")
            
            # Check if we have a final text response
            elif response.text and not response.function_calls:
                print_final_response(response.text)
                return True
            
            # Unexpected response format
            else:
                print_warning("Unexpected response format")
                if verbose:
                    print_info(f"Has text: {bool(response.text)}")
                    print_info(f"Has function calls: {bool(response.function_calls)}")
                return False
                
        except Exception as e:
            print_error(str(e), iteration)
            if verbose:
                import traceback
                console.print(f"[red]{traceback.format_exc()}[/red]")
            return False
    
    print_warning(f"Reached maximum iterations ({max_iterations}) without final response")
    return False

def main():
    try:
        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")
        
        if not api_key:
            console.print("❌ [bold red]Error:[/bold red] GEMINI_API_KEY not found in environment variables")
            console.print("💡 [yellow]Please set your API key in the .env file[/yellow]")
            sys.exit(1)
        
        client = genai.Client(api_key=api_key)
        
        print_header()
        
        while True:
            try:
                prompt, verbose = get_user_input()
                success = process_query(client, prompt, verbose)
                
                if success:
                    print_success("Query completed successfully!")
                else:
                    print_warning("Query completed with issues")
                
                # Add separator for next query
                console.print()
                from rich.rule import Rule
                console.print(Rule(style="dim"))
                console.print()
                
            except KeyboardInterrupt:
                console.print("\n[yellow]👋 Chat session ended[/yellow]")
                break
            except Exception as e:
                print_error(f"Error processing query: {e}", 0)
                console.print("[dim]Continuing to next query...[/dim]")
                console.print()
    
    except KeyboardInterrupt:
        console.print("\n[yellow]👋 Operation cancelled by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[bold red]❌ Fatal error:[/bold red] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()