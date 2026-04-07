from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio.session import AsyncSession
from backend.app.core.db import get_session
from backend.app.core.logging import get_logger
from backend.app.auth.schema import UserCreateSchema, UserReadSchema
from backend.app.api.services.user_auth import user_auth_service

logger = get_logger()

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register", response_model=UserReadSchema, status_code=status.HTTP_201_CREATED
)
async def register_user(
    user_data: UserCreateSchema,
    session: AsyncSession = Depends(get_session),
):
    try:
        if await user_auth_service.check_user_email_exists(user_data.email, session):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exist",
            )

        if await user_auth_service.check_user_id_no_exists(user_data.id_no, session):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this ID number already exist",
            )
        new_user = await user_auth_service.create_user(user_data, session)
        logger.info(
            f"New User {new_user.email} registered successfully, awaiting activation"
        )
        return new_user
    except HTTPException as http_ex:
        await session.rollback()
        raise http_ex

    except Exception as e:
        await session.rollback()
        logger.error(f"Error to register user {user_data.email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
