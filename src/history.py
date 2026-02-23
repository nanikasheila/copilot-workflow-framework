"""Calculation history module for recording and exporting arithmetic operations."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class CalculationEntry:
    """Immutable record of a single arithmetic operation and its result.

    Why: A dedicated data class makes each history record self-describing
         and easy to serialize, replacing fragile tuple-based storage.
    How: Python dataclass auto-generates __init__, __repr__, and __eq__,
         keeping the definition declarative and concise.
    """

    operation: str
    left_operand: float
    right_operand: float
    result: float


class CalculationHistory:
    """Stores and manages a sequence of calculation entries.

    Why: Separating history concerns from calculation logic follows the
         Single Responsibility Principle and allows independent testing.
    How: Maintains an internal list of CalculationEntry objects. Public
         methods expose record/query/clear/export operations without leaking
         the internal list reference.
    """

    def __init__(self) -> None:
        """Initialize an empty history store.

        Why: An explicit __init__ makes the internal state contract clear
             and ensures no shared mutable state between instances.
        How: Stores entries in a private list; callers access only via
             the public API.
        """
        self._entries: list[CalculationEntry] = []

    def record(
        self,
        operation: str,
        left_operand: float,
        right_operand: float,
        result: float,
    ) -> None:
        """Append a new calculation entry to the history.

        Why: Centralizing entry creation here ensures all records are
             consistently formed and the caller never constructs raw entries.
        How: Wraps arguments in a CalculationEntry and appends to the
             internal list. Call site is responsible for only recording
             successful operations.
        """
        entry = CalculationEntry(
            operation=operation,
            left_operand=left_operand,
            right_operand=right_operand,
            result=result,
        )
        self._entries.append(entry)

    def get_entries(self) -> list[CalculationEntry]:
        """Return a shallow copy of all recorded calculation entries.

        Why: Returning the internal list directly would allow callers to
             mutate history state without going through the public API.
        How: list() creates a shallow copy; CalculationEntry is a dataclass
             (effectively immutable for our purposes) so shallow copy is safe.
        """
        return list(self._entries)

    def clear(self) -> None:
        """Remove all entries from the history.

        Why: Resetting history is needed for scenarios such as starting a
             new calculation session without creating a new instance.
        How: Reassigns the internal list to a new empty list rather than
             mutating the existing one, avoiding aliasing issues.
        """
        self._entries = []

    def export_to_json(self, file_path: Path) -> None:
        """Serialize all history entries to a JSON file at the given path.

        Why: Persistent export allows users to audit or analyse calculation
             history outside of the application session.
        How: Converts each CalculationEntry to a dict via dataclasses.asdict,
             then writes a JSON array to the file using UTF-8 encoding with
             human-readable indentation.
        """
        serialized = [asdict(entry) for entry in self._entries]
        file_path.write_text(
            json.dumps(serialized, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
