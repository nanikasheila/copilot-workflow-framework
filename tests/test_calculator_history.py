"""Tests for Calculator + CalculationHistory integration.

Why: The Calculator‐History coupling via optional DI is a critical contract.
     Verifying that operations are recorded correctly, that failures are
     excluded, and that history-less Calculators still work prevents silent
     regressions in the integration seam.
How: Uses pytest with AAA pattern. Two fixtures compose Calculator and
     CalculationHistory together; a separate test verifies backward
     compatibility (no history injected).
"""

import pytest

from src.calculator import Calculator
from src.history import CalculationHistory


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def history() -> CalculationHistory:
    """Provide a fresh CalculationHistory instance for integration tests.

    Why: Isolating the history object allows asserting its state independently
         from the Calculator, making failures easier to diagnose.
    How: Default (function) scope creates a new CalculationHistory per test.
    """
    return CalculationHistory()


@pytest.fixture
def calculator_with_history(history: CalculationHistory) -> Calculator:
    """Provide a Calculator wired to a CalculationHistory instance.

    Why: Integration tests need access to both the Calculator and its history
         dependency; this fixture composes them the same way production code
         would.
    How: Injects the history fixture into a new Calculator instance so tests
         can inspect history state after each operation.
    """
    return Calculator(history=history)


# ---------------------------------------------------------------------------
# Recording successful operations
# ---------------------------------------------------------------------------


def test_add_records_entry_in_history(
    calculator_with_history: Calculator, history: CalculationHistory
) -> None:
    # Arrange / Act
    calculator_with_history.add(3.0, 5.0)
    entries = history.get_entries()
    # Assert
    assert len(entries) == 1
    assert entries[0].operation == "add"
    assert entries[0].left_operand == 3.0
    assert entries[0].right_operand == 5.0
    assert entries[0].result == 8.0


def test_subtract_records_entry_in_history(
    calculator_with_history: Calculator, history: CalculationHistory
) -> None:
    # Arrange / Act
    calculator_with_history.subtract(10.0, 4.0)
    entries = history.get_entries()
    # Assert
    assert len(entries) == 1
    assert entries[0].operation == "subtract"
    assert entries[0].result == 6.0


def test_multiply_records_entry_in_history(
    calculator_with_history: Calculator, history: CalculationHistory
) -> None:
    # Arrange / Act
    calculator_with_history.multiply(3.0, 7.0)
    entries = history.get_entries()
    # Assert
    assert len(entries) == 1
    assert entries[0].operation == "multiply"
    assert entries[0].result == 21.0


def test_divide_records_entry_in_history_on_success(
    calculator_with_history: Calculator, history: CalculationHistory
) -> None:
    # Arrange / Act
    calculator_with_history.divide(10.0, 2.0)
    entries = history.get_entries()
    # Assert
    assert len(entries) == 1
    assert entries[0].operation == "divide"
    assert entries[0].result == 5.0


def test_multiple_operations_are_recorded_in_insertion_order(
    calculator_with_history: Calculator, history: CalculationHistory
) -> None:
    # Arrange / Act
    calculator_with_history.add(1.0, 2.0)
    calculator_with_history.multiply(3.0, 4.0)
    calculator_with_history.subtract(9.0, 1.0)
    entries = history.get_entries()
    # Assert
    assert len(entries) == 3
    assert entries[0].operation == "add"
    assert entries[1].operation == "multiply"
    assert entries[2].operation == "subtract"


# ---------------------------------------------------------------------------
# No recording on failure
# ---------------------------------------------------------------------------


def test_divide_does_not_record_entry_when_divisor_is_zero(
    calculator_with_history: Calculator, history: CalculationHistory
) -> None:
    # Arrange / Act
    with pytest.raises(ValueError):
        calculator_with_history.divide(5.0, 0.0)
    # Assert
    assert history.get_entries() == []


# ---------------------------------------------------------------------------
# Backward compatibility — calculator without history
# ---------------------------------------------------------------------------


def test_calculator_without_history_does_not_raise_on_any_operation() -> None:
    """Verify Calculator() with no history arg still works (ADR-001 contract).

    Why: ADR-001 mandates backward compatibility; Calculator() must remain
         valid and raise no errors on any operation.
    How: Instantiate without arguments and call every arithmetic method.
    """
    # Arrange
    calc = Calculator()
    # Act / Assert — no AttributeError or TypeError expected
    assert calc.add(1.0, 1.0) == 2.0
    assert calc.subtract(5.0, 3.0) == 2.0
    assert calc.multiply(2.0, 3.0) == 6.0
    assert calc.divide(10.0, 2.0) == 5.0
