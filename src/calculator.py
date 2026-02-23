"""Basic arithmetic calculator module."""


class Calculator:
    """Provides basic arithmetic operations as instance methods.

    Why: A centralized arithmetic class allows consumers to depend on a
         single, testable unit rather than scattered standalone functions.
    How: Each method delegates to Python's built-in operators and raises
         domain-specific errors (ValueError) for undefined operations such
         as division by zero.
    """

    def add(self, left_operand: float, right_operand: float) -> float:
        """Return the sum of two numbers.

        Why: Encapsulating addition in a method keeps the API consistent
             with the other arithmetic operations on this class.
        How: Delegates directly to Python's + operator, which handles both
             int and float operands transparently.
        """
        return left_operand + right_operand

    def subtract(self, left_operand: float, right_operand: float) -> float:
        """Return the difference of two numbers (left minus right).

        Why: Encapsulating subtraction keeps the API surface uniform and
             makes swapping implementations (e.g., decimal-based) easy.
        How: Delegates directly to Python's - operator.
        """
        return left_operand - right_operand

    def multiply(self, left_operand: float, right_operand: float) -> float:
        """Return the product of two numbers.

        Why: Centralizing multiplication ensures consistent behavior
             (e.g., floating-point semantics) across all call sites.
        How: Delegates directly to Python's * operator.
        """
        return left_operand * right_operand

    def divide(self, dividend: float, divisor: float) -> float:
        """Return the quotient of two numbers (dividend divided by divisor).

        Why: Division by zero is mathematically undefined; allowing it to
             propagate as a ZeroDivisionError leaks implementation details.
             Raising ValueError instead signals a contract violation to
             callers in a language-idiomatic way.
        How: Explicitly checks the divisor before delegating to Python's /
             operator. Raises ValueError with a descriptive message so
             callers can distinguish this from other value-related errors.
        """
        if divisor == 0:
            raise ValueError("Division by zero is undefined")
        return dividend / divisor
