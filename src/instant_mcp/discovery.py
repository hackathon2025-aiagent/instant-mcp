import importlib
import importlib.util
import inspect
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from .protocol import get_server_protocols, SeverProtocol
from .config import get_target_path

def discover_mcp_servers(target_path: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
    """
    Discover MCP servers from multiple sources:
    1. Files ending with _mcp.py
    2. Files containing SeverProtocol definitions (detected after import)
    3. Files with server configuration variables (name, instructions, tools)
    """
    servers = {}
    
    # Use config target_path if not provided
    if target_path is None:
        target_path = get_target_path()
    
    # Convert to Path object
    if target_path.startswith("./"):
        # Relative to current working directory (where the command is run)
        search_dir = Path.cwd() / target_path.replace("./", "")
    else:
        search_dir = Path(target_path)
    
    if not search_dir.exists():
        print(f"Warning: Target path does not exist: {search_dir}")
        return servers
    
    # Clear protocol registry to avoid conflicts
    from .protocol import _server_protocols
    _server_protocols.clear()
    
    # Add paths to sys.path temporarily for imports
    search_dir_str = str(search_dir)
    instant_mcp_path = str(Path(__file__).parent.parent)  # src directory
    
    paths_to_add = []
    if search_dir_str not in sys.path:
        sys.path.insert(0, search_dir_str)
        paths_to_add.append(search_dir_str)
    if instant_mcp_path not in sys.path:
        sys.path.insert(0, instant_mcp_path)
        paths_to_add.append(instant_mcp_path)
    
    try:
        # Store initial protocol state
        initial_protocols = set(_server_protocols.keys())
        
        # Load all Python files and track which ones register protocols
        file_to_protocol = {}
        
        for py_file in search_dir.glob("*.py"):
            if py_file.name.startswith("__"):
                continue
                
            try:
                # Store protocols before loading this file
                protocols_before = set(_server_protocols.keys())
                
                # Try to load the module (this might register SeverProtocol)
                module = _load_module_from_file(py_file)
                
                # Check what new protocols were registered
                protocols_after = set(_server_protocols.keys())
                new_protocols = protocols_after - protocols_before
                
                # Map file to any protocols it registered
                for protocol_name in new_protocols:
                    file_to_protocol[protocol_name] = py_file
                
                # If no protocol was registered, check if it's a regular server file
                if not new_protocols and _is_server_file(module):
                    server_name = py_file.stem
                    
                    # Get server configuration from module attributes
                    name = getattr(module, 'name', server_name)
                    instructions = getattr(module, 'instructions', f"Server: {server_name}")
                    tools = getattr(module, 'tools', [])
                    
                    # If tools is empty, auto-discover functions
                    if not tools:
                        tools = _discover_functions(module)
                    
                    # Determine server type
                    server_type = "mcp_file" if py_file.name.endswith("_mcp.py") else "config_file"
                    
                    servers[server_name] = {
                        "type": server_type,
                        "name": name,
                        "instructions": instructions,
                        "tools": tools,
                        "file_path": str(py_file)
                    }
                    
            except Exception as e:
                print(f"Warning: Could not load {py_file}: {e}")
        
        # Now process all registered protocols
        protocols = get_server_protocols()
        for protocol_name, protocol in protocols.items():
            # Find the file that registered this protocol
            protocol_file = file_to_protocol.get(protocol_name)
            if protocol_file:
                servers[protocol_name] = {
                    "type": "protocol",
                    "name": protocol.name,
                    "instructions": protocol.instructions,
                    "tools": protocol.tools,
                    "file_path": str(protocol_file)
                }
    
    finally:
        # Remove the added paths from sys.path
        for path in paths_to_add:
            if path in sys.path:
                sys.path.remove(path)
    
    return servers

def _is_server_file(module) -> bool:
    """Check if a module contains server configuration."""
    # Check for explicit server configuration
    has_name = hasattr(module, 'name')
    has_instructions = hasattr(module, 'instructions')
    has_tools = hasattr(module, 'tools')
    
    # Check for functions (potential tools)
    functions = _discover_functions(module)
    
    # It's a server file if it has explicit config OR has callable functions
    return (has_name or has_instructions or has_tools) or len(functions) > 0

def _load_module_from_file(file_path: Path):
    """Load a Python module from a file path."""
    module_name = file_path.stem
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec for {file_path}")
    
    module = importlib.util.module_from_spec(spec)
    # Add to sys.modules to make it available for imports
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def _discover_functions(module) -> List[str]:
    """Auto-discover callable functions in a module (excluding private and built-ins)."""
    functions = []
    for name, obj in inspect.getmembers(module):
        if (inspect.isfunction(obj) and 
            not name.startswith('_') and 
            obj.__module__ == module.__name__):
            functions.append(name)
    return functions 