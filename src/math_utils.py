"""Math utility functions for basic arithmetic and number theory operations.

Why: Provide a reusable, well-tested collection of mathematical operations
     that encapsulate edge-case handling (zero division, negative inputs)
     and shield callers from repeating boilerplate validation.
How: Each function is a pure function with no side effects.
     Input validation raises descriptive built-in exceptions so callers
     can handle errors without importing custom exception types.
"""


def add(a: float, b: float) -> float:
    """Return the sum of two numbers.

    Why: Centralise addition so callers benefit from consistent type handling.
    How: Delegates directly to Python's built-in + operator.
    """
    return a + b


def subtract(a: float, b: float) -> float:
    """Return the difference of two numbers (a - b).

    Why: Centralise subtraction to maintain a uniform interface across
         all arithmetic helpers in this module.
    How: Delegates directly to Python's built-in - operator.
    """
    return a - b


def multiply(a: float, b: float) -> float:
    """Return the product of two numbers.

    Why: Centralise multiplication to maintain a uniform interface.
    How: Delegates directly to Python's built-in * operator.
    """
    return a * b


def divide(a: float, b: float) -> float:
    """Return the quotient of two numbers (a / b).

    Why: Division requires explicit zero-check to produce a clear error
         message instead of a cryptic Python ZeroDivisionError with no
         context about which call site triggered the error.
    How: Validates divisor before performing division. Raises
         ZeroDivisionError with a descriptive message when b == 0.
    """
    if b == 0:
        raise ZeroDivisionError("divisor 'b' must not be zero")
    return a / b


def power(base: float, exponent: float) -> float:
    """Return base raised to the given exponent.

    Why: Wraps Python's ** operator to keep the module's API consistent
         and allow future instrumentation (e.g. logging, overflow guards)
         without touching call sites.
    How: Delegates directly to Python's built-in ** operator.
    """
    return base ** exponent


def factorial(n: int) -> int:
    """Return the factorial of a non-negative integer n (n!).

    Why: Factorial is frequently needed in combinatorics and probability
         calculations. Centralising the implementation ensures consistent
         handling of the n=0 edge case and rejection of negative inputs.
    How: Validates that n >= 0, then iteratively multiplies 1..n.
         Uses iteration rather than recursion to avoid hitting Python's
         default recursion limit for large values of n.
         Raises ValueError for negative inputs with a descriptive message.
    """
    if n < 0:
        raise ValueError(f"factorial is not defined for negative integers, got {n}")

    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def fibonacci(n: int) -> list[int]:
    """Return the first n Fibonacci numbers as a list.

    Why: Fibonacci sequences appear in algorithm analysis, data-structure
         sizing, and mathematical modelling. A single canonical implementation
         prevents off-by-one bugs and inconsistent seed values across callers.
    How: Validates n >= 0 and returns an empty list for n == 0.
         Builds the sequence iteratively (O(n) time, O(n) space) by
         seeding with [0, 1] and appending sum of the last two elements.
         Raises ValueError for negative n with a descriptive message.
    """
    if n < 0:
        raise ValueError(f"fibonacci requires a non-negative integer, got {n}")

    if n == 0:
        return []

    if n == 1:
        return [0]

    sequence: list[int] = [0, 1]
    for _ in range(2, n):
        sequence.append(sequence[-1] + sequence[-2])
    return sequence
