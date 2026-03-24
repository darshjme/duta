"""Tests for Dispatcher."""

import time
import pytest
from concurrent.futures import Future

from agent_dispatcher import Dispatcher, Task, DispatchResult


def add(a, b):
    return a + b


def slow(n):
    time.sleep(n)
    return n


def boom():
    raise ValueError("intentional error")


def echo(x):
    return x


class TestDispatcherBasic:
    def test_dispatch_single_task(self):
        d = Dispatcher()
        tasks = [Task(id="t1", func=add, args=(2, 3))]
        results = d.dispatch(tasks)
        d.shutdown()
        assert len(results) == 1
        assert results[0].success is True
        assert results[0].result == 5

    def test_dispatch_multiple_tasks(self):
        d = Dispatcher(max_workers=4)
        tasks = [Task(id=str(i), func=add, args=(i, i)) for i in range(5)]
        results = d.dispatch(tasks)
        d.shutdown()
        assert len(results) == 5
        assert all(r.success for r in results)
        result_map = {r.task_id: r.result for r in results}
        for i in range(5):
            assert result_map[str(i)] == i * 2

    def test_dispatch_returns_dispatch_results(self):
        d = Dispatcher()
        tasks = [Task(id="x", func=echo, args=("hello",))]
        results = d.dispatch(tasks)
        d.shutdown()
        assert isinstance(results[0], DispatchResult)

    def test_duration_ms_populated(self):
        d = Dispatcher()
        tasks = [Task(id="t", func=add, args=(1, 1))]
        results = d.dispatch(tasks)
        d.shutdown()
        assert results[0].duration_ms is not None
        assert results[0].duration_ms >= 0

    def test_task_status_updated_to_completed(self):
        d = Dispatcher()
        task = Task(id="s", func=add, args=(1, 1))
        d.dispatch([task])
        d.shutdown()
        assert task.status == "completed"

    def test_task_result_set(self):
        d = Dispatcher()
        task = Task(id="s2", func=add, args=(10, 20))
        d.dispatch([task])
        d.shutdown()
        assert task.result == 30

    def test_parallel_speedup(self):
        """10 parallel 0.1s sleeps should finish well under 1s."""
        d = Dispatcher(max_workers=10)
        tasks = [Task(id=str(i), func=slow, args=(0.1,)) for i in range(10)]
        start = time.perf_counter()
        d.dispatch(tasks)
        elapsed = time.perf_counter() - start
        d.shutdown()
        assert elapsed < 1.0, f"Expected parallel execution, took {elapsed:.2f}s"


class TestDispatcherErrors:
    def test_failing_task_marked_failed(self):
        d = Dispatcher()
        task = Task(id="fail", func=boom)
        results = d.dispatch([task])
        d.shutdown()
        assert results[0].success is False
        assert "intentional error" in results[0].error
        assert task.status == "failed"

    def test_failing_task_error_set_on_task(self):
        d = Dispatcher()
        task = Task(id="fail2", func=boom)
        d.dispatch([task])
        d.shutdown()
        assert task.error is not None
        assert "intentional error" in task.error

    def test_mixed_success_and_failure(self):
        d = Dispatcher(max_workers=4)
        tasks = [
            Task(id="ok", func=add, args=(1, 2)),
            Task(id="bad", func=boom),
        ]
        results = d.dispatch(tasks)
        d.shutdown()
        result_map = {r.task_id: r for r in results}
        assert result_map["ok"].success is True
        assert result_map["bad"].success is False

    def test_timeout_marks_task(self):
        d = Dispatcher(max_workers=1, timeout_seconds=0.05)
        task = Task(id="slow", func=slow, args=(5.0,))
        results = d.dispatch([task])
        d.shutdown(wait=False)
        assert results[0].success is False
        assert "timed out" in results[0].error.lower()


class TestDispatcherSubmit:
    def test_submit_returns_task_id(self):
        d = Dispatcher()
        task = Task(id="sub1", func=add, args=(1, 1))
        returned_id = d.submit(task)
        assert returned_id == "sub1"
        d.shutdown()

    def test_results_populated_after_submit(self):
        d = Dispatcher()
        task = Task(id="sub2", func=add, args=(3, 4))
        d.submit(task)
        time.sleep(0.2)  # let it finish
        assert "sub2" in d.results
        d.shutdown()


class TestDispatchNowait:
    def test_returns_dict_of_futures(self):
        d = Dispatcher()
        tasks = [Task(id="nw1", func=add, args=(1, 2)), Task(id="nw2", func=add, args=(3, 4))]
        futures = d.dispatch_nowait(tasks)
        assert isinstance(futures, dict)
        assert set(futures.keys()) == {"nw1", "nw2"}
        assert all(isinstance(f, Future) for f in futures.values())
        # Wait for completion
        for f in futures.values():
            f.result(timeout=5)
        d.shutdown()


class TestDispatcherContextManager:
    def test_context_manager(self):
        with Dispatcher(max_workers=2) as d:
            tasks = [Task(id="cm1", func=add, args=(5, 5))]
            results = d.dispatch(tasks)
        assert results[0].result == 10

    def test_results_property(self):
        with Dispatcher() as d:
            tasks = [Task(id="rp1", func=add, args=(7, 8))]
            d.dispatch(tasks)
        # After context exit, results still accessible
        assert "rp1" in d.results
        assert d.results["rp1"].result == 15

    def test_repr(self):
        d = Dispatcher(max_workers=6, timeout_seconds=15.0)
        r = repr(d)
        assert "6" in r
        assert "15.0" in r
