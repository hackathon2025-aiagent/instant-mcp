# Installation Guide

## Quick Install

```bash
pip install git+https://github.com/crimson206/instant-mcp
```

## Prerequisites

- Python 3.10 or higher
- Git (for Git workflow features)

## Alternative Installation Methods

### From Source

```bash
git clone https://github.com/crimson206/instant-mcp
cd instant-mcp
pip install -e .
```

### Using Poetry

```bash
git clone https://github.com/crimson206/instant-mcp
cd instant-mcp
poetry install
```

## Verify Installation

```bash
instant-mcp servers
```

You should see a list of available example servers.

## Development Installation

For development with additional dependencies:

```bash
git clone https://github.com/crimson206/instant-mcp
cd instant-mcp
pip install -e ".[dev]"

# Run tests
pytest
```

## Troubleshooting Installation

### Common Issues

1. **Python version**: Ensure you're using Python 3.10 or higher
2. **Permission errors**: Use virtual environments or user installation (`pip install --user`)
3. **Git not found**: Install Git for your operating system

### Virtual Environment Setup

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install git+https://github.com/crimson206/instant-mcp
``` 