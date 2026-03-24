"""@dispatch_parallel decorator — run a function in parallel over many arg-tuples."""

from __future__ import annotations

import functools
import uuid
from typing import Any, Callable

from .task import Task
from .dispatcher import Dispatcher


def dispatch_parallel(max_workers: int = 4, timeout_seconds: float = 30.0):
    """
    Decorator factory.  Wrap a function so that calling it with a *list of
    arg-tuples* dispatches each tuple as a parallel task.

    Example::

        @dispatch_parallel(max_workers=8)
        def call_llm(prompt: str) -> str:
            return llm.complete(prompt)

        results = call_llm([("Tell me a joke",), ("Explain gravity",)])
        # returns list of raw return values (or raises on failure)
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(arg_tuples: list[tuple], **shared_kwargs) -> list[Any]:
            tasks = [
                Task(
                    id=str(uuid.uuid4()),
                    func=func,
                    args=arg_tuple if isinstance(arg_tuple, tuple) else (arg_tuple,),
                    kwargs=shared_kwargs,
                )
                for arg_tuple in arg_tuples
            ]
            with Dispatcher(max_workers=max_workers, timeout_seconds=timeout_seconds) as d:
                dispatch_results = d.dispatch(tasks)

            # Raise on first failure, otherwise return raw results in order
            out = []
            for dr in dispatch_results:
                if not dr.success:
                    raise RuntimeError(
                        f"Task {dr.task_id} failed: {dr.error}"
                    )
                out.append(dr.result)
            return out

        return wrapper

    return decorator
