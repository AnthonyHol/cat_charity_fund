from datetime import datetime
from typing import List, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def get_available_objects(
    obj_in: Union[CharityProject, Donation],
    session: AsyncSession,
) -> List[Union[CharityProject, Donation]]:
    """
    Ф-я для получения проектов, в которые можно инвестировать, и
    пожертвований, который доступны для инвестирования.
    """

    objects = await session.execute(
        select(obj_in)
        .where(obj_in.fully_invested == 0)
        .order_by(obj_in.create_date)
    )
    return objects.scalars().all()


async def close_donation_for_obj(obj_in: Union[CharityProject, Donation]):
    """Ф-я закрытия для объекта (проекта или пожертвования)."""

    obj_in.invested_amount = obj_in.full_amount
    obj_in.fully_invested = True
    obj_in.close_date = datetime.now()

    return obj_in


# async def invest_money(
#     donation: Union[CharityProject, Donation],
#     project: Union[CharityProject, Donation],
# ) -> Union[CharityProject, Donation]:
#     """Ф-я инвестирования пожертвований в проект."""

#     # остаток пожертвования
#     donation_free_amount = donation.full_amount - donation.invested_amount
#     # остаток требумой суммы в проекте
#     project_free_amount = project.full_amount - project.invested_amount

#     if donation_free_amount > project_free_amount:
#         donation.invested_amount += project_free_amount
#         await close_donation_for_obj(project)

#     elif donation_free_amount == project_free_amount:
#         await close_donation_for_obj(donation)
#         await close_donation_for_obj(project)

#     else:
#         project.invested_amount += donation_free_amount
#         await close_donation_for_obj(donation)

#     return donation, project


# async def investing_process(
#     obj_in: Union[CharityProject, Donation],
#     model_add: Union[CharityProject, Donation],
#     session: AsyncSession,
# ) -> Union[CharityProject, Donation]:
#     objects_model = await get_available_projects(obj_in, session)

#     for model in objects_model:
#         obj_in, model = await invest_money(model_add, model)
#         session.add(obj_in)
#         session.add(model)

#     await session.commit()
#     await session.refresh(obj_in)


#     return obj_in
async def close_invested_object(
    obj_to_close: Union[CharityProject, Donation],
) -> None:
    obj_to_close.fully_invested = True
    obj_to_close.close_date = datetime.now()


async def investing_process(
    object_in: Union[CharityProject, Donation], session: AsyncSession
):
    model = CharityProject if isinstance(object_in, Donation) else Donation

    not_invested_objects = await get_available_objects(model, session)
    available_amount = object_in.full_amount

    if not not_invested_objects:
        return object_in

    for not_invested_obj in not_invested_objects:
        need_to_invest = (
            not_invested_obj.full_amount - not_invested_obj.invested_amount
        )
        to_invest = (
            need_to_invest
            if need_to_invest < available_amount
            else available_amount
        )
        not_invested_obj.invested_amount += to_invest
        object_in.invested_amount += to_invest
        available_amount -= to_invest

        if not_invested_obj.full_amount == not_invested_obj.invested_amount:
            await close_invested_object(not_invested_obj)

        if not available_amount:
            await close_invested_object(object_in)
            break

    await session.commit()

    return object_in
