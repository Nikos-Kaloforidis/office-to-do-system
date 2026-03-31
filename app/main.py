from .database import engine, Base, get_db
from fastapi import FastAPI   
from contextlib import asynccontextmanager
from .router.users import user_router 
from .router.departments import department_router
from .router.tasks import task_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    #Initialize DB
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(department_router)
app.include_router(task_router)

@app.get("/health")
def health_check(): 
    return {"status": "Running"}

