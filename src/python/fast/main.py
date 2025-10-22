from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from fast.config import Settings
from fast.db import get_engine_and_sessionmaker


from mylib.main import hello

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


app = FastAPI()


@app.get("/")
async def root():
    # Return own string plus result of hello()
    own_string = "This is my own string."
    hello_result = hello()
    return {"message": f"{own_string} {hello_result}"}


# To run with uvicorn: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
