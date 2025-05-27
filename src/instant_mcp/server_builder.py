import importlib
import importlib.util
import sys
from pathlib import Path
from typing import Any, Dict
from mcp.server.fastmcp import FastMCP
from .discovery import discover_mcp_servers, _load_module_from_file

def build_server(server_name: str) -> FastMCP:
    """Build an MCP server from discovered server configuration."""
    servers = discover_mcp_servers()
    
    if server_name not in servers:
        raise ValueError(f"Server '{server_name}' not found")
    
    server_config = servers[server_name]
    
    # Create FastMCP server
    mcp = FastMCP(
        server_config["name"],
        instructions=server_config["instructions"],
    )
    
    # Load the module from file path
    file_path = Path(server_config["file_path"])
    try:
        module = _load_module_from_file(file_path)
    except Exception as e:
        raise ImportError(f"Could not load module from {file_path}: {e}")
    
    # Register tools from the module
    for tool_name in server_config["tools"]:
        if hasattr(module, tool_name):
            tool_func = getattr(module, tool_name)
            if callable(tool_func):
                # Register the function as a tool
                mcp.tool()(tool_func)
            else:
                raise ValueError(f"'{tool_name}' is not callable in module {file_path}")
        else:
            raise ValueError(f"Tool '{tool_name}' not found in module {file_path}")
    
    return mcp

def run_server(server_name: str):
    """Build and run a server."""
    import asyncio
    
    mcp = build_server(server_name)
    asyncio.run(mcp.run(transport="stdio")) 