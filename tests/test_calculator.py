"""Tests for the Calculator class (pure arithmetic operations).

Why: Verifying every arithmetic operation—including edge cases—prevents
     regressions and documents the expected contract of Calculator.
How: Uses pytest with the AAA (Arrange, Act, Assert) pattern. Each test
     function name fully expresses the scenario being verified.
"""

import pytest

from src.calculator import Calculator


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def calculator() -> Calculator:
    """Provide a fresh Calculator instance for each test.

    Why: Sharing a single instance across tests could mask state-mutation
         bugs; a fresh instance per test guarantees isolation.
    How: pytest fixture with default (function) scope instantiates a new
         Calculator before each test function.
    """
    return Calculator()


# ---------------------------------------------------------------------------
# Addition
# ---------------------------------------------------------------------------


def test_add_returns_correct_sum_for_positive_numbers(calculator: Calculator) -> None:
    # Arrange
    a, b = 3.0, 5.0
    # Act
    result = calculator.add(a, b)
    # Assert
    assert result == 8.0


def test_add_returns_correct_sum_for_negative_numbers(calculator: Calculator) -> None:
    # Arrange
    a, b = -4.0, -6.0
    # Act
    result = calculator.add(a, b)
    # Assert
    assert result == -10.0


def test_add_returns_correct_sum_when_one_operand_is_zero(calculator: Calculator) -> None:
    # Arrange
    a, b = 0.0, 7.0
    # Act
    result = calculator.add(a, b)
    # Assert
    assert result == 7.0


def test_add_returns_correct_sum_for_floating_point_numbers(calculator: Calculator) -> None:
    # Arrange
    a, b = 1.1, 2.2
    # Act
    result = calculator.add(a, b)
    # Assert
    assert result == pytest.approx(3.3)


# ---------------------------------------------------------------------------
# Subtraction
# ---------------------------------------------------------------------------


def test_subtract_returns_correct_difference_for_positive_numbers(calculator: Calculator) -> None:
    # Arrange
    a, b = 10.0, 4.0
    # Act
    result = calculator.subtract(a, b)
    # Assert
    assert result == 6.0


def test_subtract_returns_correct_difference_for_negative_numbers(calculator: Calculator) -> None:
    # Arrange
    a, b = -3.0, -8.0
    # Act
    result = calculator.subtract(a, b)
    # Assert
    assert result == 5.0


def test_subtract_returns_zero_when_operands_are_equal(calculator: Calculator) -> None:
    # Arrange
    a, b = 9.0, 9.0
    # Act
    result = calculator.subtract(a, b)
    # Assert
    assert result == 0.0


# ---------------------------------------------------------------------------
# Multiplication
# ---------------------------------------------------------------------------


def test_multiply_returns_correct_product_for_positive_numbers(calculator: Calculator) -> None:
    # Arrange
    a, b = 3.0, 4.0
    # Act
    result = calculator.multiply(a, b)
    # Assert
    assert result == 12.0


def test_multiply_returns_zero_when_one_operand_is_zero(calculator: Calculator) -> None:
    # Arrange
    a, b = 100.0, 0.0
    # Act
    result = calculator.multiply(a, b)
    # Assert
    assert result == 0.0


def test_multiply_returns_correct_product_for_negative_numbers(calculator: Calculator) -> None:
    # Arrange
    a, b = -5.0, 3.0
    # Act
    result = calculator.multiply(a, b)
    # Assert
    assert result == -15.0


# ---------------------------------------------------------------------------
# Division
# ---------------------------------------------------------------------------


def test_divide_returns_correct_quotient_when_result_is_whole_number(calculator: Calculator) -> None:
    # Arrange
    a, b = 10.0, 2.0
    # Act
    result = calculator.divide(a, b)
    # Assert
    assert result == 5.0


def test_divide_returns_float_quotient_when_result_is_not_whole_number(calculator: Calculator) -> None:
    # Arrange
    a, b = 1.0, 3.0
    # Act
    result = calculator.divide(a, b)
    # Assert
    assert result == pytest.approx(0.3333333333333333)


# ---------------------------------------------------------------------------
# Division — error cases
# ---------------------------------------------------------------------------


def test_divide_raises_value_error_when_divisor_is_positive_zero(calculator: Calculator) -> None:
    # Arrange
    dividend, divisor = 5.0, 0.0
    # Act & Assert
    with pytest.raises(ValueError, match=r"Division by zero"):
        calculator.divide(dividend, divisor)


def test_divide_raises_value_error_when_divisor_is_negative_zero(calculator: Calculator) -> None:
    # Arrange
    dividend, divisor = -8.0, -0.0
    # Act & Assert
    with pytest.raises(ValueError, match=r"Division by zero"):
        calculator.divide(dividend, divisor)
