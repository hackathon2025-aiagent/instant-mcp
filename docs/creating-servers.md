# Creating Custom Servers

## Overview

Instant MCP supports three different methods for creating custom servers. Each method has its own use cases and benefits.

## Method 1: MCP File Format

The simplest way to create a server. Create a Python file ending with `_mcp.py`:

```python
# my_server_mcp.py
def my_function(param: str) -> str:
    """My custom function."""
    return f"Hello, {param}!"

def calculate_sum(a: int, b: int) -> int:
    """Calculate sum of two numbers."""
    return a + b

# Server configuration
name = "my_server"
instructions = "My custom MCP server"
tools = ["my_function", "calculate_sum"]
```

## Method 2: Protocol Definition

Create a server with ServerProtocol class for more advanced features:

```python
# my_protocol_server.py
from mcp.server import Server
from mcp.types import Tool

app = Server("my-protocol-server")

@app.tool()
def my_tool(text: str) -> str:
    """Process text."""
    return text.upper()

@app.tool()
def reverse_text(text: str) -> str:
    """Reverse the input text."""
    return text[::-1]

# Server configuration
name = "my_protocol_server"
instructions = "Server with protocol definition"
tools = ["my_tool", "reverse_text"]
```

## Method 3: Config File Format

For complex servers with external dependencies:

```python
# my_config_server.py
import subprocess
import os
from typing import Optional

def my_git_tool(repo_path: str) -> str:
    """Git operations tool."""
    try:
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True,
            check=True,
            cwd=repo_path
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"

def file_operations(file_path: str, operation: str) -> str:
    """File system operations."""
    if operation == "read":
        try:
            with open(file_path, 'r') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {e}"
    elif operation == "exists":
        return str(os.path.exists(file_path))
    else:
        return "Unknown operation"

# Server configuration
name = "my_config_server"
instructions = "Server with config file format"
tools = ["my_git_tool", "file_operations"]
```

## Server Configuration Variables

All servers must include these configuration variables:

- `name`: Unique identifier for the server
- `instructions`: Description of what the server does
- `tools`: List of function names to expose as tools

## Best Practices

### Function Documentation

Always include docstrings for your functions:

```python
def my_function(param: str) -> str:
    """
    Brief description of what the function does.
    
    Args:
        param: Description of the parameter
        
    Returns:
        Description of the return value
    """
    return f"Result: {param}"
```

### Error Handling

Include proper error handling:

```python
def safe_operation(data: str) -> str:
    """Safely process data with error handling."""
    try:
        # Your operation here
        result = data.upper()
        return result
    except Exception as e:
        return f"Error: {str(e)}"
```

### Type Hints

Use type hints for better integration:

```python
from typing import List, Dict, Optional

def process_list(items: List[str]) -> Dict[str, int]:
    """Process a list and return statistics."""
    return {
        "count": len(items),
        "total_length": sum(len(item) for item in items)
    }
```

## Testing Your Server

1. Place your server file in the `instant_servers/` directory
2. Run `instant-mcp servers` to verify it's discovered
3. Test with `instant-mcp run your_server_name`

## Advanced Features

### Async Functions

For I/O intensive operations:

```python
import asyncio
import aiohttp

async def fetch_data(url: str) -> str:
    """Fetch data from URL asynchronously."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

# Server configuration
name = "async_server"
instructions = "Server with async capabilities"
tools = ["fetch_data"]
```

### Complex Data Types

Handle complex input/output:

```python
from typing import Dict, List
import json

def process_json(json_data: str) -> Dict:
    """Process JSON data and return analysis."""
    try:
        data = json.loads(json_data)
        return {
            "keys": list(data.keys()) if isinstance(data, dict) else [],
            "type": type(data).__name__,
            "size": len(data) if hasattr(data, '__len__') else 0
        }
    except json.JSONDecodeError:
        return {"error": "Invalid JSON"}
```

## Deployment

Once your server is ready:

1. Test thoroughly with different inputs
2. Add comprehensive docstrings
3. Consider adding it to the main repository via pull request
4. Share with the community! 