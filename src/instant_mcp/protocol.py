from typing import List, Dict, Any, Callable
from dataclasses import dataclass

@dataclass
class SeverProtocol:
    """Protocol for defining MCP servers with minimal configuration."""
    name: str
    instructions: str
    tools: List[str]
    
    def __post_init__(self):
        # Register this server protocol globally
        _register_server_protocol(self)

# Global registry for server protocols
_server_protocols: Dict[str, 'SeverProtocol'] = {}

def _register_server_protocol(protocol: 'SeverProtocol'):
    """Register a server protocol globally."""
    _server_protocols[protocol.name] = protocol

def get_server_protocols() -> Dict[str, 'SeverProtocol']:
    """Get all registered server protocols."""
    return _server_protocols.copy()

def get_server_protocol(name: str) -> 'SeverProtocol':
    """Get a specific server protocol by name."""
    return _server_protocols.get(name)