# Instant MCP

A powerful CLI tool for managing and running Model Context Protocol (MCP) servers with automatic discovery, configuration management, and Git workflow automation.

## Features

- 🚀 **Automatic Server Discovery**: Automatically discovers and registers MCP servers from Python files
- 🎯 **Clean CLI Interface**: Modern command-line interface built with Cleo framework
- ⚙️ **Configuration Management**: Flexible configuration system with path management
- 📤 **Export Capabilities**: Export configurations to Cursor IDE and other formats
- 🔄 **Git Workflow Automation**: Advanced Git tools for version management and release automation
- 🔧 **Extensible Architecture**: Easy to add new servers and tools

## Installation

```bash
pip install git+https://github.com/crimson206/instant-mcp
```

> 📖 **Detailed installation guide**: [docs/installation.md](docs/installation.md)

## Quick Start

### 1. List Available Servers

```bash
instant-mcp servers
```

### 2. Run a Server

```bash
# Run a specific server
instant-mcp run math_mcp

# Or use direct server name (backward compatibility)
instant-mcp math_mcp
```

### 3. Configure Target Path

```bash
# Show current configuration
instant-mcp config:show

# Set custom server directory
instant-mcp config:set-target-path /path/to/your/servers

# Reset to defaults
instant-mcp config:reset
```

### 4. Export Configurations

```bash
# Export to Cursor IDE format
instant-mcp export:cursor

# Preview configuration without writing
instant-mcp export:preview

# Export detailed configuration
instant-mcp export:detailed
```

## Example Servers

### Math MCP Server
Basic mathematical calculations (`calculate`, `square_root`, `factorial`)

### Text Server  
Text processing tools (`reverse_text`, `count_words`)

### GitHub Workflow Server
Git workflow automation (`show_changes_since_latest_tag`, `write_release_commit_message`)

> 📖 **Creating custom servers**: [docs/creating-servers.md](docs/creating-servers.md)  
> 📖 **Git workflow guide**: [docs/git-workflow.md](docs/git-workflow.md)  
> 🤖 **Using with Cursor AI**: [docs/cursor-ai-usage.md](docs/cursor-ai-usage.md)

## Configuration

```bash
# Show current configuration
instant-mcp config:show

# Set custom server directory
instant-mcp config:set-target-path /path/to/your/servers

# Reset to defaults
instant-mcp config:reset
```

## Cursor IDE Integration

Export your MCP configuration for Cursor IDE:

```bash
instant-mcp export:cursor
```

This creates `.cursor/mcp.json` with all discovered servers.

## Command Reference

```bash
# Server management
instant-mcp servers              # List available servers
instant-mcp run <server>         # Run specific server

# Configuration  
instant-mcp config:show          # Show current config
instant-mcp config:set-target-path <path>
instant-mcp config:reset

# Export
instant-mcp export:cursor        # Export to Cursor IDE
instant-mcp export:preview       # Preview configuration
```

## Contributing

1. Fork the repository
2. Create a feature branch  
3. Make your changes
4. Submit a pull request

## License

MIT License

## Changelog

### v0.1.1 (Latest)
- Major CLI refactoring from argparse to Cleo framework
- Added Git workflow automation tools
- Improved configuration system with absolute path handling
- Enhanced MCP server integration
- Added comprehensive export functionality

### v0.1.0
- Initial release
- Basic server discovery and execution
- Configuration management
- Export to Cursor IDE format