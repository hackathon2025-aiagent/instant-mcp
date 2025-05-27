import math
from typing import Any

# Server configuration
name = "math_server"
instructions = "A math server providing basic calculations"
tools = ["calculate", "square_root", "factorial"]

async def calculate(expression: str) -> dict[str, Any]:
    """Calculate a mathematical expression."""
    try:
        # Simple and safe evaluation
        result = eval(expression, {"__builtins__": {}, "math": math})
        return {
            "expression": expression,
            "result": result,
            "status": "success"
        }
    except Exception as e:
        return {
            "error": f"Failed to calculate {expression}: {str(e)}",
            "status": "error"
        }

async def square_root(number: float) -> dict[str, Any]:
    """Calculate square root of a number."""
    try:
        result = math.sqrt(number)
        return {
            "number": number,
            "square_root": result,
            "status": "success"
        }
    except Exception as e:
        return {
            "error": f"Failed to calculate square root: {str(e)}",
            "status": "error"
        }

async def factorial(n: int) -> dict[str, Any]:
    """Calculate factorial of a number."""
    try:
        result = math.factorial(n)
        return {
            "number": n,
            "factorial": result,
            "status": "success"
        }
    except Exception as e:
        return {
            "error": f"Failed to calculate factorial: {str(e)}",
            "status": "error"
        } 