from typing import Any
from instant_mcp import SeverProtocol

SeverProtocol(
    name="my_text_server",
    instructions="A text processing server providing string manipulation tools",
    tools=[
        "reverse_text",
        "count_words",
    ]
)

async def reverse_text(text: str) -> dict[str, Any]:
    """Reverse the given text."""
    try:
        return {
            "original": text,
            "reversed": text[::-1],
            "status": "success"
        }
    except Exception as e:
        return {
            "error": f"Failed to reverse text: {str(e)}",
            "status": "error"
        }

async def count_words(text: str) -> dict[str, Any]:
    """Count words in the given text."""
    try:
        words = text.split()
        return {
            "text": text,
            "word_count": len(words),
            "character_count": len(text),
            "status": "success"
        }
    except Exception as e:
        return {
            "error": f"Failed to count words: {str(e)}",
            "status": "error"
        }

def to_uppercase(text: str) -> dict[str, Any]:
    """Convert text to uppercase."""
    try:
        return {
            "original": text,
            "uppercase": text.upper(),
            "status": "success"
        }
    except Exception as e:
        return {
            "error": f"Failed to convert to uppercase: {str(e)}",
            "status": "error"
        } 