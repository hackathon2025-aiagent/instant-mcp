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


def get_diff_from_latest_tag(repo_path: str = ".") -> Tuple[Optional[str], str]:
    """
    Get the diff between the latest version tag and current HEAD
    Returns: (latest_tag, diff_output)
    """
    latest_tag = get_latest_version_tag(repo_path)
    
    if not latest_tag:
        return None, "No version tags found in repository"
    
    try:
        # Get diff between latest tag and HEAD
        result = subprocess.run(
            ['git', 'diff', f'{latest_tag}..HEAD'],
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


def show_changes_since_latest_tag(repo_path: str = "/home/crimson/manager/cursor-workspace/instant-mcp"):
    """
    Display changes since the latest version tag
    """
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
    
    # Show latest tag and diff
    latest_tag, diff_output = get_diff_from_latest_tag(repo_path)
    result.append(f"\nLatest version tag: {latest_tag}")
    
    # Show commit summary
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
        result.append(f"\nNo changes since {latest_tag}")
    
    return "\n".join(result)


# Server configuration
name = "github"
instructions = "git diff between latest version tag and current HEAD"
tools = ["show_changes_since_latest_tag"]
