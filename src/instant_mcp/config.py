import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

# Default configuration
DEFAULT_CONFIG = {
    "target_path": "./instant_servers"
}

def get_config_file_path() -> Path:
    """Get the path to the configuration file."""
    # Use user's home directory for config
    config_dir = Path.home() / ".instant_mcp"
    config_dir.mkdir(exist_ok=True)
    return config_dir / "config.json"

def load_config() -> Dict[str, Any]:
    """Load configuration from file or return defaults."""
    config_file = get_config_file_path()
    
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                # Merge with defaults to ensure all keys exist
                merged_config = DEFAULT_CONFIG.copy()
                merged_config.update(config)
                return merged_config
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load config file: {e}")
    
    return DEFAULT_CONFIG.copy()

def save_config(config: Dict[str, Any]) -> None:
    """Save configuration to file."""
    config_file = get_config_file_path()
    
    try:
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"Configuration saved to {config_file}")
    except IOError as e:
        print(f"Error saving config: {e}")

def get_target_path() -> str:
    """Get the current target path from config."""
    config = load_config()
    return config["target_path"]

def set_target_path(path: str) -> None:
    """Set the target path in config."""
    config = load_config()
    # Convert relative path to absolute path
    absolute_path = os.path.abspath(path)
    config["target_path"] = absolute_path
    save_config(config)
    print(f"Target path set to: {absolute_path}")

def show_config() -> None:
    """Display current configuration."""
    config = load_config()
    config_file = get_config_file_path()
    
    print(f"Configuration file: {config_file}")
    print("Current settings:")
    for key, value in config.items():
        print(f"  {key}: {value}")

def reset_config() -> None:
    """Reset configuration to defaults."""
    save_config(DEFAULT_CONFIG.copy())
    print("Configuration reset to defaults.") 