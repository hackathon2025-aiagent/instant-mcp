import subprocess
import re
import os
from typing import Optional, List, Tuple


def is_version_tag(tag: str) -> bool:
    """
    Check if a tag is a version tag (e.g., v1.0.0, v0.1.0, 1.2.3, etc.)
    """
    # Common version patterns: v1.0.0, v0.1.0, 1.2.3, v1.0, etc.
    version_patterns = [
        r'^v?\d+\.\d+\.\d+$',  # v1.0.0 or 1.0.0
        r'^v?\d+\.\d+$',       # v1.0 or 1.0
        r'^v?\d+\.\d+\.\d+-.+$',  # v1.0.0-alpha, v1.0.0-beta.1
    ]
    
    for pattern in version_patterns:
        if re.match(pattern, tag):
            return True
    return False


def get_all_version_tags(repo_path: str = ".") -> List[str]:
    """
    Get all version tags from the repository, sorted by creation date (newest first)
    """
    try:
        # Get all tags sorted by creation date
        result = subprocess.run(
            ['git', 'tag', '--sort=-creatordate'],
            capture_output=True,
            text=True,
            check=True,
            cwd=repo_path
        )
        
        all_tags = result.stdout.strip().split('\n')
        if all_tags == ['']:
            return []
        
        # Filter only version tags
        version_tags = [tag for tag in all_tags if is_version_tag(tag)]
        return version_tags
        
    except subprocess.CalledProcessError as e:
        print(f"Error getting tags: {e}")
        return []


def get_latest_version_tag(repo_path: str = ".") -> Optional[str]:
    """
    Get the latest version tag from the repository
    """
    version_tags = get_all_version_tags(repo_path)
    return version_tags[0] if version_tags else None


def get_diff_from_latest_tag(repo_path: str = ".", include_working_dir: bool = True) -> Tuple[Optional[str], str]:
    """
    Get the diff between the latest version tag and current state
    
    Args:
        repo_path: Path to the git repository
        include_working_dir: If True, compare with working directory (includes uncommitted changes)
                           If False, compare with HEAD (committed changes only)
    
    Returns: (latest_tag, diff_output)
    """
    latest_tag = get_latest_version_tag(repo_path)
    
    if not latest_tag:
        return None, "No version tags found in repository"
    
    try:
        if include_working_dir:
            # Compare with working directory (includes uncommitted changes)
            cmd = ['git', 'diff', latest_tag]
        else:
            # Compare with HEAD (committed changes only)
            cmd = ['git', 'diff', f'{latest_tag}..HEAD']
            
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            cwd=repo_path
        )
        
        return latest_tag, result.stdout
        
    except subprocess.CalledProcessError as e:
        return latest_tag, f"Error getting diff: {e}"


def get_commit_summary_from_latest_tag(repo_path: str = ".") -> Tuple[Optional[str], str]:
    """
    Get a summary of commits between the latest version tag and current HEAD
    Returns: (latest_tag, commit_summary)
    """
    latest_tag = get_latest_version_tag(repo_path)
    
    if not latest_tag:
        return None, "No version tags found in repository"
    
    try:
        # Get commit summary between latest tag and HEAD
        result = subprocess.run(
            ['git', 'log', f'{latest_tag}..HEAD', '--oneline'],
            capture_output=True,
            text=True,
            check=True,
            cwd=repo_path
        )
        
        return latest_tag, result.stdout
        
    except subprocess.CalledProcessError as e:
        return latest_tag, f"Error getting commit summary: {e}"


