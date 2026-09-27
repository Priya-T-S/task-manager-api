# Task Manager API - Test Cases

## POST /tasks

### TC-001: Create task with valid data
Precondition:
- API server is running.

Steps:
1. Send POST request to `/tasks`.
2. Provide a valid title.
3. Provide a description.
4. Check the response.

Expected:
- Status code is 200.
- Task is created.
- Response contains task ID.
- Title and description match the request.
- `completed` defaults to false.

---

### TC-002: Create task with title only

Steps:
1. Send POST request to `/tasks`.
2. Provide only a title.

Expected:
- Status code is 200.
- Task is created.
- Description is null.
- `completed` is false.

---

### TC-003: Create task without title

Steps:
1. Send POST request to `/tasks`.
2. Omit the title.

Expected:
- Request is rejected.
- Status code is 422.

---

### TC-004: Create task with invalid data type

Steps:
1. Send POST request to `/tasks`.
2. Send an invalid value for `completed`.

Expected:
- Request is rejected.
- Status code is 422.


## GET /tasks

### TC-005: Retrieve all tasks

Precondition:
- API server is running.
- At least one task exists.

Steps:
1. Send GET request to `/tasks`.
2. Check the response.

Expected:
- Status code is 200.
- Response is JSON.
- Created tasks are returned.


---

### TC-006: Retrieve tasks when no tasks exist

Precondition:
- No tasks exist.

Steps:
1. Send GET request to `/tasks`.
2. Check the response.

Expected:
- Status code is 200.
- Response is an empty list.


## DELETE /tasks/{task_id}

### TC-007: Delete an existing task

Precondition:
- At least one task exists.

Steps:
1. Create a task.
2. Note its task ID.
3. Send DELETE request using that ID.
4. Send GET request to `/tasks`.

Expected:
- DELETE returns 200.
- Success message is returned.
- Deleted task no longer appears in GET /tasks.


---

### TC-008: Delete a non-existent task

Steps:
1. Send DELETE request using a task ID that does not exist.

Expected:
- Status code is 404.
- Error message is returned.

