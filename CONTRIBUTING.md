# Contributing

Thank you for your interest in contributing to **agent-dispatcher**!

## Getting Started

```bash
git clone https://github.com/darshjme-codes/agent-dispatcher
cd agent-dispatcher
pip install -e ".[dev]"
```

## Running Tests

```bash
python -m pytest tests/ -v
```

## Code Style

- Follow PEP 8.
- Type-hint all public API functions.
- Keep zero runtime dependencies (stdlib only).

## Pull Request Guidelines

1. Fork the repo and create a feature branch.
2. Write tests for any new behaviour.
3. Ensure `pytest` passes with no failures.
4. Open a PR with a clear description.

## Reporting Bugs

Open an issue with a minimal reproducible example.
