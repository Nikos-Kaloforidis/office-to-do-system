from .database import engine, Base, get_db
from fastapi import FastAPI   ,APIRouter,Depends
from contextlib import asynccontextmanager
from .router.users import user_router 
from .router.departments import department_router
from .router.tasks import task_router
from .router.auth_router import router as public_router
from .auth.jwt import get_current_active_user
@asynccontextmanager
async def lifespan(app: FastAPI):
    #Initialize DB
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)
api_private_router = APIRouter(prefix="/api",tags=["Private"],dependencies=[Depends(get_current_active_user)])

api_private_router.include_router(user_router)
api_private_router.include_router(department_router)
api_private_router.include_router(task_router)

app.include_router(public_router)
app.include_router(api_private_router)

@app.get("/health")
def health_check(): 
    return {"status": "Running"}

