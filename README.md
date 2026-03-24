<div align="center">
<img src="assets/hero.svg" width="100%"/>
</div>

# agent-dispatcher

**Concurrent parallel task execution for LLM agents. Zero external dependencies.**

[![PyPI](https://img.shields.io/pypi/v/agent-dispatcher?color=blue)](https://pypi.org/project/agent-dispatcher/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Zero deps](https://img.shields.io/badge/dependencies-zero-brightgreen)](pyproject.toml)

---

## The Problem

Production LLM agents fail silently. Without concurrent parallel task execution, you get undefined behaviour at scale — race conditions, lost state, cascading failures, and no way to debug what went wrong.

`agent-dispatcher` gives you a production-ready concurrent parallel task execution primitive with a clean API, tested edge cases, and zero configuration.

## Installation

```bash
pip install agent-dispatcher
```

Or from source:

```bash
git clone https://github.com/darshjme/agent-dispatcher.git
cd agent-dispatcher
pip install -e .
```

## Quick Start

```python
from agent_dispatcher import *  # see API reference below

# See examples/ directory for complete working examples
```

## API Reference

The main classes and functions are defined in `agent_dispatcher/__init__.py`.

Key exports: `ThreadPoolExecutor · @dispatch_parallel · result aggregation`

All classes follow a consistent interface:
- Instantiate with sensible defaults
- Compose with other arsenal libraries
- Zero external dependencies required

See the source code and `tests/` directory for verified usage examples.

## How It Works

```mermaid
flowchart LR
    A[Agent Task] --> B[agent-dispatcher]
    B --> C{Decision}
    C -->|success| D[✅ Result]
    C -->|failure| E[⚠️ Handle]
    E --> B

    style B fill:#161b22,stroke:#8957e5,stroke-width:2,color:#8957e5
    style D fill:#1a3320,stroke:#238636,color:#3fb950
    style E fill:#3d1a1a,stroke:#f85149,color:#f85149
```

```mermaid
sequenceDiagram
    participant Agent
    participant AgentDispatcher as agent-dispatcher
    participant Output

    Agent->>AgentDispatcher: initialize()
    AgentDispatcher-->>Agent: ready

    loop Agent Run
        Agent->>AgentDispatcher: process(input)
        AgentDispatcher-->>Agent: result
    end

    Agent->>Output: deliver(result)
```

## Philosophy

Indra commands the devas in parallel — each to their domain, all at once. agent-dispatcher is that command.

---

## Part of the Arsenal

`agent-dispatcher` is one of six production libraries for LLM agents:

| Library | Purpose |
|---------|---------|
| [herald](https://github.com/darshjme/herald) | Semantic task routing |
| [engram](https://github.com/darshjme/engram) | Agent memory |
| [sentinel](https://github.com/darshjme/sentinel) | ReAct loop guards |
| [verdict](https://github.com/darshjme/verdict) | Agent evaluation |
| [agent-guardrails](https://github.com/darshjme/agent-guardrails) | Output validation |
| [agent-observability](https://github.com/darshjme/agent-observability) | Tracing & metrics |

→ [arsenal](https://github.com/darshjme/arsenal) — the complete stack

---

*Built by [Darshankumar Joshi](https://github.com/darshjme), Gujarat, India.*
