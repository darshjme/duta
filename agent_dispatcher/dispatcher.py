"""Dispatcher — runs tasks concurrently using a ThreadPoolExecutor."""

from __future__ import annotations

import time
from concurrent.futures import Future, ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from typing import Optional

from .task import Task
from .result import DispatchResult


class Dispatcher:
    """
    Concurrent task dispatcher backed by a thread pool.

    Example::

        dispatcher = Dispatcher(max_workers=8)
        tasks = [Task(id=str(i), func=my_fn, args=(i,)) for i in range(10)]
        results = dispatcher.dispatch(tasks)
        dispatcher.shutdown()
    """

    def __init__(self, max_workers: int = 4, timeout_seconds: float = 30.0) -> None:
        self.max_workers = max_workers
        self.timeout_seconds = timeout_seconds
        self._executor: Optional[ThreadPoolExecutor] = None
        self._results: dict[str, DispatchResult] = {}

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_executor(self) -> ThreadPoolExecutor:
        if self._executor is None or self._executor._shutdown:
            self._executor = ThreadPoolExecutor(max_workers=self.max_workers)
        return self._executor

    def _run_task(self, task: Task) -> DispatchResult:
        task.status = "running"
        start = time.perf_counter()
        try:
            value = task.func(*task.args, **task.kwargs)
            elapsed_ms = (time.perf_counter() - start) * 1000
            task.status = "completed"
            task.result = value
            task.duration_ms = elapsed_ms
            dr = DispatchResult(
                task_id=task.id,
                success=True,
                result=value,
                error=None,
                duration_ms=elapsed_ms,
            )
        except Exception as exc:  # noqa: BLE001
            elapsed_ms = (time.perf_counter() - start) * 1000
            task.status = "failed"
            task.error = str(exc)
            task.duration_ms = elapsed_ms
            dr = DispatchResult(
                task_id=task.id,
                success=False,
                result=None,
                error=str(exc),
                duration_ms=elapsed_ms,
            )
        self._results[task.id] = dr
        return dr

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def submit(self, task: Task) -> str:
        """Submit a single task for async execution. Returns task_id."""
        executor = self._get_executor()
        executor.submit(self._run_task, task)
        return task.id

    def dispatch(self, tasks: list[Task]) -> list[DispatchResult]:
        """
        Run all tasks concurrently and wait for all to finish (or timeout).
        Returns a list of DispatchResult in the same order as *tasks*.
        """
        executor = self._get_executor()
        future_map: dict[Future, Task] = {
            executor.submit(self._run_task, task): task for task in tasks
        }
        results: list[DispatchResult] = []
        for future, task in future_map.items():
            try:
                dr = future.result(timeout=self.timeout_seconds)
            except FuturesTimeoutError:
                elapsed_ms = self.timeout_seconds * 1000
                task.status = "timeout"
                task.error = "Task timed out"
                task.duration_ms = elapsed_ms
                dr = DispatchResult(
                    task_id=task.id,
                    success=False,
                    result=None,
                    error="Task timed out",
                    duration_ms=elapsed_ms,
                )
                self._results[task.id] = dr
            except Exception as exc:  # noqa: BLE001
                dr = DispatchResult(
                    task_id=task.id,
                    success=False,
                    result=None,
                    error=str(exc),
                    duration_ms=0.0,
                )
                self._results[task.id] = dr
            results.append(dr)
        return results

    def dispatch_nowait(self, tasks: list[Task]) -> dict[str, Future]:
        """
        Fire-and-forget: submit all tasks, return a mapping of task_id -> Future.
        The caller can inspect futures whenever convenient.
        """
        executor = self._get_executor()
        return {task.id: executor.submit(self._run_task, task) for task in tasks}

    @property
    def results(self) -> dict[str, DispatchResult]:
        """All completed DispatchResult objects keyed by task_id."""
        return dict(self._results)

    def shutdown(self, wait: bool = True) -> None:
        """Shut down the underlying thread pool."""
        if self._executor is not None:
            self._executor.shutdown(wait=wait)
            self._executor = None

    def __enter__(self) -> "Dispatcher":
        return self

    def __exit__(self, *_) -> None:
        self.shutdown()

    def __repr__(self) -> str:
        return (
            f"Dispatcher(max_workers={self.max_workers}, "
            f"timeout_seconds={self.timeout_seconds})"
        )
