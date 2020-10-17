import datetime
import logging

from txmatching.auth.data_types import BearerTokenRequest, UserRole, TokenType, DecodedBearerToken
from txmatching.auth.exceptions import InvalidOtpException, require_auth_condition
from txmatching.auth.user.sms_service import send_sms
from txmatching.auth.user.totp import OTP_VALIDITY_MINUTES, generate_otp_for_user, verify_otp_for_user
from txmatching.database.sql_alchemy_schema import AppUserModel

logger = logging.getLogger(__name__)

OTP_RESEND_WINDOW_MULTIPLIER = 10
"""
How much time does the user have to ask for resending the OTP.
"""

JWT_OTP_EXPIRATION_MINUTES = OTP_VALIDITY_MINUTES * OTP_RESEND_WINDOW_MULTIPLIER
"""
JWT with TokenType.OTP expiration.

The OTP itself is valid for [OTP_VALIDITY_MINUTES], but we want to give user option 
to resend the OTP so we need to extend the expiration to bigger window by [OTP_RESEND_WINDOW_MULTIPLIER].
"""


def user_login_flow(user: AppUserModel, jwt_expiration_days: int) -> BearerTokenRequest:
    """
    Issues temporary JWT and sends OTP code for further verification.
    """
    require_auth_condition(user.role != UserRole.SERVICE, f'{user.role} used for user login flow!')

    if user.require_2fa:
        generate_and_send_otp(user)
        token = BearerTokenRequest(
            user_id=user.id,
            role=user.role,
            type=TokenType.OTP,
            expiration=datetime.timedelta(minutes=JWT_OTP_EXPIRATION_MINUTES)
        )
    else:
        token = BearerTokenRequest(
            user_id=user.id,
            role=user.role,
            type=TokenType.ACCESS,
            expiration=datetime.timedelta(days=jwt_expiration_days)
        )
    return token


def generate_and_send_otp(user: AppUserModel):
    """
    Generates OTP and sends it to user.
    """
    otp = generate_otp_for_user(user)
    _send_sms_otp(otp, user)


def user_otp_login(user: AppUserModel, otp: str, jwt_expiration_days: int) -> BearerTokenRequest:
    """
    Validates OTP and creates request for bearer.
    """
    require_auth_condition(user.role != UserRole.SERVICE, f'OTP login request for {user.role}.')

    if not verify_otp_for_user(user, otp):
        raise InvalidOtpException(f'OTP is not valid for the user {user.email}')

    return BearerTokenRequest(
        user_id=user.id,
        role=user.role,
        type=TokenType.ACCESS,
        expiration=datetime.timedelta(days=jwt_expiration_days)
    )


def refresh_user_token(token: DecodedBearerToken, jwt_expiration_days: int) -> BearerTokenRequest:
    """"
    Generates new JWT with extended lifespan.
    """
    require_auth_condition(token.type == TokenType.ACCESS, f'{token.type} used for token refresh!')
    require_auth_condition(token.role != UserRole.SERVICE, f'{token.role} used for token refresh!')

    return BearerTokenRequest(
        user_id=token.user_id,
        role=token.role,
        type=token.type,
        expiration=datetime.timedelta(days=jwt_expiration_days)
    )


def _send_sms_otp(otp: str, user: AppUserModel):
    require_auth_condition(user.phone_number is not None, f'No phone number for user {user.email}')
    require_auth_condition(bool(otp), 'Empty OTP!')
    send_sms(user.phone_number, message_body=f'{otp} - use this code for TXMatching login.')
