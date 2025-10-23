import pytest


async def test_create_and_list_todos(async_client):
    # Create a new todo
    todo_data = {"title": "Test Todo", "description": "A test todo", "completed": False}
    create_resp = await async_client.post("/todos", json=todo_data)
    assert create_resp.status_code == 200
    created = create_resp.json()
    assert created["title"] == todo_data["title"]
    assert created["description"] == todo_data["description"]
    assert created["completed"] == todo_data["completed"]
    assert "id" in created

    # List todos
    list_resp = await async_client.get("/todos")
    assert list_resp.status_code == 200
    todos = list_resp.json()
    assert any(t["id"] == created["id"] for t in todos)
