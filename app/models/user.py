from ..database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String, index=True)
    lastName = Column(String, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    # Department relationship
    dep_id = Column(Integer, ForeignKey("departments.dep_id"))
    department = relationship("Department", back_populates="users")

    # Task relationships - NEW
    created_tasks = relationship(
        "Task", foreign_keys="Task.created_by_id", back_populates="created_by"
    )
    assigned_tasks = relationship(
        "Task", foreign_keys="Task.assigned_user_id", back_populates="assigned_user"
    )


class Department(Base):
    __tablename__ = "departments"

    dep_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    domain = Column(String)

    users = relationship("User", back_populates="department")
    tasks = relationship(
        "Task",
        foreign_keys="Task.assigned_dep_id",
        back_populates="assigned_department",
    )
    # roles = relationship("Role", back_populates="department")


# class Role(Base):
#     __tablename__ = "roles"
#     role_id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     description = Column(String)
#     admin_rights = Column(Boolean)

#     # Department relationship (one-to-many)
#     dep_id = Column(Integer, ForeignKey("departments.dep_id"))
#     department = relationship("Department", back_populates="roles")

#     # One-to-One back to User - ADD THIS
#     user = relationship("User", back_populates="role", uselist=False)
