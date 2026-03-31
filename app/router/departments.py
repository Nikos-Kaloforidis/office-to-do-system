from fastapi import APIRouter,status,Response,Depends
from sqlalchemy.orm import Session
from ..crud.department import deleteDepartment,getAllDepartments,getDepartment,addDepartment ,getEmployeesDepartment
from ..schemas.user import Department as DepartmentSchema
from ..database import get_db

department_router = APIRouter(
    prefix="/department",
    tags=["Department"],
    responses= {404: {"description": "Not found"}},
)

@department_router.get("/show/all")
def showAllDepartments(db_instance:Session=Depends(get_db)): 
    response = getAllDepartments(db=db_instance)
    dep_list  = [dep.name for dep in response]
    department_str = ", ".join(dep_list)
    if response: 
        return Response(status_code=status.HTTP_200_OK,content=f"Departments: {department_str}",media_type="text/plain")
    return Response(status_code=status.HTTP_204_NO_CONTENT,content=f"There are no departments in the system",media_type="text/plain") 

@department_router.get("/show/{id}")
def showDepartment(id:int,db_instance:Session=Depends(get_db)): 
    department  = getDepartment(dep_id=id,db=db_instance)

    if department:
        return Response(status_code=status.HTTP_200_OK,content=f"Current departments: {department.name}")
    return Response(status_code=status.HTTP_404_NOT_FOUND,content=f"No department with {department.name} found",  media_type="text/plain")


@department_router.post("/add")
def createDepartment(department_new: DepartmentSchema , db_instance:Session=Depends(get_db)): 
    new_dep  = addDepartment(department_input=department_new,db=db_instance)

    if new_dep: 
        return Response(status_code=status.HTTP_201_CREATED,content = "Department Created Successfully")
    return Response(status_code=status.HTTP_404_NOT_FOUND,content ="Could not create department")

@department_router.delete("/remove")
def removeDepartment(id:int , db_instance:Session=Depends(get_db)): 
    deleteDepartment(dep_id = id , db= db_instance)

@department_router.get("/all_users")
def getAllUsersFromDepartment(id:int,db_instance:Session=Depends(get_db)):
    response = getEmployeesDepartment(id,db_instance)
    employee_list = [f'{emp.firstName} {emp.lastName}' for emp in response]
    employee_str = ", ".join(employee_list)

    if  not employee_list: 
        return Response(status_code=status.HTTP_204_NO_CONTENT,content="This Department has no people yet")
    return Response(status_code=status.HTTP_200_OK,content= f"Employee List : {employee_str}")

