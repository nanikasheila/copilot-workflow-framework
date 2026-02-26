"""Tests for math_utils module.

Why: Verify all public functions handle normal cases, boundary values,
     and error conditions correctly, satisfying the development Gate
     (pass_rate=100%, coverage_min=70%).
How: Uses pytest with the AAA pattern. Each test function is independent
     and covers exactly one condition to keep failures diagnostic.
"""

import pytest

from src.math_utils import (
    add,
    divide,
    factorial,
    fibonacci,
    multiply,
    power,
    subtract,
)


# ---------------------------------------------------------------------------
# add
# ---------------------------------------------------------------------------


def test_add_positive_numbers_returns_sum() -> None:
    # Arrange
    a, b = 3.0, 4.0
    # Act
    result = add(a, b)
    # Assert
    assert result == 7.0


def test_add_with_zero_returns_same_number() -> None:
    assert add(5.0, 0.0) == 5.0


def test_add_negative_numbers_returns_negative_sum() -> None:
    assert add(-2.0, -3.0) == -5.0


def test_add_mixed_sign_numbers_returns_correct_sum() -> None:
    assert add(-1.0, 4.0) == 3.0


def test_add_floats_returns_correct_sum() -> None:
    assert add(0.1, 0.2) == pytest.approx(0.3)


# ---------------------------------------------------------------------------
# subtract
# ---------------------------------------------------------------------------


def test_subtract_positive_numbers_returns_difference() -> None:
    assert subtract(10.0, 4.0) == 6.0


def test_subtract_with_zero_subtrahend_returns_same_number() -> None:
    assert subtract(7.0, 0.0) == 7.0


def test_subtract_results_in_negative_value() -> None:
    assert subtract(2.0, 5.0) == -3.0


def test_subtract_negative_numbers_returns_correct_difference() -> None:
    assert subtract(-3.0, -1.0) == -2.0


# ---------------------------------------------------------------------------
# multiply
# ---------------------------------------------------------------------------


def test_multiply_positive_numbers_returns_product() -> None:
    assert multiply(3.0, 4.0) == 12.0


def test_multiply_by_zero_returns_zero() -> None:
    assert multiply(99.0, 0.0) == 0.0


def test_multiply_negative_numbers_returns_positive_product() -> None:
    assert multiply(-3.0, -4.0) == 12.0


def test_multiply_mixed_sign_returns_negative_product() -> None:
    assert multiply(3.0, -4.0) == -12.0


def test_multiply_by_one_returns_same_number() -> None:
    assert multiply(7.5, 1.0) == 7.5


# ---------------------------------------------------------------------------
# divide
# ---------------------------------------------------------------------------


def test_divide_positive_numbers_returns_quotient() -> None:
    assert divide(10.0, 2.0) == 5.0


def test_divide_with_negative_divisor_returns_negative_quotient() -> None:
    assert divide(9.0, -3.0) == -3.0


def test_divide_floats_returns_correct_quotient() -> None:
    assert divide(1.0, 4.0) == pytest.approx(0.25)


def test_divide_dividend_zero_returns_zero() -> None:
    assert divide(0.0, 5.0) == 0.0


def test_divide_by_zero_raises_zero_division_error() -> None:
    # Arrange / Act / Assert
    with pytest.raises(ZeroDivisionError, match="divisor 'b' must not be zero"):
        divide(10.0, 0.0)


def test_divide_negative_dividend_by_zero_raises_zero_division_error() -> None:
    with pytest.raises(ZeroDivisionError):
        divide(-5.0, 0.0)


# ---------------------------------------------------------------------------
# power
# ---------------------------------------------------------------------------


def test_power_positive_base_and_exponent_returns_correct_value() -> None:
    assert power(2.0, 10.0) == 1024.0


def test_power_exponent_zero_returns_one() -> None:
    assert power(99.0, 0.0) == 1.0


def test_power_base_zero_returns_zero() -> None:
    assert power(0.0, 5.0) == 0.0


def test_power_negative_exponent_returns_reciprocal() -> None:
    assert power(2.0, -1.0) == pytest.approx(0.5)


def test_power_base_one_returns_one() -> None:
    assert power(1.0, 1000.0) == 1.0


def test_power_fractional_exponent_returns_root() -> None:
    assert power(9.0, 0.5) == pytest.approx(3.0)


# ---------------------------------------------------------------------------
# factorial
# ---------------------------------------------------------------------------


def test_factorial_zero_returns_one() -> None:
    # Boundary: 0! == 1 by convention
    assert factorial(0) == 1


def test_factorial_one_returns_one() -> None:
    assert factorial(1) == 1


def test_factorial_five_returns_120() -> None:
    assert factorial(5) == 120


def test_factorial_large_value_returns_correct_result() -> None:
    assert factorial(10) == 3628800


def test_factorial_negative_input_raises_value_error() -> None:
    with pytest.raises(ValueError, match="factorial is not defined for negative integers"):
        factorial(-1)


def test_factorial_large_negative_input_raises_value_error() -> None:
    with pytest.raises(ValueError):
        factorial(-100)


# ---------------------------------------------------------------------------
# fibonacci
# ---------------------------------------------------------------------------


def test_fibonacci_zero_returns_empty_list() -> None:
    # Boundary: n == 0
    assert fibonacci(0) == []


def test_fibonacci_one_returns_list_with_zero() -> None:
    # Boundary: n == 1
    assert fibonacci(1) == [0]


def test_fibonacci_two_returns_seed_values() -> None:
    # Boundary: n == 2
    assert fibonacci(2) == [0, 1]


def test_fibonacci_five_returns_correct_sequence() -> None:
    assert fibonacci(5) == [0, 1, 1, 2, 3]


def test_fibonacci_ten_returns_correct_sequence() -> None:
    assert fibonacci(10) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


def test_fibonacci_negative_input_raises_value_error() -> None:
    with pytest.raises(ValueError, match="fibonacci requires a non-negative integer"):
        fibonacci(-1)


def test_fibonacci_large_negative_input_raises_value_error() -> None:
    with pytest.raises(ValueError):
        fibonacci(-50)


def test_fibonacci_sequence_property_each_element_is_sum_of_previous_two() -> None:
    """Verify the Fibonacci recurrence relation for n=8."""
    # Arrange
    sequence = fibonacci(8)
    # Act / Assert
    for i in range(2, len(sequence)):
        assert sequence[i] == sequence[i - 1] + sequence[i - 2]
