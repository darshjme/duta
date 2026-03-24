"""Task — a dispatchable unit of work."""

from __future__ import annotations
from typing import Any, Callable, Optional


class Task:
    """A dispatchable unit of work for the Dispatcher."""

    def __init__(
        self,
        id: str,
        func: Callable,
        args: tuple = (),
        kwargs: Optional[dict] = None,
        priority: int = 0,
    ) -> None:
        self.id = id
        self.func = func
        self.args = args
        self.kwargs = kwargs if kwargs is not None else {}
        self.priority = priority
        self.status: str = "pending"
        self.result: Any = None
        self.error: Optional[str] = None
        self.duration_ms: Optional[float] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "func": getattr(self.func, "__name__", str(self.func)),
            "args": self.args,
            "kwargs": self.kwargs,
            "priority": self.priority,
            "status": self.status,
            "result": self.result,
            "error": self.error,
            "duration_ms": self.duration_ms,
        }

    def __repr__(self) -> str:
        return f"Task(id={self.id!r}, status={self.status!r}, priority={self.priority})"
