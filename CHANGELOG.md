# Changelog

All notable changes to **agent-dispatcher** will be documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), versioning follows [SemVer](https://semver.org/).

## [1.0.0] — 2026-03-24

### Added
- `Task` dataclass with `id`, `func`, `args`, `kwargs`, `priority`, `status`, `result`, `error`, `duration_ms`, and `to_dict()`.
- `DispatchResult` with `task_id`, `success`, `result`, `error`, `duration_ms`, and `to_dict()`.
- `Dispatcher` with `submit()`, `dispatch()`, `dispatch_nowait()`, `results` property, `shutdown()`, and context-manager support.
- `@dispatch_parallel` decorator for zero-boilerplate parallel function calls.
- Zero external dependencies — pure Python stdlib (`concurrent.futures`).
- Full pytest test suite (22+ tests).
