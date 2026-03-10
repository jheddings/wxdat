# CLAUDE.md — wxdat

## Overview

wxdat is a weather data collection service that fetches observations from
weather APIs and stores them locally. It exports metrics to Prometheus and
runs as a long-lived service, typically in Docker.

## Commit Conventions

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <description>
```

Types: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `style`, `perf`

Scope is optional but encouraged (e.g. `fix(api): ...`, `feat(metrics): ...`).

Include the issue number when applicable (e.g. `feat: add humidity metric (#8)`).

## Branch Naming

Use the same type prefixes as commits, followed by a short description:

```
<type>/<short-description>
```

Examples: `feat/humidity-metric`, `fix/api-rate-limit`, `chore/update-deps`
