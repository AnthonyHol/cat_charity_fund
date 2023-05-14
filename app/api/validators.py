from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject, Donation, User


async def check_name_duplicate(
    room_name: str,
    session: AsyncSession,
) -> None:
    room_id = await charity_project_crud.get_charity_project_by_id(
        room_name, session
    )

    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession,
):
    project = await charity_project_crud.get_charity_project_by_id(
        project_id, session
    )
    if project is None:
        raise HTTPException(status_code=404, detail='Проект не найден!')
    return project
