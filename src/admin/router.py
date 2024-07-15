from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.Manager import get_user_manager
from src.auth.config import auth_backend
from src.auth.models import user, technic
from src.database import User, get_async_session
from src.technic.schemas import Procreate

router = APIRouter(
    prefix="/admin",
    tags=["admin panel"],
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_superuser = fastapi_users.current_user(superuser=True)


@router.get("/get_list_admins")
async def get_users(user_: User = Depends(current_superuser), session: AsyncSession = Depends(get_async_session)):
    query = select(user).where(user.c.is_superuser == True)
    result = await session.execute(query)
    return {
        "status": 200,
        "users": result.mappings().all()
    }


@router.get("/get_list_users")
async def get_users(user_: User = Depends(current_superuser), session: AsyncSession = Depends(get_async_session)):
    query = select(user).where(user.c.is_superuser == False)
    result = await session.execute(query)
    return {
        "status": 200,
        "users": result.mappings().all()
    }


@router.get("/get_list_users/{user_id}")
async def get_user(user_id: int, user_: User = Depends(current_superuser),
                   session: AsyncSession = Depends(get_async_session)):
    query = select(user).where(user.c.id == user_id)
    result = await session.execute(query)
    return {
        "status": 200,
        "users": result.mappings().all()
    }


@router.post("/technic_add_product")
async def technic_add_product(new_product: Procreate, user_: User = Depends(current_superuser),
                              session: AsyncSession = Depends(get_async_session)):
    """
        To add entries, keep in mind that there are only 5 categories, you must enter the required category ID in the **cat_id** parameter :

        - **Computer equipment**: cat_id = 1

        - **Headphones and headset**:  cat_id = 2

        - **Computer mice**: cat_id = 3

        - **Computer keyboard**:  cat_id = 4

        - **Computer Other**:  cat_id = 5

        **Please delete the Z in the *created_at* line, if you don't delete Z, otherwise you won't create a product.**
    """
    stmt = insert(technic).values(**new_product.dict())
    await session.execute(stmt)
    await session.commit()
    return {
        "status": "200",
        "message": "The product has been successfully added",
    }
