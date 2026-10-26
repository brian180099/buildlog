from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)
    nickname: str = Field(min_length=2, max_length=20)

    @field_validator("email", mode="before")
    @classmethod
    def trim_email(cls, value: str) -> str:
        return value.strip().lower()

    @field_validator("nickname", mode="before")
    @classmethod
    def trim_nickname(cls, value: str) -> str:
        return value.strip()

    @field_validator("nickname")
    @classmethod
    def validate_nickname(cls, value: str) -> str:
        if not value or not all(character.isalnum() or character == "_" for character in value):
            raise ValueError("닉네임에는 한글, 영문, 숫자와 밑줄만 사용할 수 있습니다.")
        return value


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=64)

    @field_validator("email", mode="before")
    @classmethod
    def trim_email(cls, value: str) -> str:
        return value.strip().lower()


class NicknameUpdateRequest(BaseModel):
    nickname: str = Field(min_length=2, max_length=20)

    @field_validator("nickname", mode="before")
    @classmethod
    def trim_nickname(cls, value: str) -> str:
        return value.strip()

    @field_validator("nickname")
    @classmethod
    def validate_nickname(cls, value: str) -> str:
        if not value or not all(character.isalnum() or character == "_" for character in value):
            raise ValueError("닉네임에는 한글, 영문, 숫자와 밑줄만 사용할 수 있습니다.")
        return value


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    nickname: str


class AuthResponse(BaseModel):
    data: UserResponse


class MessageResponse(BaseModel):
    data: dict[str, str]

