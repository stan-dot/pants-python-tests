from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, RedirectResponse
from mylib.main import hello
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Boolean, Column, Integer, String, Text, select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

from fast.config import Settings
from fast.db import Base, get_engine_and_sessionmaker
from fast.dependencies import get_session

engine: AsyncEngine | None = None
AsyncSessionLocal: sessionmaker | None = None

settings: Settings | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global settings
    settings = Settings()

    assert settings is not None, "Settings must be initialized"

    engine, sessionmaker = get_engine_and_sessionmaker(settings)
    app.state.engine = engine
    app.state.sessionmaker = sessionmaker
    app.state.settings = settings

    yield

    await engine.dispose()


class TodoORM(Base):
    __tablename__ = "todo"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, default="")
    completed = Column(Boolean, default=False, nullable=False)


class Todo(BaseModel):
    title: str
    description: str = ""
    completed: bool = False


class TodoOut(Todo):
    id: int

    model_config = ConfigDict(from_attributes=True)


TODO_NOT_FOUND = "Todo not found"

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    # Return own string plus result of hello()
    own_string = "This is my own string."
    hello_result = hello()
    return {"message": f"{own_string} {hello_result}"}


# Endpoint: Get all todos
@app.get("/todos", response_model=list[TodoOut])
async def get_todos(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(TodoORM))
    todos = result.scalars().all()
    return [TodoOut.model_validate(todo) for todo in todos]


# Endpoint: Create a new todo
@app.post("/todos", response_model=TodoOut)
async def create_todo(todo: Todo, session: AsyncSession = Depends(get_session)):
    todo_obj = TodoORM(**todo.model_dump())
    session.add(todo_obj)
    await session.commit()
    await session.refresh(todo_obj)
    return TodoOut.model_validate(todo_obj)


# To run with uvicorn: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
