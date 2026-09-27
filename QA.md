# QA Strategy – Task Manager

This document describes how the Task Manager (FastAPI backend + Streamlit frontend) is tested: what is covered, which tools are used, how to run the suite, and how it runs in CI.

## 1. Testing strategy

The suite has two layers:

| Layer | What it checks | How | Speed |
|-------|----------------|-----|-------|
| **API** (`tests/api`) | Endpoint behaviour, status codes, validation, error messages | FastAPI `TestClient` calls the app in-process, so no server is needed | < 1 s |
| **UI / end-to-end** (`tests/ui`) | A user can create tasks through the Streamlit form and see them listed | Playwright drives Chromium against the running frontend + backend | ~ 5–10 s |

Most of the behaviour is checked at the API level, where tests are fast and reliable. The UI tests cover only the main user journeys through the real frontend and backend.

**Test isolation**
- API tests clear the in-memory `tasks` list before and after each test (`reset_tasks` fixture), so they don't depend on each other.
- UI tests run against live servers whose data carries over between tests. Each test checks only data it created itself and doesn't assume the list starts empty.

**Types of tests covered**
- Positive: valid create / list / delete.
- Negative: missing required field, wrong data type, deleting a non-existent ID.
- Boundary: optional fields left out (description defaults to `null`, `completed` defaults to `false`).

## 2. Test cases

### API

| ID | Endpoint | Scenario | Expected | Automated test |
|----|----------|----------|----------|----------------|
| TC-001 | `POST /tasks` | Create task with title + description | 200; ID returned; fields echoed; `completed` = false | `test_create_task` |
| TC-002 | `POST /tasks` | Create task with title only | 200; `description` = null; `completed` = false | `test_create_task_without_description` |
| TC-003 | `POST /tasks` | Title missing | 422 validation error | `test_create_task_without_title` |
| TC-004 | `POST /tasks` | `completed` is not a boolean (`"banana"`) | 422 validation error | `test_create_task_invalid_completed` |
| TC-005 | `GET /tasks` | List tasks after creating one | 200; non-empty JSON list | `test_get_tasks_returns_tasks` |
| TC-006 | `GET /tasks` | List when no tasks exist | 200; empty list | *Manual (not yet automated)* |
| TC-007 | `DELETE /tasks/{id}` | Delete an existing task | 200; `"Task deleted successfully"` | `test_delete_task` |
| TC-008 | `DELETE /tasks/{id}` | Delete an ID that doesn't exist | 404; `"Task not found"` | `test_delete_nonexistent_task` |

### UI

| ID | Scenario | Expected | Automated test |
|----|----------|----------|----------------|
| UI-001 | Submit form with title + description | "Created task #N" success message | `test_create_task` |
| UI-002 | Submit form with empty title | "Title is required" error; no request sent | `test_create_task_without_title` |
| UI-003 | Submit form with title only | Success message | `test_create_task_with_title_only` |
| UI-004 | Created task shows in the task table | Task title visible in the list | `test_task_appears_in_list` |

## 3. Tools

| Tool | Purpose |
|------|---------|
| **pytest** | Test runner, fixtures, markers |
| **FastAPI TestClient** (httpx) | In-process API testing |
| **Playwright** + `pytest-playwright` | Browser automation for UI tests |
| **pytest-html** | Self-contained HTML test report |
| **GitHub Actions** | CI pipeline |

## 4. How to run tests

Setup (once):

```bash
python -m venv venv
venv\Scripts\activate            # Windows
# source venv/bin/activate       # macOS / Linux
pip install -r requirements-dev.txt
playwright install chromium
```

API tests don't need any servers running:

```bash
pytest -m api
```

UI tests need both apps running, each in its own terminal:

```bash
uvicorn app.main:app --reload
streamlit run frontend/app.py
pytest -m ui
```

Everything, with an HTML report:

```bash
pytest -v --html=reports/qa-report.html --self-contained-html
```

Useful options:
- `pytest -m ui --headed` shows the browser while the tests run.
- Set `UI_URL` to point the UI tests at a different frontend (default `http://localhost:8501`).

### Failure artifacts

`pytest.ini` configures Playwright so that when a UI test fails, it saves the following to `test-results/<test-name>/`:
- `test-failed-1.png` – screenshot at the moment of failure
- `trace.zip` – full step-by-step trace; open it with `playwright show-trace test-results/<test-name>/trace.zip`
- `video.webm` – recording of the test

Passing tests leave nothing behind.

## 5. CI/CD flow

Workflow: [`.github/workflows/qa.yml`](.github/workflows/qa.yml)

The workflow runs on every push and pull request to `main` and `develop`, in these steps:

1. Check out the code and set up Python 3.12.
2. Install `requirements-dev.txt` and Playwright Chromium.
3. Start FastAPI (port 8000) and Streamlit (port 8501) in the background.
4. Wait until both health checks respond (up to 60 s each).
5. Run the full suite (`pytest`), producing `reports/qa-report.html`.
6. Upload artifacts:
   - `qa-test-report` – the HTML report (every run)
   - `playwright-failures` – screenshots, traces and videos (failed runs only)

If any test fails, the job fails, and that failed check shows on the pull request.

**Debugging a red build:** open the run → **Artifacts** → download `playwright-failures` → look at the screenshot, or open `trace.zip` at <https://trace.playwright.dev>.

Branch flow: `feature/*` → PR into `develop` (CI must pass) → PR `develop` into `main` (CI must pass).

## 6. Regression strategy

- **Every change is regression-tested.** CI runs the full API + UI suite on every push and PR, so a change to one endpoint can't quietly break another.
- **Every bug gets a test.** When a bug is fixed, first add a test that reproduces it, then fix the bug. The test stays in the suite permanently.
- **Every feature gets tests.** A new endpoint or UI flow needs at least one positive and one negative test case, added to the tables above and automated before it's merged.
- **Quick local check.** Run `pytest -m api` before every commit (under a second). Run the full suite before opening a PR.
- **Flaky tests get fixed, not re-run.** UI tests wait for specific elements (`wait_for()`) instead of fixed sleeps. Any test that fails intermittently is investigated using its trace.

## 7. Known gaps

- **No persistent storage.** Tasks are kept in memory, so they are lost when the backend restarts. The non-functional requirement to store tasks in a database ([docs/requirements.md](docs/requirements.md)) isn't met yet.
- **TC-006 is manual.** The empty-list case isn't automated yet.
- **Duplicate titles in UI-004.** UI-004 uses a fixed title and `.first`, so a leftover row with the same title from an earlier run could make the test pass even if the new task wasn't displayed. Using a unique title per run would make it stricter.
