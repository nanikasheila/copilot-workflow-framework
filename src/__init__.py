"""src package — exposes math_utils as the public API of this package.

Why: An explicit __init__.py prevents accidental wildcard imports from
     consuming internal symbols and makes the intended public surface clear.
How: Re-exports only the public functions from math_utils so callers can
     use either `from src import add` or `from src.math_utils import add`.
"""

from src.math_utils import (
    add,
    divide,
    factorial,
    fibonacci,
    multiply,
    power,
    subtract,
)

__all__ = [
    "add",
    "subtract",
    "multiply",
    "divide",
    "power",
    "factorial",
    "fibonacci",
]
