import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.title("Task Manager")

with st.form("create_task", clear_on_submit=True):
    title = st.text_input("Title")
    description = st.text_area("Description")
    completed = st.checkbox("Completed")
    submitted = st.form_submit_button("Create Task")

if submitted:
    if not title:
        st.error("Title is required")
    else:
        try:
            response = requests.post(
                f"{API_URL}/tasks",
                json={"title": title, "description": description or None, "completed": completed},
            )
            response.raise_for_status()
            st.success(f"Created task #{response.json()['id']}")
        except requests.RequestException as e:
            st.error(f"Could not create task: {e}")

st.subheader("Tasks")
try:
    tasks = requests.get(f"{API_URL}/tasks").json()
    if tasks:
        st.table(tasks)
    else:
        st.info("No tasks yet")
except requests.RequestException:
    st.error("Backend not reachable. Start it with: uvicorn app.main:app --reload")
