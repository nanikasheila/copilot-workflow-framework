"""Tests for CalculationHistory and CalculationEntry.

Why: CalculationHistory is the single source of truth for the audit trail;
     verifying all public methods prevents silent data loss or corruption.
How: Uses pytest with the AAA pattern. File I/O tests rely on pytest's
     tmp_path fixture to avoid touching the real filesystem.
"""

import json
from pathlib import Path

import pytest

from src.history import CalculationEntry, CalculationHistory


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def history() -> CalculationHistory:
    """Provide a fresh CalculationHistory instance for each test.

    Why: Shared state between tests hides order-dependent failures;
         a new instance per test guarantees full isolation.
    How: Default (function) scope creates a new CalculationHistory before
         each test function.
    """
    return CalculationHistory()


# ---------------------------------------------------------------------------
# CalculationEntry construction
# ---------------------------------------------------------------------------


def test_calculation_entry_stores_all_fields_correctly() -> None:
    # Arrange / Act
    entry = CalculationEntry(
        operation="add",
        left_operand=3.0,
        right_operand=5.0,
        result=8.0,
    )
    # Assert
    assert entry.operation == "add"
    assert entry.left_operand == 3.0
    assert entry.right_operand == 5.0
    assert entry.result == 8.0


def test_calculation_entry_supports_equality_comparison() -> None:
    # Arrange
    entry_a = CalculationEntry("multiply", 2.0, 4.0, 8.0)
    entry_b = CalculationEntry("multiply", 2.0, 4.0, 8.0)
    # Act / Assert
    assert entry_a == entry_b


# ---------------------------------------------------------------------------
# record / get_entries
# ---------------------------------------------------------------------------


def test_get_entries_returns_empty_list_for_new_history(history: CalculationHistory) -> None:
    # Act
    entries = history.get_entries()
    # Assert
    assert entries == []


def test_record_appends_single_entry_to_history(history: CalculationHistory) -> None:
    # Arrange
    history.record("add", 1.0, 2.0, 3.0)
    # Act
    entries = history.get_entries()
    # Assert
    assert len(entries) == 1
    assert entries[0] == CalculationEntry("add", 1.0, 2.0, 3.0)


def test_record_appends_multiple_entries_in_order(history: CalculationHistory) -> None:
    # Arrange
    history.record("add", 1.0, 2.0, 3.0)
    history.record("subtract", 10.0, 4.0, 6.0)
    history.record("multiply", 3.0, 3.0, 9.0)
    # Act
    entries = history.get_entries()
    # Assert
    assert len(entries) == 3
    assert entries[0].operation == "add"
    assert entries[1].operation == "subtract"
    assert entries[2].operation == "multiply"


def test_get_entries_returns_copy_not_internal_reference(history: CalculationHistory) -> None:
    # Arrange
    history.record("add", 1.0, 1.0, 2.0)
    # Act — mutate the returned list
    returned = history.get_entries()
    returned.clear()
    # Assert — internal state must be unchanged
    assert len(history.get_entries()) == 1


# ---------------------------------------------------------------------------
# clear
# ---------------------------------------------------------------------------


def test_clear_removes_all_entries(history: CalculationHistory) -> None:
    # Arrange
    history.record("add", 5.0, 5.0, 10.0)
    history.record("divide", 10.0, 2.0, 5.0)
    # Act
    history.clear()
    # Assert
    assert history.get_entries() == []


def test_record_after_clear_starts_fresh_history(history: CalculationHistory) -> None:
    # Arrange
    history.record("add", 1.0, 1.0, 2.0)
    history.clear()
    # Act
    history.record("multiply", 3.0, 3.0, 9.0)
    entries = history.get_entries()
    # Assert
    assert len(entries) == 1
    assert entries[0].operation == "multiply"


# ---------------------------------------------------------------------------
# export_to_json
# ---------------------------------------------------------------------------


def test_export_to_json_creates_file_at_given_path(
    history: CalculationHistory, tmp_path: Path
) -> None:
    # Arrange
    history.record("add", 1.0, 2.0, 3.0)
    output_file = tmp_path / "history.json"
    # Act
    history.export_to_json(output_file)
    # Assert
    assert output_file.exists()


def test_export_to_json_writes_valid_json_array(
    history: CalculationHistory, tmp_path: Path
) -> None:
    # Arrange
    history.record("add", 1.0, 2.0, 3.0)
    output_file = tmp_path / "history.json"
    # Act
    history.export_to_json(output_file)
    data = json.loads(output_file.read_text(encoding="utf-8"))
    # Assert
    assert isinstance(data, list)
    assert len(data) == 1


def test_export_to_json_serializes_entry_fields_correctly(
    history: CalculationHistory, tmp_path: Path
) -> None:
    # Arrange
    history.record("divide", 10.0, 4.0, 2.5)
    output_file = tmp_path / "history.json"
    # Act
    history.export_to_json(output_file)
    data = json.loads(output_file.read_text(encoding="utf-8"))
    # Assert
    assert data[0]["operation"] == "divide"
    assert data[0]["left_operand"] == 10.0
    assert data[0]["right_operand"] == 4.0
    assert data[0]["result"] == 2.5


def test_export_to_json_writes_empty_array_when_history_is_empty(
    history: CalculationHistory, tmp_path: Path
) -> None:
    # Arrange
    output_file = tmp_path / "empty.json"
    # Act
    history.export_to_json(output_file)
    data = json.loads(output_file.read_text(encoding="utf-8"))
    # Assert
    assert data == []


def test_export_to_json_preserves_insertion_order(
    history: CalculationHistory, tmp_path: Path
) -> None:
    # Arrange
    history.record("add", 1.0, 2.0, 3.0)
    history.record("multiply", 4.0, 5.0, 20.0)
    output_file = tmp_path / "ordered.json"
    # Act
    history.export_to_json(output_file)
    data = json.loads(output_file.read_text(encoding="utf-8"))
    # Assert
    assert data[0]["operation"] == "add"
    assert data[1]["operation"] == "multiply"


def test_export_to_json_overwrites_existing_file(
    history: CalculationHistory, tmp_path: Path
) -> None:
    # Arrange
    output_file = tmp_path / "overwrite.json"
    history.record("add", 1.0, 1.0, 2.0)
    history.export_to_json(output_file)
    history.clear()
    history.record("multiply", 3.0, 3.0, 9.0)
    # Act
    history.export_to_json(output_file)
    data = json.loads(output_file.read_text(encoding="utf-8"))
    # Assert
    assert len(data) == 1
    assert data[0]["operation"] == "multiply"
