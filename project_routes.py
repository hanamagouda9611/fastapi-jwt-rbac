from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from models import Project, ProjectCreate, ProjectRead, ProjectUpdate, User
from database import AsyncSessionLocal
from auth import get_current_user, require_admin

router = APIRouter(
    tags=["projects"],
    prefix="/projects"
)

@router.get("/", response_model=dict)
async def list_projects(user: User = Depends(get_current_user)):
    async with AsyncSessionLocal() as session:
        result = await session.exec(select(Project))
        projects = result.all()
        return {"message": "Project list retrieved successfully", "projects": projects}


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_project(
    data: ProjectCreate,
    user: User = Depends(require_admin)
):
    project = Project(**data.model_dump())
    async with AsyncSessionLocal() as session:
        session.add(project)
        await session.commit()
        await session.refresh(project)
        return {
            "message": "Project created successfully",
            "project": project
        }


@router.put("/{project_id}", response_model=dict)
async def update_project(
    project_id: int,
    data: ProjectUpdate,
    user: User = Depends(require_admin)
):
    async with AsyncSessionLocal() as session:
        project = await session.get(Project, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        for field_name, field_value in data.model_dump(exclude_unset=True).items():
            setattr(project, field_name, field_value)

        await session.commit()
        await session.refresh(project)
        return {
            "message": "Project updated successfully",
            "project": project
        }


@router.delete("/{project_id}", response_model=dict)
async def delete_project(
    project_id: int,
    user: User = Depends(require_admin)
):
    async with AsyncSessionLocal() as session:
        project = await session.get(Project, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        await session.delete(project)
        await session.commit()
        return {"message": "Project deleted successfully"}
