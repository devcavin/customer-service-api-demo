"""Routes for account `/account`"""

from fastapi import (
    APIRouter,
    status,
    HTTPException,
    Depends,
    Query,
)
from fastapi.encoders import jsonable_encoder
from fastapi.security.oauth2 import OAuth2PasswordRequestFormStrict
from typing import Annotated

from users.models import CustomUser, AuthToken
from project.utils import get_expiry_datetime

from api.v1.utils import send_email, get_value
from api.v1.account.utils import get_user, generate_token, generate_password_reset_token

from api.v1.account.models import (
    TokenAuth,
    ResetPassword,
    UserProfile,
    EditablePersonalData,
    TransactionInfo,
    PaymentAccountDetails,
    SendMPESAPopupTo,
)
from api.v1.models import ProcessFeedback
from django.db.models import Q
import asyncio

router = APIRouter(
    prefix="/account",
    tags=["Account"],
)


@router.post("/token", name="User auth token")
async def fetch_token(
    form_data: Annotated[OAuth2PasswordRequestFormStrict, Depends()]
) -> TokenAuth:
    """
    Get user account token
    """
    try:
        user = await CustomUser.objects.aget(username=form_data.username)
        if await user.acheck_password(form_data.password):
            if user.token is None:
                user.token = generate_token()
                await user.asave()
            return TokenAuth(
                access_token=user.token,
                token_type="bearer",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password."
            )
    except CustomUser.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User does not exist.",
        )


@router.patch("/token", name="Generate new user token")
async def generate_new_token(
    user: Annotated[CustomUser, Depends(get_user)]
) -> TokenAuth:
    """Generate new token"""
    user.token = generate_token()
    await user.asave()
    return TokenAuth(access_token=user.token)


@router.get("/profile", name="Get user profile")
async def profile_information(
    user: Annotated[CustomUser, Depends(get_user)]
) -> UserProfile:
    return user.model_dump()


@router.patch("/profile", name="Update user profile")
async def update_personal_info(
    user: Annotated[CustomUser, Depends(get_user)],
    updated_personal_data: EditablePersonalData,
) -> EditablePersonalData:
    user.first_name = get_value(updated_personal_data.first_name, user.first_name)
    user.last_name = get_value(updated_personal_data.last_name, user.last_name)
    user.phone_number = get_value(updated_personal_data.phone_number, user.phone_number)
    user.email = get_value(updated_personal_data.email, user.email)
    user.address = get_value(updated_personal_data.address, user.address)
    await user.asave()
    return user.model_dump()


@router.get("/exists", name="Check if username exists")
async def check_if_username_exists(
    username: Annotated[str, Query(description="Username to check against")]
) -> ProcessFeedback:
    """Checks if account with a particular username exists
    - Useful when setting username at account creation
    """
    existance_status = (
        await CustomUser.objects.filter(username=username).afirst() is not None
    )
    return ProcessFeedback(detail=existance_status)



@router.get("/password/send-password-reset-token", name="Send password reset token")
async def reset_password(
    identity: Annotated[str, Query(description="Username or email address")]
) -> ProcessFeedback:
    """Emails password reset token to user"""
    try:
        target_user = await CustomUser.objects.filter(
            Q(username=identity) | Q(email=identity)
        ).aget()
        auth_token = await AuthToken.objects.filter(user=target_user).afirst()
        if auth_token is not None:
            auth_token.token = generate_password_reset_token()
            auth_token.expiry_datetime = get_expiry_datetime()
        else:
            auth_token = await AuthToken.objects.acreate(
                user=target_user,
                token=generate_password_reset_token(),
            )
        await auth_token.asave()
        await asyncio.to_thread(
            send_email,
            **dict(
                subject="Password Reset Token",
                recipient=auth_token.user.email,
                template_name="email/password_reset_token",
                context=dict(auth_token=auth_token),
            )
        )

    except CustomUser.DoesNotExist:
        # Let's not diclose about this for security reasons
        pass
    finally:
        return ProcessFeedback(
            detail=(
                "If an account with the provided identity exists, "
                "a password reset token has been sent to the associated email address."
            )
        )


@router.post("/password/reset", name="Set new account password")
async def reset_password(info: ResetPassword) -> ProcessFeedback:
    """Resets user account password"""
    try:
        auth_token = await AuthToken.objects.select_related("user").aget(
            token=info.token
        )
        if auth_token.is_expired():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token has expired.",
            )
        user = auth_token.user
        if user.username == info.username:
            user.set_password(info.new_password)
            user.token = generate_token()
            await user.asave()
            await auth_token.adelete()
            return ProcessFeedback(detail="Password reset successfully.")
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username"
            )

    except AuthToken.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token.",
        )
