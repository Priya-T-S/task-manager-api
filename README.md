# Task Manager API

A small task manager with a **FastAPI** backend, a **Streamlit** frontend, and an automated QA suite (pytest + Playwright) that runs in GitHub Actions.

## Features

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/tasks` | Create a task (`title` required; `description` and `completed` optional) |
| `GET` | `/tasks` | List all tasks |
| `DELETE` | `/tasks/{task_id}` | Delete a task (404 if it doesn't exist) |

The Streamlit frontend has a form for creating tasks and a table of existing tasks.

> Tasks are stored in memory and are lost when the server restarts.

## Project structure

```
app/                  FastAPI backend (main.py, models.py)
frontend/             Streamlit UI (app.py)
tests/
  api/                API tests (TestClient, no servers needed)
  ui/                 Playwright end-to-end tests
docs/requirements.md  Product requirements
QA.md                 Testing strategy, test cases, CI flow
.github/workflows/    CI pipeline
```

## Getting started

```bash
python -m venv venv
venv\Scripts\activate             # Windows
# source venv/bin/activate        # macOS / Linux
pip install -r requirements-dev.txt   # or requirements.txt to run the app only
playwright install chromium
```

Run the app (two terminals):

```bash
uvicorn app.main:app --reload     # API on http://localhost:8000  (docs at /docs)
streamlit run frontend/app.py     # UI  on http://localhost:8501
```

## Testing

```bash
pytest -m api     # API tests only, no servers needed
pytest -m ui      # UI tests, needs both apps running
pytest            # everything
```

When a UI test fails, a screenshot, trace and video are saved to `test-results/`. CI also uploads them as a build artifact.

See **[QA.md](QA.md)** for the full testing strategy, test cases and CI/CD flow.
