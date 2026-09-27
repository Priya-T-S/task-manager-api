import os

import pytest
from playwright.sync_api import Page

UI_URL = os.getenv("UI_URL", "http://localhost:8501")


@pytest.fixture
def task_manager(page: Page):
    page.goto(UI_URL)
    return page
