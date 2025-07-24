# AI-AGENT

A simple version of something like Cursor/Zed's Agentic Mode, or Claude Code. This is a basic demonstration of an AI coding assistant that can interact with your filesystem, please note this isn't at the level of their sophisticated agents, it's just a learning demo!

*Here will be a demo gif*

## Features

- 🤖 **Interactive Chat Interface** - Continuous conversation mode with rich terminal UI
- 📁 **File System Operations** - List, read, and write files in your project
- 🐍 **Python Script Execution** - Run Python files with arguments directly from the agent
- 🎨 **Rich Terminal UI** - Beautiful interface with syntax highlighting and panels
- 📂 **Configurable Working Directory** - Set custom working directories for your projects

## What It Can Do

- Analyze your codebase structure
- Read and understand existing files
- Create new files or modify existing ones
- Execute Python scripts and handle errors
- Provide coding assistance and debugging help
- Navigate project directories

## Working Directory Configuration

**Important:** By default, the AI agent operates in the `/calculator` directory. This means all file operations (reading, writing, executing) will be performed relative to this location. This provides an easy way to test the agent.

### Changing the Working Directory

To change the default working directory, you need to modify the configuration in the `config.py` file:

```python
# In config.py, look for the working directory setting
WORKING_DIRECTORY = "/calculator"  # Change this to your desired path
```

You can set this to:
- An absolute path: `WORKING_DIRECTORY = "/path/to/your/project"`
- A relative path: `WORKING_DIRECTORY = "./my-project"`
- Current directory: `WORKING_DIRECTORY = "."`

**Note:** Make sure the directory exists before running the agent, or the agent may encounter errors when trying to perform file operations.

## Demo The Project

### 1. Clone the repository:
```bash
git clone https://github.com/ABT099/ai-agent
cd ai-agent
```

### 2. Install dependencies with uv:
```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install project dependencies
uv sync
```

### 3. Set up your API key:
```bash
# Create a .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

### 5. Run the project:
```bash
uv run main.py
```

## Usage Examples

Once running, you can ask the agent to help with various tasks:

- `"analyze the main.py file"`
- `"create a simple calculator script"`
- `"show me all Python files in this project"`
- `"fix the bug in my script.py file"`
- `"create a README for this project"`

Type `help` for available commands or `quit` to exit.

## Requirements

- Python 3.8+
- [uv](https://docs.astral.sh/uv/) package manager
- Google Gemini API key

## Limitations

This is a simple demonstration project with several limitations:

- Basic error handling compared to production tools
- Limited to file operations and Python execution
- No advanced code understanding or refactoring capabilities
- Single-threaded execution
- No git integration or advanced project management
- Works within a single configured directory (though this can be changed)

## Contributing

Feel free to fork and experiment! This is meant to be a learning project to understand how AI coding agents work at a basic level.