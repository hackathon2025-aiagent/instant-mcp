# Git Workflow Automation

The GitHub server provides powerful Git workflow automation tools for version management and release processes.

## Features

- Automatic version tag detection
- Diff generation between tags and current state
- Automated commit message generation with change summaries
- Force commit option for clean comparisons
- Absolute path validation for reliability

## Available Tools

### show_changes_since_latest_tag

Compare current state with the latest version tag.

```python
show_changes_since_latest_tag(
    repo_path="/absolute/path/to/repo",
    include_working_dir="true",  # Include uncommitted changes
    force_commit="true"          # Auto-commit before comparison
)
```

**Parameters:**
- `repo_path`: ABSOLUTE path to git repository (required)
- `include_working_dir`: "true" to include uncommitted changes, "false" for committed only
- `force_commit`: "true" to auto-commit all changes before comparison

**Example Output:**
```
=== Version Tag Analysis ===
Repository path: /home/user/my-project
✅ Auto-committed all changes before comparison
Comparison mode: working directory (includes uncommitted changes)

Latest version tag: v0.1.0

Commits since v0.1.0:
abc123f Add new feature
def456g Fix bug in parser
ghi789h Update documentation

Diff since v0.1.0:
[Detailed diff output showing all changes]
```

### write_release_commit_message

Generate and write release commit messages with automatic change summaries.

```python
write_release_commit_message(
    repo_path="/absolute/path/to/repo",
    title="Release v1.0.0: Major update",
    body="Detailed description of changes..."
)
```

**Parameters:**
- `repo_path`: ABSOLUTE path to git repository (required)
- `title`: Commit title/subject line (required)
- `body`: Optional detailed description

**Features:**
- Automatically includes file changes since latest tag
- Adds commit summaries
- Uses emoji indicators for different change types:
  - 🔄 Modified files
  - ✅ Added files
  - ❌ Deleted files
  - 📝 Renamed files
  - 📋 Copied files

## Usage Examples

### Basic Workflow

1. **Check current changes:**
```bash
instant-mcp run github
# Use show_changes_since_latest_tag with your repo path
```

2. **Prepare release commit:**
```bash
# Use write_release_commit_message with title and description
```

### Advanced Workflow

1. **Auto-commit and compare:**
```python
# Force commit all changes before comparison
show_changes_since_latest_tag(
    repo_path="/home/user/my-project",
    include_working_dir="false",  # Only committed changes
    force_commit="true"           # Commit everything first
)
```

2. **Generate comprehensive release message:**
```python
write_release_commit_message(
    repo_path="/home/user/my-project",
    title="Release v1.2.0: Enhanced Git workflow automation",
    body="""This release introduces significant improvements to Git workflow automation.

## New Features
- Auto-commit functionality for clean tag comparisons
- Enhanced diff output with file change indicators
- Improved error handling and validation

## Bug Fixes
- Fixed path resolution issues
- Improved commit message formatting

## Breaking Changes
- Requires absolute paths for all Git operations
"""
)
```

## Version Tag Detection

The system automatically detects version tags using these patterns:

- `v1.0.0`, `v0.1.0` (semantic versioning with 'v' prefix)
- `1.0.0`, `0.1.0` (semantic versioning without prefix)
- `v1.0`, `1.0` (major.minor format)
- `v1.0.0-alpha`, `v1.0.0-beta.1` (pre-release versions)

## Best Practices

### Repository Setup

1. **Use semantic versioning** for tags (v1.0.0, v1.1.0, etc.)
2. **Tag releases consistently** to enable proper comparison
3. **Use absolute paths** for all Git operations

### Workflow Integration

1. **Before creating a release:**
   - Use `show_changes_since_latest_tag` to review changes
   - Set `force_commit="true"` to ensure clean comparison

2. **When creating release commits:**
   - Use descriptive titles following conventional commit format
   - Include detailed body with breaking changes and new features
   - Let the tool automatically add file changes and commit summaries

### Example Release Process

```bash
# 1. Review changes since last tag
instant-mcp run github
# Call show_changes_since_latest_tag with force_commit="true"

# 2. Create release commit with auto-generated details
# Call write_release_commit_message with comprehensive title and body

# 3. Create and push tag
git tag v1.1.0
git push origin v1.1.0

# 4. Create GitHub release (optional)
gh release create v1.1.0 --generate-notes
```

## Troubleshooting

### Common Issues

1. **"Only absolute paths are supported"**
   - Always use absolute paths like `/home/user/project`
   - Avoid relative paths like `./project` or `../project`

2. **"Not a git repository"**
   - Ensure the path points to a directory containing `.git`
   - Check that you have proper permissions

3. **"No version tags found"**
   - Create at least one version tag: `git tag v0.1.0`
   - Ensure tags follow supported patterns

### Debug Tips

- Use `git tag --list` to see all tags in your repository
- Use `git log --oneline` to see recent commits
- Verify paths with `ls -la /absolute/path/to/repo/.git` 