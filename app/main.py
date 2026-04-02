from .database import engine, Base,SessionLocal
from .models.user import User as UserModel
from  .models.user import Department as DepartmentModel
from fastapi import FastAPI, APIRouter, Depends
from contextlib import asynccontextmanager
from .router.users import user_router
from .router.departments import department_router
from .router.tasks import task_router
from .router.auth_router import router as public_router
from .auth.jwt import get_current_active_user,hash_password


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # 2. Seed the Admin User
    # Use SessionLocal() directly here, NOT get_db()
    db = SessionLocal() 
    try:
        dept_name = "Management"
        dept = db.query(DepartmentModel).filter(DepartmentModel.name == dept_name).first()
        
        if not dept:
            print(f"Creating department: {dept_name}")
            dept = DepartmentModel(name=dept_name)
            db.add(dept)
            db.commit()
            db.refresh(dept)
        admin_exists = db.query(UserModel).filter(UserModel.username == "admin").first()
        if not admin_exists:
            print("Creating default admin user...")
            # Note: Ensure your UserModel has a password hashing logic 
            # or hash it here before saving!
            new_admin = UserModel(
                username="admin",
                password=hash_password("admin"), 
                firstName="System",
                lastName="Admin",
                dep_id=dept.dep_id
            )
            db.add(new_admin)
            db.commit()
    except Exception as e:
        print(f"Error seeding admin: {e}")
        db.rollback()
    finally:
        db.close()

    yield  # CRITICAL: This allows the app to start
app = FastAPI(lifespan=lifespan)
api_private_router = APIRouter(
    prefix="/api", tags=["Private"], dependencies=[Depends(get_current_active_user)]
)

api_private_router.include_router(user_router)
api_private_router.include_router(department_router)
api_private_router.include_router(task_router)

app.include_router(public_router)
app.include_router(api_private_router)


@app.get("/health")
def health_check():
    return {"status": "Running"}
