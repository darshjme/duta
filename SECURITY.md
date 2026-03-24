# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.x     | ✅ Yes    |

## Reporting a Vulnerability

Please **do not** open a public GitHub issue for security vulnerabilities.

Email **darshjme@gmail.com** with:
- A description of the vulnerability.
- Steps to reproduce.
- Potential impact.

We will respond within 72 hours and coordinate a fix + disclosure timeline with you.

## Scope

- agent-dispatcher uses only Python's standard library (`concurrent.futures`).
- There is no network I/O, no serialization of untrusted data, and no subprocess execution within the library itself.
- The primary security concern is **user-supplied callables**: never dispatch untrusted code.
