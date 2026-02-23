"""Basic arithmetic calculator module."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.history import CalculationHistory


class Calculator:
    """Provides basic arithmetic operations as instance methods.

    Why: A centralized arithmetic class allows consumers to depend on a
         single, testable unit rather than scattered standalone functions.
    How: Each method delegates to Python's built-in operators and raises
         domain-specific errors (ValueError) for undefined operations such
         as division by zero. An optional CalculationHistory dependency is
         accepted via constructor injection; the class never self-creates one.
    """

    def __init__(self, history: Optional[CalculationHistory] = None) -> None:
        """Initialize Calculator with an optional history dependency.

        Why: Constructor injection allows callers to supply a shared or mock
             CalculationHistory without forcing the class to create one,
             and preserves backward compatibility for callers that pass no
             arguments (Calculator() still works).
        How: Stores the injected history reference; None means history
             recording is disabled for this instance.
        """
        self._history = history

    def add(self, left_operand: float, right_operand: float) -> float:
        """Return the sum of two numbers.

        Why: Encapsulating addition in a method keeps the API consistent
             with the other arithmetic operations on this class.
        How: Delegates directly to Python's + operator, which handles both
             int and float operands transparently. Records the operation to
             history when a history instance is present.
        """
        result = left_operand + right_operand
        if self._history is not None:
            self._history.record("add", left_operand, right_operand, result)
        return result

    def subtract(self, left_operand: float, right_operand: float) -> float:
        """Return the difference of two numbers (left minus right).

        Why: Encapsulating subtraction keeps the API surface uniform and
             makes swapping implementations (e.g., decimal-based) easy.
        How: Delegates directly to Python's - operator. Records the
             operation to history on success.
        """
        result = left_operand - right_operand
        if self._history is not None:
            self._history.record("subtract", left_operand, right_operand, result)
        return result

    def multiply(self, left_operand: float, right_operand: float) -> float:
        """Return the product of two numbers.

        Why: Centralizing multiplication ensures consistent behavior
             (e.g., floating-point semantics) across all call sites.
        How: Delegates directly to Python's * operator. Records the
             operation to history on success.
        """
        result = left_operand * right_operand
        if self._history is not None:
            self._history.record("multiply", left_operand, right_operand, result)
        return result

    def divide(self, dividend: float, divisor: float) -> float:
        """Return the quotient of two numbers (dividend divided by divisor).

        Why: Division by zero is mathematically undefined; allowing it to
             propagate as a ZeroDivisionError leaks implementation details.
             Raising ValueError instead signals a contract violation to
             callers in a language-idiomatic way.
        How: Explicitly checks the divisor before delegating to Python's /
             operator. Raises ValueError with a descriptive message so
             callers can distinguish this from other value-related errors.
             History is recorded only after a successful division to avoid
             polluting the log with failed operations.
        """
        if divisor == 0:
            raise ValueError("Division by zero is undefined")
        result = dividend / divisor
        if self._history is not None:
            self._history.record("divide", dividend, divisor, result)
        return result
