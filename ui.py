import sys
import time
from typing import Optional

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.prompt import Prompt, Confirm
    from rich.markdown import Markdown
    from rich.syntax import Syntax
    from rich.table import Table
    from rich.live import Live
    from rich.rule import Rule
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

if not RICH_AVAILABLE:
    raise ImportError("The rich library is required. Install it with: pip install rich")

# Initialize console
console = Console()

def print_header():
    """Print a nice header for the AI agent"""
    title = Text("🤖 AI Agent Assistant", style="bold bright_blue")
    subtitle = Text("Continuous chat mode - Type 'quit' to exit", style="dim cyan")
    
    header_panel = Panel.fit(
        Text.assemble(title, "\n", subtitle),
        style="bright_blue",
        padding=(1, 2),
        border_style="bright_blue"
    )
    
    console.print(header_panel)
    console.print()

def print_thinking():
    """Show a thinking animation"""
    with console.status("[yellow]🤔 Thinking...[/yellow]", spinner="dots"):
        time.sleep(1)

def print_function_call(function_name: str, verbose: bool = False):
    """Pretty print function calls"""
    icon_map = {
        'get_file_content': '📄',
        'get_files_info': '📁', 
        'run_python_file': '🐍',
        'write_file': '✏️'
    }
    icon = icon_map.get(function_name, '🔧')
    
    if verbose:
        console.print(f"  {icon} [bright_magenta]Executing:[/bright_magenta] [bold white]{function_name}[/bold white]")
    else:
        friendly_name = function_name.replace('_', ' ').title()
        console.print(f"  {icon} [bright_magenta]{friendly_name}[/bright_magenta]")

def print_iteration_info(iteration: int, max_iterations: int, tokens_info: Optional[dict] = None):
    """Print iteration information in a clean format"""
    progress_text = Text()
    progress_text.append(f"[{iteration}/{max_iterations}]", style="bright_cyan bold")
    
    if tokens_info:
        prompt_tokens = tokens_info.get('prompt_token_count', 0)
        response_tokens = tokens_info.get('candidates_token_count', 0)
        progress_text.append(f" Tokens: {prompt_tokens}→{response_tokens}", style="dim white")
    
    console.print(progress_text)

def print_final_response(response: str):
    """Print the final response with clean formatting"""
    if has_markdown_elements(response):
        try:
            markdown = Markdown(response)
            response_panel = Panel(
                markdown,
                title="🎯 Final Response",
                title_align="left",
                style="bright_green",
                padding=(1, 2),
                border_style="bright_green"
            )
            console.print(response_panel)
        except Exception:
            # Fallback to plain text if markdown parsing fails
            response_panel = Panel(
                response,
                title="🎯 Final Response",
                title_align="left",
                style="bright_green",
                padding=(1, 2),
                border_style="bright_green"
            )
            console.print(response_panel)
    else:
        response_panel = Panel(
            response,
            title="🎯 Final Response",
            title_align="left",
            style="bright_green",
            padding=(1, 2),
            border_style="bright_green"
        )
        console.print(response_panel)

def has_markdown_elements(text: str) -> bool:
    """Check if text contains markdown-like elements"""
    markdown_indicators = [
        '**', '*', '`', '#', '-', '1.', '2.', '3.',
        '```', '---', '###', '##', '[', '](', '|'
    ]
    return any(indicator in text for indicator in markdown_indicators)

def print_error(error_msg: str, iteration: int):
    """Print errors in a user-friendly way"""
    error_panel = Panel(
        f"[bold red]Error in iteration {iteration}:[/bold red]\n[red]{error_msg}[/red]",
        title="❌ Error",
        title_align="left",
        style="red",
        border_style="red"
    )
    console.print(error_panel)

def print_usage():
    """Print usage information"""
    usage_text = Text()
    usage_text.append("🔍 Available commands:\n\n", style="bold bright_blue")
    usage_text.append("• ", style="bright_cyan")
    usage_text.append("help", style="bold yellow")
    usage_text.append(" - Show this help message\n", style="white")
    usage_text.append("• ", style="bright_cyan")
    usage_text.append("quit/exit/q", style="bold yellow")
    usage_text.append(" - Exit the application\n", style="white")
    usage_text.append("• ", style="bright_cyan")
    usage_text.append("Any other text", style="bold yellow")
    usage_text.append(" - Your prompt for the AI agent", style="white")
    
    examples_text = Text()
    examples_text.append("\n💡 Example prompts:\n\n", style="bold bright_green")
    examples_text.append("• \"analyze the main.py file\"\n", style="cyan")
    examples_text.append("• \"create a hello world script\"\n", style="cyan")
    examples_text.append("• \"show me all Python files in the project\"", style="cyan")
    
    help_panel = Panel(
        Text.assemble(usage_text, examples_text),
        title="📖 Help",
        title_align="left",
        style="bright_blue",
        border_style="bright_blue"
    )
    console.print(help_panel)

def print_warning(message: str):
    """Print warning messages"""
    console.print(f"[bold yellow]⚠️  {message}[/bold yellow]")

def print_success(message: str):
    """Print success messages"""
    console.print(f"[bold bright_green]✅ {message}[/bold bright_green]")

def print_info(message: str):
    """Print info messages"""
    console.print(f"[dim bright_white]ℹ️  {message}[/dim bright_white]")

def get_user_input() -> tuple[str, bool]:
    """Get user input in an interactive way"""
    console.print("[bright_yellow]💬 Enter your prompt:[/bright_yellow]")
    console.print("[dim](type 'help' for commands or 'quit' to exit)[/dim]\n")
    
    while True:
        try:
            user_input = Prompt.ask(
                "[bright_cyan]❯[/bright_cyan]",
                default="",
                show_default=False
            ).strip()
            
            if not user_input:
                console.print("[red]⚠️  Please enter a prompt[/red]")
                continue
            
            if user_input.lower() in ['help', '--help', '-h']:
                print_usage()
                console.print()  # Add spacing
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                console.print("[bright_yellow]👋 Goodbye![/bright_yellow]")
                sys.exit(0)
            
            # Show the query in a nice format
            query_panel = Panel(
                user_input,
                title="📝 Your Query",
                title_align="left",
                style="bright_cyan",
                border_style="bright_cyan"
            )
            console.print(query_panel)
            
            # Ask for verbose mode only once per session
            verbose = Confirm.ask(
                "[dim]Enable verbose output for this query?[/dim]",
                default=False
            )
            
            console.print()  # Add spacing before processing
            return user_input, verbose
            
        except KeyboardInterrupt:
            # Don't exit immediately on Ctrl+C, let main handle it
            raise
        except EOFError:
            console.print("\n[bright_yellow]👋 Goodbye![/bright_yellow]")
            sys.exit(0)