def prepare_commit_with_message(repo_path: str, title: str, body: str = ""):
    """
    Prepare a commit by staging all changes and setting up commit message.
    Typically used after running show_changes_since_latest_tag to review changes.
    
    Args:
        repo_path: ABSOLUTE path to the git repository (relative paths not supported)
        title: Commit title/subject line
        body: Optional commit body with detailed description
    
    Returns:
        Status message indicating success or failure
    """
    # Validate that absolute path is provided
    if not os.path.isabs(repo_path):
        return f"Error: Only absolute paths are supported. Provided path '{repo_path}' is relative."
    
    # Check if the path exists and is a directory
    if not os.path.exists(repo_path):
        return f"Error: Repository path '{repo_path}' does not exist"
    
    if not os.path.isdir(repo_path):
        return f"Error: Repository path '{repo_path}' is not a directory"
    
    # Check if it's a git repository
    git_dir = os.path.join(repo_path, '.git')
    if not os.path.exists(git_dir):
        return f"Error: '{repo_path}' is not a git repository"
    
    try:
        # Stage all changes (git add .)
        add_result = subprocess.run(
            ['git', 'add', '.'],
            capture_output=True,
            text=True,
            check=True,
            cwd=repo_path
        )
        
        # Prepare commit command with -m options
        commit_cmd = ['git', 'commit', '-m', title]
        
        # Add body as separate -m if provided
        if body.strip():
            commit_cmd.extend(['-m', body])
        
        # Run git commit with -m options
        commit_result = subprocess.run(
            commit_cmd,
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        
        # Prepare display message for user
        commit_message = title
        if body.strip():
            commit_message += f"\n\n{body}"
        
        result_lines = []
        result_lines.append("=== Commit Process Complete ===")
        result_lines.append(f"Repository: {os.path.abspath(repo_path)}")
        result_lines.append(f"All changes have been staged (git add .)")
        result_lines.append("")
        
        if commit_result.returncode == 0:
            result_lines.append("✅ Commit successful!")
            result_lines.append("")
            result_lines.append("Commit message used:")
            result_lines.append("-" * 40)
            result_lines.append(commit_message)
            result_lines.append("-" * 40)
            
            # Show commit output
            if commit_result.stdout.strip():
                result_lines.append("")
                result_lines.append("Git output:")
                result_lines.append(commit_result.stdout.strip())
        else:
            result_lines.append("❌ Commit was cancelled or failed")
            if commit_result.stderr.strip():
                result_lines.append("")
                result_lines.append("Error details:")
                result_lines.append(commit_result.stderr.strip())
            
            result_lines.append("")
            result_lines.append("The commit message was prepared as:")
            result_lines.append("-" * 40)
            result_lines.append(commit_message)
            result_lines.append("-" * 40)
            result_lines.append("")
            result_lines.append("You can retry with: git commit")
        
        return "\n".join(result_lines)
        
    except subprocess.CalledProcessError as e:
        return f"Error during commit process: {e}"
    except IOError as e:
        return f"Error writing commit message: {e}"


def show_changes_since_latest_tag(repo_path: str, include_working_dir: str = "true"):
    """
    Display changes since the latest version tag
    
    Args:
        repo_path: ABSOLUTE path to the git repository (relative paths not supported)
        include_working_dir: "true" to include uncommitted changes (recommended), 
                           "false" to show only committed changes
    """
    # Convert string parameter to boolean
    include_working = include_working_dir.lower() == "true"
    
    # Validate that absolute path is provided
    if not os.path.isabs(repo_path):
        return f"Error: Only absolute paths are supported. Provided path '{repo_path}' is relative."
    
    # Check if the path exists and is a directory
    if not os.path.exists(repo_path):
        return f"Error: Repository path '{repo_path}' does not exist"
    
    if not os.path.isdir(repo_path):
        return f"Error: Repository path '{repo_path}' is not a directory"
    
    # Check if it's a git repository
    git_dir = os.path.join(repo_path, '.git')
    if not os.path.exists(git_dir):
        return f"Error: '{repo_path}' is not a git repository"
    
    result = []
    result.append("=== Version Tag Analysis ===")
    result.append(f"Repository path: {os.path.abspath(repo_path)}")
    
    comparison_type = "working directory (includes uncommitted changes)" if include_working else "HEAD (committed changes only)"
    result.append(f"Comparison mode: {comparison_type}")
    
    # Show latest tag and diff
    latest_tag, diff_output = get_diff_from_latest_tag(repo_path, include_working)
    result.append(f"\nLatest version tag: {latest_tag}")
    
    # Show commit summary (only for committed changes)
    _, commit_summary = get_commit_summary_from_latest_tag(repo_path)
    
    if commit_summary.strip():
        result.append(f"\nCommits since {latest_tag}:")
        result.append(commit_summary)
    else:
        result.append(f"\nNo commits since {latest_tag}")
    
    # Show diff if there are changes
    if diff_output.strip():
        result.append(f"\nDiff since {latest_tag}:")
        result.append(diff_output)
    else:
        if include_working:
            result.append(f"\nNo changes since {latest_tag}")
        else:
            result.append(f"\nNo committed changes since {latest_tag}")
    
    return "\n".join(result)


# Server configuration
name = "github"
instructions = "Compare current state with latest version tag. Requires ABSOLUTE path to git repository. Includes uncommitted changes by default (recommended for development)."
tools = ["show_changes_since_latest_tag", "prepare_commit_with_message"]
