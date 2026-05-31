# devbin

A developer pastebin — save and manage code snippets, notes, and scripts. Each user has their own private collection of pastes, stored in a database and accessible from any browser.

## Stack

- **Frontend** — plain HTML/JS + highlight.js, served by nginx
- **Backend** — FastAPI (Python) REST API
- **Database** — SQLite (file-based, zero config)
- **Container** — Docker Compose

## Quick start

### Prerequisites

- Docker Desktop installed and running
- Git

### Run locally

```bash
git clone https://github.com/YOUR_USERNAME/devbin.git
cd devbin
docker compose up --build
```

Then open **http://localhost:3000** in your browser.

- Register an account with any email + password
- Start saving pastes — they're stored in `./data/devbin.db` on your machine
- Each user only sees their own pastes

### Stop

```bash
docker compose down
```

Your data in `./data/` is preserved between restarts.

## Project structure

```
devbin/
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
│   ├── main.py          # FastAPI routes
│   ├── models.py        # SQLAlchemy DB models
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── auth.py          # Password hashing + JWT tokens
│   ├── database.py      # DB connection setup
│   └── requirements.txt
├── frontend/
│   ├── Dockerfile       # nginx serving index.html
│   └── index.html       # Full UI
└── data/                # SQLite DB lives here (git-ignored)
```

## API endpoints

| Method | Path          | Description       |
| ------ | ------------- | ----------------- |
| POST   | `/register`   | Create account    |
| POST   | `/login`      | Get JWT token     |
| GET    | `/me`         | Current user info |
| GET    | `/pastes`     | List your pastes  |
| POST   | `/pastes`     | Create a paste    |
| PUT    | `/pastes/:id` | Update a paste    |
| DELETE | `/pastes/:id` | Delete a paste    |

Interactive API docs available at **http://localhost:8000/docs** when running.

## Configuration

Change the `SECRET_KEY` in `docker-compose.yml` before sharing the app with anyone:

```yaml
environment:
  - SECRET_KEY=your-long-random-secret-here
```

Generate a good one with:

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

## Supported languages

Plain text, Markdown, JavaScript, TypeScript, Python, C, C++, Java, C#, Go, Rust, PHP, Ruby, Swift, Kotlin, Shell/Bash, SQL, HTML, CSS, JSON, YAML, XML, Dockerfile, INI/Config, Diff — and more can be added easily.
