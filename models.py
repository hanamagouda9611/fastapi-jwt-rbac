from sqlmodel import SQLModel, Field
from enum import Enum
from typing import Optional

class Role(str, Enum):
    admin = "admin"
    user = "user"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    hashed_password: str
    role: Role = Role.user

class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None

# Schemas
class UserCreate(SQLModel):
    username: str
    password: str
    role: Role = Role.user

class UserLogin(SQLModel):
    username: str
    password: str
    role: Role = Role.user
     
class Token(SQLModel):
    access_token: str
    token_type: str

class ProjectCreate(SQLModel):
    name: str
    description: Optional[str] = None

class ProjectRead(Project):
    pass

class ProjectUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
