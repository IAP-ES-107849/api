from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from db.create_database import create_tables
from db.database import SessionLocal

from routers import task


@asynccontextmanager
async def lifespan(app):
    create_tables()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Todo List API",
    version="0.0.1",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "TodoList",
    },
    servers=[{"url": "http://localhost:8001", "description": "Local server"}],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task.router)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response