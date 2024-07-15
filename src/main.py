from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.Manager import get_user_manager
from src.auth.config import auth_backend
from src.auth.models import user
from src.auth.schemas import UserRead, UserCreate
from src.database import User, get_async_session
from src.admin.router import router as admin_router
from src.technic.router import router as technic_router

app = FastAPI(
    title="Market App",
)


@app.get("/", tags=["main"])
def get_home():
    return {"status": "success"}


# auth
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
# for admin
current_user = fastapi_users.current_user()

@app.get("/profile", tags=["main"])
async def get_profile(user_: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    query = select(user).where(user.c.id == user_.id)
    result = await session.execute(query)
    return {
        "status": 200,
        "message": "Your profile",
        "user": result.mappings().all()
    }


# admin panel
app.include_router(admin_router)


# technic
app.include_router(technic_router)