from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.auth.Manager import get_user_manager
from src.auth.config import auth_backend
from src.auth.models import technic
from src.database import User, get_async_session

router = APIRouter(
    prefix="/technic",
    tags=["technic products"],
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()


@router.get("/technic_product")
async def technic_get_product(cat_id: int, user_: User = Depends(current_user),
                              session: AsyncSession = Depends(get_async_session)):
    """
        params: min-1, max-5:

            - **Computer equipment**: cat_id = 1

            - **Headphones and headset**:  cat_id = 2

            - **Computer mice**: cat_id = 3

            - **Computer keyboard**:  cat_id = 4

            - **Computer Other**:  cat_id = 5
        """
    query = select(technic).where(technic.c.cat_id == cat_id)
    result = await session.execute(query)
    if cat_id <= 5:
        return {
            "status": 200,
            "product list": result.mappings().all()
        }
    return {
        "error": "Enter the correct cat_id"
    }
