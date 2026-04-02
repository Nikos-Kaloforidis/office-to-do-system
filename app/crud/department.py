from sqlalchemy.orm import Session
from sqlalchemy import delete
from ..schemas.department import DepartmentCreate
from ..models.user import User as UserModel
from ..models.user import Department as DepartmentModel  # Fixed import


def getDepartment(dep_id: int, db: Session):
    return db.query(DepartmentModel).filter(DepartmentModel.dep_id == dep_id).first()


def getAllDepartments(db: Session):
    return db.query(DepartmentModel).all()


def addDepartment(department_input: DepartmentCreate, db: Session):
    department = DepartmentModel(
        name=department_input.name, domain=department_input.domain
    )
    db.add(department)
    db.commit()
    db.refresh(department)
    return department


def deleteDepartment(dep_id: int, db: Session):
    department = (
        db.query(DepartmentModel).filter(DepartmentModel.dep_id == dep_id).first()
    )
    if department:
        db.delete(department)
        db.commit()
        return True
    return False


def getEmployeesDepartment(dep_id: int, db: Session):
    return db.query(UserModel).filter(UserModel.dep_id == dep_id).all()
