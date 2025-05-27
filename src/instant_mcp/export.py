import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from .discovery import discover_mcp_servers

def export_cursor_config(output_path: Optional[str] = None, base_command: str = "instant-mcp") -> None:
    """
    Export discovered servers to Cursor MCP configuration format.
    
    Args:
        output_path: Path to save the mcp.json file. If None, saves to .cursor/mcp.json
        base_command: Base command to use for server execution
    """
    # Discover all available servers
    servers = discover_mcp_servers()
    
    if not servers:
        print("No servers found to export.")
        return
    
    # Build MCP configuration
    mcp_config = {
        "mcpServers": {}
    }
    
    for server_name, server_info in servers.items():
        # Use proper command/args format and add metadata
        mcp_config["mcpServers"][server_name] = {
            "command": base_command,
            "args": [server_name],
            "description": server_info['instructions'],
            "tools": server_info['tools']
        }
    
    # Determine output path
    if output_path is None:
        output_path = ".cursor/mcp.json"
    
    output_file = Path(output_path)
    
    # Create directory if it doesn't exist
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Write the configuration
    try:
        with open(output_file, 'w') as f:
            json.dump(mcp_config, f, indent=2)
        
        print(f"MCP configuration exported to: {output_file}")
        print(f"Found {len(servers)} servers:")
        for server_name, server_info in servers.items():
            print(f"  - {server_name}: {server_info['instructions']}")
        
    except IOError as e:
        print(f"Error writing configuration file: {e}")

def export_detailed_config(output_path: Optional[str] = None, base_command: str = "instant-mcp") -> None:
    """
    Export detailed MCP configuration with server descriptions and tools.
    
    Args:
        output_path: Path to save the detailed config file
        base_command: Base command to use for server execution
    """
    # Discover all available servers
    servers = discover_mcp_servers()
    
    if not servers:
        print("No servers found to export.")
        return
    
    # Build detailed configuration
    detailed_config = {
        "mcpServers": {},
        "serverDetails": {}
    }
    
    for server_name, server_info in servers.items():
        # Basic MCP config with proper format
        detailed_config["mcpServers"][server_name] = {
            "command": base_command,
            "args": [server_name],
            "description": server_info['instructions'],
            "tools": server_info['tools']
        }
        
        # Detailed information
        detailed_config["serverDetails"][server_name] = {
            "name": server_info["name"],
            "type": server_info["type"],
            "instructions": server_info["instructions"],
            "tools": server_info["tools"],
            "file_path": server_info["file_path"]
        }
    
    # Determine output path
    if output_path is None:
        output_path = "mcp-detailed.json"
    
    output_file = Path(output_path)
    
    # Create directory if it doesn't exist
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Write the configuration
    try:
        with open(output_file, 'w') as f:
            json.dump(detailed_config, f, indent=2)
        
        print(f"Detailed MCP configuration exported to: {output_file}")
        print(f"Found {len(servers)} servers with detailed information.")
        
    except IOError as e:
        print(f"Error writing detailed configuration file: {e}")

def show_export_preview() -> None:
    """Show a preview of what would be exported without writing files."""
    servers = discover_mcp_servers()
    
    if not servers:
        print("No servers found.")
        return
    
    print("Export Preview:")
    print("=" * 50)
    
    mcp_config = {
        "mcpServers": {}
    }
    
    for server_name, server_info in servers.items():
        mcp_config["mcpServers"][server_name] = {
            "command": "instant-mcp",
            "args": [server_name],
            "description": server_info['instructions'],
            "tools": server_info['tools']
        }
    
    print(json.dumps(mcp_config, indent=2))
    print("=" * 50)
    print(f"Total servers: {len(servers)}")
    
    print("\nServer Details:")
    for server_name, server_info in servers.items():
        print(f"  {server_name} ({server_info['type']}):")
        print(f"    Instructions: {server_info['instructions']}")
        print(f"    Tools: {', '.join(server_info['tools'])}")
        print(f"    File: {server_info['file_path']}")
        print() 