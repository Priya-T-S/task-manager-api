import pytest
from playwright.sync_api import Page


@pytest.fixture
def task_manager(page: Page):
    page.goto("http://localhost:8501")
    return page