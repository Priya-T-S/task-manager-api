from playwright.sync_api import Page


def test_create_task(task_manager: Page):
    task_manager.get_by_label("Title").fill("Playwright Task")
    task_manager.get_by_label("Description").fill("Testing task creation")

    task_manager.get_by_role("button", name="Create Task").click()

    task_manager.get_by_text("Created task").wait_for()

    assert task_manager.get_by_text("Created task").is_visible()


def test_create_task_without_title(task_manager: Page):
    task_manager.get_by_role("button", name="Create Task").click()

    task_manager.get_by_text("Title is required").wait_for()

    assert task_manager.get_by_text("Title is required").is_visible()


def test_create_task_with_title_only(task_manager: Page):
    task_manager.get_by_label("Title").fill("Title Only Task")

    task_manager.get_by_role("button", name="Create Task").click()

    task_manager.get_by_text("Created task").wait_for()

    assert task_manager.get_by_text("Created task").is_visible()


def test_task_appears_in_list(task_manager: Page):
    task_manager.get_by_label("Title").fill("Visible Task")
    task_manager.get_by_label("Description").fill("Check task display")

    task_manager.get_by_role("button", name="Create Task").click()

    task_manager.get_by_text("Created task").wait_for()
    task_manager.get_by_text("Visible Task").first.wait_for()

    assert task_manager.get_by_text("Visible Task").first.is_visible()