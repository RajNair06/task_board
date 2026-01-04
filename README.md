## Real-time Collaborative Task Board (WIP)

This repository contains the backend for a Trello-like real-time collaborative task board. The project is a work in progress and currently implements core API endpoints, role-based access control (RBAC), and tests covering boards, members, and cards.

Status
 - Work in progress: core board, card, and auth features implemented
 - RBAC with roles: owner, editor, viewer
 - Unit tests for board/card flows included

Getting started
1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run tests:

```bash
python -m pytest
```

Project overview
 - `main.py` — FastAPI app and lifespan initialization
 - `routers/` — API route definitions for auth, boards, and cards
 - `commands/` and `queries/` — command/query handlers for business logic
 - `db/` — SQLAlchemy models and DB setup
 - `schemas/` — Pydantic models for request/response validation
 - `utils/` — authentication and permission helpers
 - `tests/` — test suite validating core flows and RBAC


