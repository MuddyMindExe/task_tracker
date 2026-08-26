import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.users.schemas import UserCreate, UserUpdate
from src.users.dependencies import get_user_storage, UserJsonStorage

client = TestClient(app)
test_json_file = "tests/users.json"
app.dependency_overrides[get_user_storage] = lambda: UserJsonStorage(test_json_file)

def clear_file():
    with open(test_json_file, "w", encoding="utf-8") as file:
        file.write("{}")

@pytest.fixture(autouse=True)
def rollback_json():
    clear_file()
    yield
    clear_file()

@pytest.fixture
def users() -> tuple[UserCreate, UserCreate, UserCreate]:
    return (
        UserCreate(name="name_1", login="login_1", email="email1@gmail.com", password="pass1"),
        UserCreate(name="name_2", login="login_2", email="email2@gmail.com", password="pass2"),
        UserCreate(name="name_3", login="login_3", email="email3@gmail.com", password="pass3"),
            )

@pytest.fixture
def full_file(users):
    user1, user2, user3 = users
    for task in users:
        client.post("/users", json=task.model_dump())
    awaited_json_state = {
        '1': user1.model_dump(),
        '2': user2.model_dump(),
        '3': user3.model_dump(),
    }
    return awaited_json_state

class TestShowUser:
    def test_show_user(self, users):
        client.post("/users/1", json=users[0].model_dump())
        assert client.get("/users/1").json() == users[0].model_dump()
        assert client.get("/users/0").status_code == 404

class TestAddUser:
    def test_add_user(self, users):
        response = client.post("/users/1", json=users[0].model_dump())
        assert response.status_code == 201
        assert response.json() == users[0].model_dump()

class TestChangeTask:
    def test_change_task(self, users):
        client.post("/users/1", json=users[0].model_dump())
        response = client.patch("/users/1", json=UserUpdate(name="changed").model_dump())
        user_to_check = users[0]
        user_to_check.name = "changed"
        assert response.status_code == 200
        assert response.json() == user_to_check.model_dump()

class TestDeleteTask:
    def test_delete_task(self, users):
        client.post("/users/1", json=users[0].model_dump())
        assert client.delete("/users/1").status_code == 204
        assert client.get("/users/1").status_code == 404
