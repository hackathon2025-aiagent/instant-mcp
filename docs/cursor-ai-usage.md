# Using Instant MCP with Cursor AI

## Important Considerations

When using instant-mcp tools through Cursor AI, especially for terminal operations and file system access, it's crucial to provide detailed context and absolute paths.

## Why Absolute Paths Matter

Cursor AI operates in an isolated environment and may not have access to your current working directory or environment variables. This can lead to:

- **Path resolution errors**: Relative paths like `./project` or `../folder` may not work as expected
- **Environment confusion**: AI doesn't know your current shell, working directory, or environment setup
- **Permission issues**: AI may not understand your file system permissions or access rights

## Best Practices

### 1. Always Use Absolute Paths

❌ **Don't do this:**
```bash
instant-mcp run github
# Then use: repo_path="./my-project"
```

✅ **Do this instead:**
```bash
instant-mcp run github
# Then use: repo_path="/home/username/projects/my-project"
```

### 2. Provide Full Context

When asking Cursor AI to help with instant-mcp operations, include:

- **Full absolute paths** to your repositories
- **Current working directory** if relevant
- **Environment details** (OS, shell, Python version)
- **Project structure** if needed

### 3. Example: Proper Git Workflow Request

❌ **Vague request:**
```
"Use the GitHub server to check changes since last tag"
```

✅ **Detailed request:**
```
"Use the GitHub server to check changes since last tag for my project at 
/home/username/projects/my-awesome-app. Set force_commit to true and 
include working directory changes."
```

### 4. Configuration Management

When setting up instant-mcp configuration:

```bash
# Be explicit about paths
instant-mcp config:set-target-path /home/username/my-custom-servers

# Verify the configuration
instant-mcp config:show
```

## Common Scenarios

### Git Workflow Automation

```python
# Always provide absolute paths
show_changes_since_latest_tag(
    repo_path="/home/username/projects/my-project",  # Absolute path
    include_working_dir="true",
    force_commit="true"
)
```

### Custom Server Development

```bash
# Specify exact location for custom servers
instant-mcp config:set-target-path /home/username/development/mcp-servers

# Verify server discovery
instant-mcp servers
```

### Cursor IDE Integration

```bash
# Export from specific project directory
cd /home/username/projects/my-project
instant-mcp export:cursor
```

## Troubleshooting AI Interactions

### When AI Commands Fail

1. **Check paths**: Ensure all paths are absolute and exist
2. **Verify permissions**: Make sure AI has access to specified directories
3. **Provide context**: Include your current working directory and environment
4. **Test manually**: Try commands manually first to verify they work

### Example Debug Session

```bash
# 1. Show current location
pwd
# Output: /home/username

# 2. List available servers with full context
instant-mcp servers
# This shows the current target path

# 3. Use absolute paths in all operations
instant-mcp run github
# Then provide: repo_path="/home/username/projects/my-project"
```

## Best Practices Summary

1. **Always use absolute paths** for all file and directory references
2. **Provide full context** when requesting AI assistance
3. **Verify paths exist** before using them in commands
4. **Test commands manually** before asking AI to execute them
5. **Include environment details** (OS, shell, working directory) in requests

This approach ensures reliable and predictable behavior when using instant-mcp tools through Cursor AI. 