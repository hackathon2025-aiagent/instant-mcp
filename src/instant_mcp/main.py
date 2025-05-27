#!/usr/bin/env python3
"""
Main entry point for instant-mcp servers.
Usage:
    instant-mcp utils_mcp         # Run utils server
    instant-mcp --list            # List available servers
    instant-mcp config --show     # Show current configuration
    instant-mcp config --set-target-path /path/to/servers
    instant-mcp export --cursor   # Export to .cursor/mcp.json
    instant-mcp export --preview  # Preview export configuration

"""

import sys
import argparse
from .discovery import discover_mcp_servers
from .server_builder import run_server
from .config import show_config, set_target_path, reset_config, get_target_path
from .export import export_cursor_config, export_detailed_config, show_export_preview


def list_servers():
    """List all available servers."""
    servers = discover_mcp_servers()
    if not servers:
        print("No servers found.")
        print(f"Current target path: {get_target_path()}")
        return
    
    print("Available servers:")
    for server_name, config in sorted(servers.items()):
        server_type = config["type"]
        instructions = config["instructions"]
        tools = ", ".join(config["tools"])
        print(f"  - {server_name} ({server_type}): {instructions}")
        print(f"    Tools: {tools}")
    
    print(f"\nCurrent target path: {get_target_path()}")

def handle_config_command(args):
    """Handle config subcommands."""
    parser = argparse.ArgumentParser(prog='instant-mcp config')
    parser.add_argument('--show', action='store_true', help='Show current configuration')
    parser.add_argument('--set-target-path', type=str, help='Set target path for server discovery')
    parser.add_argument('--reset', action='store_true', help='Reset configuration to defaults')
    
    config_args = parser.parse_args(args)
    
    if config_args.show:
        show_config()
    elif config_args.set_target_path:
        set_target_path(config_args.set_target_path)
    elif config_args.reset:
        reset_config()
    else:
        parser.print_help()

def handle_export_command(args):
    """Handle export subcommands."""
    parser = argparse.ArgumentParser(prog='instant-mcp export')
    parser.add_argument('--cursor', action='store_true', help='Export to Cursor MCP format (.cursor/mcp.json)')
    parser.add_argument('--detailed', action='store_true', help='Export detailed configuration with server info')
    parser.add_argument('--preview', action='store_true', help='Preview export configuration without writing files')
    parser.add_argument('--output', type=str, help='Custom output file path')
    
    export_args = parser.parse_args(args)
    
    if export_args.cursor:
        output_path = export_args.output if export_args.output else None
        export_cursor_config(output_path)
    elif export_args.detailed:
        output_path = export_args.output if export_args.output else None
        export_detailed_config(output_path)
    elif export_args.preview:
        show_export_preview()
    else:
        parser.print_help()



def main():
    # Discover servers first to get available choices
    servers = discover_mcp_servers()
    server_names = list(servers.keys())
    
    # Manual argument parsing to handle subcommands and server names
    if len(sys.argv) == 1:
        # No arguments, show help
        show_help(server_names)
        return
    
    first_arg = sys.argv[1]
    
    # Handle --list
    if first_arg == '--list':
        list_servers()
        return
    
    # Handle --help
    if first_arg in ['-h', '--help']:
        show_help(server_names)
        return
    
    # Handle config subcommand
    if first_arg == 'config':
        handle_config_command(sys.argv[2:])
        return
    
    # Handle export subcommand
    if first_arg == 'export':
        handle_export_command(sys.argv[2:])
        return
    

    
    # Otherwise, treat as server name
    server_name = first_arg
    
    # Check if the server exists
    if server_name not in server_names:
        print(f"Error: Server '{server_name}' not found.")
        print(f"Available servers: {', '.join(sorted(server_names))}")
        sys.exit(1)
    
    # Run the selected server
    try:
        print(f"Starting {server_name}...", file=sys.stderr)
        run_server(server_name)
    except Exception as e:
        print(f"Error running {server_name}: {e}", file=sys.stderr)
        sys.exit(1)

def show_help(server_names):
    """Show help message."""
    print("Instant MCP Server Launcher")
    print()
    print("Usage:")
    print("  instant-mcp <server_name>        # Run a specific server")
    print("  instant-mcp --list              # List available servers")
    print("  instant-mcp config --show       # Show current configuration")
    print("  instant-mcp config --set-target-path PATH")
    print("  instant-mcp config --reset      # Reset configuration")
    print("  instant-mcp export --preview    # Preview MCP configuration")
    print("  instant-mcp export --cursor     # Export to .cursor/mcp.json")
    print("  instant-mcp export --detailed   # Export detailed configuration")

    print()
    print(f"Current target path: {get_target_path()}")
    print(f"Available servers: {', '.join(sorted(server_names))}")
    print()
    print("Server Discovery:")
    print("  - Files ending with _mcp.py are automatically detected")
    print("  - Files with SeverProtocol definitions are registered")

if __name__ == "__main__":
    main() 