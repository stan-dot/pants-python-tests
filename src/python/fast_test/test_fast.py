import pytest
import pytest_asyncio


@pytest_asyncio.fixture
async def sample_todo(async_session):
    # Import the ORM model here to avoid circular imports
    from fast.main import TodoORM

    todo = TodoORM(
        title="Preloaded Todo", description="Inserted by fixture", completed=False
    )
    async_session.add(todo)
    await async_session.commit()
    await async_session.refresh(todo)
    return todo


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


@pytest.mark.asyncio
async def test_retrieve_preloaded_todo(async_client, sample_todo):
    # Retrieve all todos and check the preloaded one is present
    resp = await async_client.get("/todos")
    assert resp.status_code == 200
    todos = resp.json()
    assert any(
        t["id"] == sample_todo.id and t["title"] == sample_todo.title for t in todos
    )
