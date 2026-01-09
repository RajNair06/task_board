# Real-time Collaborative Task Board

A FastAPI-based backend for a Trello-like real-time collaborative task board with role-based access control (RBAC), audit logging, and activity feed functionality.

## Status

- ✅ Core board, card, and authentication features implemented
- ✅ Role-based access control (RBAC) with roles: owner, editor, viewer
- ✅ Audit logging for board and card operations
- ✅ Activity feed with Celery async task processing
- ✅ Comprehensive unit tests covering auth, board, and card flows
- ✅ Member management and board sharing

## Features

### Authentication & Authorization

- User registration and login with JWT tokens
- Secure password hashing with passlib
- Role-based access control on boards
- Permission validation for all operations

### Board Management

- Create, read, update, and delete boards
- Add/remove board members with role assignment
- Update member roles (owner, editor, viewer)
- List user's accessible boards

### Card Management

- Create, update, and delete cards within boards
- Card positioning/ordering support
- Card completion status tracking
- Card metadata (title, description, timestamps)

### Audit & Activity Feed

- Comprehensive audit logging for all board and card operations
- Async activity feed generation using Celery
- Detailed activity messages tracking all changes
- Member management history

## Tech Stack

- **Framework**: FastAPI 0.123
- **Database**: SQLAlchemy ORM
- **Task Queue**: Celery 5.6.2 with Redis
- **Validation**: Pydantic 2.12
- **Authentication**: python-jose, passlib
- **Testing**: pytest
- **API Security**: OAuth2 with JWT

## Project Structure

```
task_board/
├── main.py                 # FastAPI app and lifespan initialization
├── routers/               # API route definitions (auth, boards, cards)
├── commands/              # Command handlers for business logic operations
├── queries/               # Query handlers for data retrieval
├── db/                    # SQLAlchemy models and database setup
├── schemas/               # Pydantic models for request/response validation
├── utils/                 # Authentication and permission utilities
├── tasks/                 # Celery async tasks and activity feed
└── tests/                 # Comprehensive test suite
```

## Getting Started

### Prerequisites

- Python 3.8+
- Redis (for Celery)
- PostgreSQL (or SQLite for local development)

### Installation

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

### Running the Application

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`. OpenAPI docs at `/docs`.

### Running Tests

```bash
python -m pytest
```

### Running Celery Worker (for activity feed)

```bash
celery -A tasks.celery_config worker --loglevel=info
```

## API Endpoints

### Authentication

- `POST /auth/register` — Register new user
- `POST /auth/login` — User login (returns JWT token)

### Boards

- `POST /boards` — Create new board
- `GET /boards` — List user's accessible boards
- `GET /boards/{id}` — Get board details
- `PUT /boards/{id}` — Update board
- `DELETE /boards/{id}` — Delete board
- `POST /boards/{id}/members` — Add member to board
- `PUT /boards/{id}/members/{user_id}` — Update member role
- `DELETE /boards/{id}/members/{user_id}` — Remove member from board

### Cards

- `POST /boards/{board_id}/cards` — Create card
- `GET /boards/{board_id}/cards` — List board cards
- `GET /cards/{id}` — Get card details
- `PUT /cards/{id}` — Update card
- `DELETE /cards/{id}` — Delete card

### Activity Feed

- `GET /boards/{board_id}/activity` — Get board activity feed
