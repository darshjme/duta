<div align="center">
<img src="assets/hero.svg" width="100%"/>
</div>

# agent-dispatcher

**Concurrent task dispatcher for parallel agent execution**

[![PyPI version](https://img.shields.io/pypi/v/agent-dispatcher?color=blue&style=flat-square)](https://pypi.org/project/agent-dispatcher/) [![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square)](https://python.org) [![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE) [![Tests](https://img.shields.io/badge/tests-passing-brightgreen?style=flat-square)](#)

---

## The Problem

Without a dispatcher, event handling logic scatters across every handler that checks `if event.type == ...`. Adding a new handler requires modifying existing code; removing one silently breaks others. The fan-out problem compounds with agent complexity.

## Installation

```bash
pip install agent-dispatcher
```

## Quick Start

```python
from agent_dispatcher import Dispatcher, DispatchResult

# Initialise
instance = Dispatcher(name="my_agent")

# Use
result = instance.run()
print(result)
```

## API Reference

### `Dispatcher`

```python
class Dispatcher:
    """
    def __init__(self, max_workers: int = 4, timeout_seconds: float = 30.0) -> None:
    def _get_executor(self) -> ThreadPoolExecutor:
    def _run_task(self, task: Task) -> DispatchResult:
```

### `DispatchResult`

```python
class DispatchResult:
    """Holds the outcome of a dispatched Task."""
    def __init__(
    def to_dict(self) -> dict:
    def __repr__(self) -> str:
```


## How It Works

### Flow

```mermaid
flowchart LR
    A[User Code] -->|create| B[Dispatcher]
    B -->|configure| C[DispatchResult]
    C -->|execute| D{Success?}
    D -->|yes| E[Return Result]
    D -->|no| F[Error Handler]
    F --> G[Fallback / Retry]
    G --> C
```

### Sequence

```mermaid
sequenceDiagram
    participant App
    participant Dispatcher
    participant DispatchResult

    App->>+Dispatcher: initialise()
    Dispatcher->>+DispatchResult: configure()
    DispatchResult-->>-Dispatcher: ready
    App->>+Dispatcher: run(context)
    Dispatcher->>+DispatchResult: execute(context)
    DispatchResult-->>-Dispatcher: result
    Dispatcher-->>-App: WorkflowResult
```

## Philosophy

> *Indra* dispatched messengers across the cosmos; routing is the oldest form of orchestration.

---

*Part of the [arsenal](https://github.com/darshjme/arsenal) — production stack for LLM agents.*

*Built by [Darshankumar Joshi](https://github.com/darshjme), Gujarat, India.*
