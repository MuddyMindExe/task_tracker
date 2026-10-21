import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.tasks.schemas import TaskStatus, TaskCreate, TaskUpdate
from src.tasks.dependencies import get_task_storage, TaskJsonStorage
from src.tasks.dependencies import tasks as in_memory
from src.database import engine

client = TestClient(app)
test_json_file = "tests/tasks.json"
app.dependency_overrides[get_task_storage] = lambda: TaskJsonStorage(test_json_file)
app.dependency_overrides[get_task_storage] = lambda: in_memory
app.dependency_overrides[get_task_storage] = lambda: engine

def clear_memory():
    in_memory.tasks = {}
    in_memory.current_id = 1

def clear_file():
    with open(test_json_file, "w", encoding="utf-8") as file:
        file.write("{}")

def clear_sql():
    pass

def clear_all():
    clear_memory()
    clear_file()
    clear_sql()

@pytest.fixture(autouse=True)
def rollback_json():
    clear_file()
    yield
    clear_file()

@pytest.fixture
def tasks() -> tuple[TaskCreate, TaskCreate, TaskCreate]:
    return (
        TaskCreate(title="task1", description="desc1", status=TaskStatus.IN_PROGRESS, user_id=1),
        TaskCreate(title="task2", description="desc2", status=TaskStatus.IN_PROGRESS, user_id=2),
        TaskCreate(title="task3", description="desc3", status=TaskStatus.IN_PROGRESS, user_id=3),
            )

@pytest.fixture(autouse=True)
def rollback_memory():
    clear_all()
    yield
    clear_all()

@pytest.fixture
def full_file(tasks):
    task1, task2, task3 = tasks
    for task in tasks:
        client.post("/tasks", json=task.model_dump())
    awaited_json_state = {
        '1': task1.model_dump(),
        '2': task2.model_dump(),
        '3': task3.model_dump(),
    }
    return awaited_json_state


class TestShowTasks:
    def test_show_tasks(self):
        response = client.get("/tasks")
        assert response.status_code == 200
        assert response.json() == {}

    def test_show_title(self, tasks, full_file):
        assert client.get("/tasks").json() == full_file

        assert client.get("/tasks", params={'title': 'task1'}).json().get('1') == tasks[0].model_dump()
        assert client.get("/tasks", params={'title': 'tasks'}).json() == {}

        assert client.get("/tasks", params={'title': "a" * 300}).status_code == 422

    def test_show_status(self, tasks, full_file):
        assert client.get("/tasks").json() == full_file

        assert client.get("/tasks", params={'status': TaskStatus.IN_PROGRESS.value}).json() == full_file
        assert client.get("/tasks", params={'status': TaskStatus.COMPLETE.value}).json() == {}

        assert client.get("/tasks", params={'status': 0}).status_code == 422

class TestShowTask:
    def test_show_task(self, tasks):
        client.post("/tasks", json=tasks[0].model_dump())
        assert client.get("/tasks/1").json() == tasks[0].model_dump()
        assert client.get("tasks/0").status_code == 422

class TestAddTask:
    def test_add_task(self, tasks):
        response = client.post("/tasks", json=tasks[0].model_dump())
        assert response.status_code == 201
        assert response.json() == tasks[0].model_dump()

class TestChangeTask:
    def test_change_task(self, tasks):
        client.post("/tasks", json=tasks[0].model_dump())
        changes = TaskUpdate(title="changed")
        response = client.patch("/tasks/1", json=changes.model_dump())
        task_to_check = tasks[0]
        task_to_check.title = "changed"
        assert response.status_code == 200
        assert response.json() == task_to_check.model_dump()

class TestDeleteTask:
    def test_delete_task(self, tasks):
        client.post("/tasks", json=tasks[0].model_dump())
        assert client.delete(f"/tasks/1").status_code == 204
        assert client.get("/tasks").json() == {}
