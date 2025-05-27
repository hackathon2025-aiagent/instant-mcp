#!/usr/bin/env python3
"""
Main entry point for instant-mcp servers using Cleo.
"""

from cleo.application import Application
from cleo.commands.command import Command
from cleo.helpers import argument, option

from .discovery import discover_mcp_servers
from .server_builder import run_server
from .config import show_config, set_target_path, reset_config, get_target_path
from .export import export_cursor_config, export_detailed_config, show_export_preview


class ServersCommand(Command):
    """
    List all available MCP servers
    
    servers
    """
    
    name = "servers"
    description = "List all available MCP servers"
    
    def handle(self):
        servers = discover_mcp_servers()
        if not servers:
            self.line("No servers found.")
            self.line(f"Current target path: {get_target_path()}")
            return
        
        self.line("Available servers:")
        for server_name, config in sorted(servers.items()):
            server_type = config["type"]
            instructions = config["instructions"]
            tools = ", ".join(config["tools"])
            self.line(f"  - <info>{server_name}</info> ({server_type}): {instructions}")
            self.line(f"    Tools: {tools}")
        
        self.line(f"\nCurrent target path: {get_target_path()}")


class RunCommand(Command):
    name = "run"
    description = "Run a specific MCP server"
    arguments = [
        argument(
            "server",
            description="The name of the server to run"
        )
    ]
    
    def handle(self):
        server_name = self.argument("server")
        servers = discover_mcp_servers()
        
        if server_name not in servers:
            self.line_error(f"Error: Server '<error>{server_name}</error>' not found.")
            self.line_error(f"Available servers: {', '.join(sorted(servers.keys()))}")
            return 1
        
        try:
            self.line_error(f"Starting <info>{server_name}</info>...")
            run_server(server_name)
        except Exception as e:
            self.line_error(f"Error running {server_name}: {e}")
            return 1


class ConfigShowCommand(Command):
    """
    Show current configuration
    
    config:show
    """
    
    name = "config:show"
    description = "Show current configuration settings"
    
    def handle(self):
        show_config()


class ConfigSetTargetPathCommand(Command):
    name = "config:set-target-path"
    description = "Set target path for server discovery"
    arguments = [
        argument(
            "path",
            description="The path to set as target directory"
        )
    ]
    
    def handle(self):
        path = self.argument("path")
        set_target_path(path)


class ConfigResetCommand(Command):
    """
    Reset configuration to defaults
    
    config:reset
    """
    
    name = "config:reset"
    description = "Reset configuration to default values"
    
    def handle(self):
        reset_config()


class ExportCursorCommand(Command):
    """
    Export to Cursor MCP format (.cursor/mcp.json)
    
    export:cursor
    """
    
    name = "export:cursor"
    description = "Export configuration to Cursor MCP format (.cursor/mcp.json)"
    
    def handle(self):
        export_cursor_config()


class ExportDetailedCommand(Command):
    """
    Export detailed configuration with server info
    
    export:detailed
    """
    
    name = "export:detailed"
    description = "Export detailed configuration with server information"
    
    def handle(self):
        export_detailed_config()


class ExportPreviewCommand(Command):
    """
    Preview export configuration without writing files
    
    export:preview
    """
    
    name = "export:preview"
    description = "Preview export configuration without writing files"
    
    def handle(self):
        show_export_preview()


def create_application():
    """Create and configure the Cleo application."""
    app = Application("instant-mcp", "0.1.0")
    
    # Add commands
    app.add(ServersCommand())
    app.add(RunCommand())
    app.add(ConfigShowCommand())
    app.add(ConfigSetTargetPathCommand())
    app.add(ConfigResetCommand())
    app.add(ExportCursorCommand())
    app.add(ExportDetailedCommand())
    app.add(ExportPreviewCommand())
    
    return app


def main():
    """Main entry point."""
    import sys
    
    # If no arguments provided, show list of servers
    if len(sys.argv) == 1:
        servers = discover_mcp_servers()
        if servers:
            # If we have servers, try to run the first argument as a server name
            app = create_application()
            app.run()
        else:
            # No servers found, show help
            app = create_application()
            app.run()
        return
    
    # Check if first argument is a server name (for backward compatibility)
    first_arg = sys.argv[1]
    servers = discover_mcp_servers()
    
    # If first argument is a known server name and no command prefix, run it directly
    if first_arg in servers and not first_arg.startswith('-'):
        try:
            print(f"Starting {first_arg}...", file=sys.stderr)
            run_server(first_arg)
        except Exception as e:
            print(f"Error running {first_arg}: {e}", file=sys.stderr)
            sys.exit(1)
        return
    
    # Otherwise, use normal Cleo command processing
    app = create_application()
    app.run()


if __name__ == "__main__":
    main() 