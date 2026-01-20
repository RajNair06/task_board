# Real-time Collaborative Task Board

A FastAPI-based backend for a Trello-like real-time collaborative task board with role-based access control (RBAC), audit logging, and activity feed functionality.

## Status

- ✅ Core board, card, and authentication features implemented
- ✅ Role-based access control (RBAC) with roles: owner, editor, viewer
- ✅ Audit logging for board and card operations
- ✅ Activity feed with Celery async task processing
- ✅ Comprehensive unit tests covering auth, board, and card flows
- ✅ Member management and board sharing
- ✅ Docker containerization with Docker Compose
- ✅ Home page documentation at `/`

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

### Real-time Collaboration

- WebSocket-based real-time updates for board collaboration
- Join/leave board rooms for live synchronization
- Secure WebSocket authentication with JWT tokens
- Automatic broadcasting of activity feed updates to connected clients
- Redis pub/sub integration for cross-instance event propagation
- Broadcasting mechanism: Redis listener

### Audit & Activity Feed

- Comprehensive audit logging for all board and card operations
- Async activity feed generation using Celery
- Detailed activity messages tracking all changes
- Member management history

## Tech Stack

- **Framework**: FastAPI 0.123
- **Database**: SQLAlchemy ORM with SQLite
- **Task Queue**: Celery 5.6.2 with RabbitMQ as broker and Redis as result backend
- **Message Broker**: RabbitMQ 3-management

- **Validation**: Pydantic 2.12
- **Authentication**: python-jose, passlib
- **Testing**: pytest
- **Containerization**: Docker & Docker Compose
- **API Security**: OAuth2 with JWT

## Project Structure

```
task_board/
├── main.py                 # FastAPI app and lifespan initialization
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Multi-service Docker setup
├── requirements.txt        # Python dependencies
├── routers/               # API route definitions (auth, boards, cards, sockets)
├── commands/              # Command handlers for business logic operations
├── queries/               # Query handlers for data retrieval
├── db/                    # SQLAlchemy models and database setup
├── schemas/               # Pydantic models for request/response validation
├── utils/                 # Authentication, permissions, and connection utilities
├── tasks/                 # Celery async tasks and activity feed
├── templates/             # Jinja2 templates for home page
├── tests/                 # Comprehensive test suite
└── .dockerignore          # Docker build exclusions
```

## Getting Started

### Prerequisites

- Docker and Docker Compose

### Quick Start with Docker

1. Clone the repository and navigate to the project directory.

2. Run the application with Docker Compose:

```bash
docker-compose up --build
```

This will start:

- **FastAPI App** at `http://localhost:8000`
- **Celery Worker** for async tasks
- **Redis** at `localhost:6379`
- **RabbitMQ** at `localhost:5672` (management UI at `http://localhost:15672`, user: guest, pass: guest)

3. Visit the home page at `http://localhost:8000` for API documentation and flow overview.

### Live Deployment

The application is deployed and available at: **https://task-board-viol.onrender.com**

You can access the API documentation and home page there as well.

### Manual Installation (Alternative)

#### Prerequisites

- Python 3.8+
- Redis
- RabbitMQ

#### Installation

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

#### Running the Application

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`. OpenAPI docs at `/docs`.

**Note**: Ensure Redis and RabbitMQ are running for real-time activity broadcasting and Celery tasks to work correctly.

#### Running Celery Worker (for activity feed)

```bash
celery -A tasks.celery_config worker --loglevel=info
```

### Running Tests

```bash
python -m pytest
```

## API Endpoints

### Home Page

- `GET /` — API documentation and flow overview (HTML page)

### Authentication

- `POST /auth/register` — Register new user
- `POST /auth/login` — User login (returns JWT token)

### Boards

- `POST /boards` — Create new board
- `GET /boards` — List user's accessible boards
- `GET /boards/{id}` — Get board details
- `PATCH /boards/{id}` — Update board
- `DELETE /boards/{id}` — Delete board
- `POST /boards/{id}/members` — Add member to board
- `PATCH /boards/{id}/members/{user_id}` — Update member role
- `DELETE /boards/{id}/members/{user_id}` — Remove member from board
- `GET /boards/{board_id}/feed` — Get board activity feed

### Cards

- `POST /boards/{board_id}/cards` — Create card
- `GET /boards/{board_id}/cards` — List board cards
- `GET /boards/{board_id}/cards/{card_id}` — Get card details
- `PATCH /boards/{board_id}/cards/{card_id}` — Update card
- `DELETE /boards/{board_id}/cards/{card_id}` — Delete card

### WebSockets

- `WS /ws?token={jwt_token}` — Real-time board collaboration
  - Send `{"type": "join", "board_id": 123}` to join a board room
  - Send `{"type": "leave"}` to leave the current board room
  - Receive activity updates with type `activity` containing board events

## Real-time Broadcasting Architecture

### Broadcasting Mechanisms

**Redis Pub/Sub Listener**: Async listener that subscribes to `board:*` channels and broadcasts messages to connected WebSocket clients in real-time.

### Event Flow

1. Action triggered (board/card creation, update, etc.)
2. Celery task (brokered by RabbitMQ) records audit log and activity feed entry
3. Event published to Redis: `redis_client.publish(f"board:{board_id}", json.dumps(payload))`
4. Redis listener receives and broadcasts to WebSocket clients
