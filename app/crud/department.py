from ..schemas.user import Department as DepartmentSchema
from sqlalchemy.orm import Session
from ..models.user import User  as UserModel 
from ..models.user import Department as DepartmentModel


def getDepartment(dep_id:int ,db:Session): 
    return db.query(DepartmentModel).filter(DepartmentModel.dep_id == dep_id).first()

def getAllDepartments(db:Session): 
    return db.query(DepartmentModel).all()

def addDepartment(department_input:DepartmentSchema,db:Session): 
    department = DepartmentModel(
        name = department_input.name,
        domain = department_input.domain
    )
    
    db.add(department)
    db.commit()
    db.refresh(department)
    return department

def deleteDepartment(dep_id:int,db:Session): 
    query = db.query().filter(DepartmentModel.dep_id == dep_id).first()
    department = query.first()
    if department: 
        query.delete()
        db.commit()
        db.refresh(query)
    
    return department

def getEmployeesDepartment(dep_id:int,db:Session):
    return db.query(UserModel).filter(dep_id == UserModel.dep_id).all()



