"""DispatchResult — result of a dispatched task."""

from __future__ import annotations
from typing import Any, Optional


class DispatchResult:
    """Holds the outcome of a dispatched Task."""

    def __init__(
        self,
        task_id: str,
        success: bool,
        result: Any = None,
        error: Optional[str] = None,
        duration_ms: float = 0.0,
    ) -> None:
        self.task_id = task_id
        self.success = success
        self.result = result
        self.error = error
        self.duration_ms = duration_ms

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "success": self.success,
            "result": self.result,
            "error": self.error,
            "duration_ms": self.duration_ms,
        }

    def __repr__(self) -> str:
        status = "OK" if self.success else f"ERR({self.error})"
        return f"DispatchResult(task_id={self.task_id!r}, {status}, {self.duration_ms:.1f}ms)"
