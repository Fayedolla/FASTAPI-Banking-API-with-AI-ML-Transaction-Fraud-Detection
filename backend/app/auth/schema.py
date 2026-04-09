from enum import Enum
from sqlmodel import SQLModel, Field
from sqlalchemy import BigInteger
from pydantic import EmailStr, field_validator
from fastapi import HTTPException, status
import uuid


class SecurityQuestionSchema(str, Enum):
    MOTHER_MAIDEN_NAME = "mother_maiden_name"
    CHILDHOOD_FRIEND = "childhood_friend"
    FAVORITE_COLOR = "favorite_color"
    BIRTH_CITY = "birth_city"

    @classmethod
    def get_description(cls, value: "SecurityQuestionSchema") -> str:
        description = {
            cls.MOTHER_MAIDEN_NAME: "What is the name of your mother?",
            cls.CHILDHOOD_FRIEND: "What is the name of your childhood friend?",
            cls.FAVORITE_COLOR: "What is your favorite color?",
            cls.BIRTH_CITY: "What is the name of the city you were born in?",
        }
        return description.get(value, "Unknown security question")


class AccountStatusSchema(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    LOCKED = "locked"
    PENDING = "pending"


class RoleChoicesSchema(str, Enum):
    CUSTOMER = "customer"
    ACCOUNT_EXECUTIVE = "account_executive"
    BRANCH_MANAGER = "branch_manager"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"
    TELLER = "teller"


class BaseUserSchema(SQLModel):
    username: str | None = Field(default=None, max_length=12, unique=True)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    first_name: str = Field(max_length=30)
    middle_name: str | None = Field(max_length=30, default=None)  # ✅ str | None
    last_name: str = Field(max_length=30)
    id_no: int = Field(unique=True, gt=0, sa_type=BigInteger)
    is_active: bool = False
    is_superuser: bool = False
    security_question: SecurityQuestionSchema = Field(
        default=SecurityQuestionSchema.MOTHER_MAIDEN_NAME  # ✅ no max_length on Enum
    )
    security_answer: str = Field(max_length=30)
    account_status: AccountStatusSchema = Field(default=AccountStatusSchema.INACTIVE)
    role: RoleChoicesSchema = Field(default=RoleChoicesSchema.CUSTOMER)


class UserCreateSchema(BaseUserSchema):
    password: str = Field(min_length=8, max_length=40)
    confirm_password: str = Field(min_length=8, max_length=40)

    @field_validator("confirm_password")
    @classmethod
    def validate_confirm_password(cls, v, info):  # ✅ use info, not values
        if "password" in info.data and v != info.data["password"]:
            raise ValueError(
                "Passwords do not match"
            )  # ✅ ValueError not HTTPException
        return v


class UserReadSchema(BaseUserSchema):
    id: uuid.UUID
    full_name: str


class EmailRequestSchema(SQLModel):
    email: EmailStr


class LoginRequestSchema(SQLModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=40,
    )


class OTPVerifyRequestSchema(SQLModel):
    email: EmailStr
    otp: str = Field(
        min_length=6,
        max_length=6,
    )


class PasswordResetRequestSchema(SQLModel):
    email: EmailStr


class PasswordResetConfirmSchema(SQLModel):
    new_password: str = Field(..., min_length=8, max_length=40)

    confirm_password: str = Field(
        ...,
        min_length=8,
        max_length=40,
    )

    @field_validator("confirm_password")
    def validate_password_match(cls, v, values):
        if "new_password" in values.data and v != values.data["new_password"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "status": "error",
                    "message": "Passwords do not match",
                    "action": "Please ensure that the passwords you entered match",
                },
            )
        return v


class TOTPSetupRequestSchema(SQLModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=40)


class TOTPEnableRequestSchema(SQLModel):
    email: EmailStr
    otp: str = Field(min_length=6, max_length=6)


class LoginTOTPRequestSchema(SQLModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=40)
    totp_code: str = Field(min_length=6, max_length=6)


class TOTPSetupResponseSchema(SQLModel):
    secret: str
    provisioning_uri: str  # Changed from qr_code_url
