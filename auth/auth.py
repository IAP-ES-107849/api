import os
import requests
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from starlette.status import HTTP_403_FORBIDDEN
from auth.JWTBearer import JWKS, JWTBearer, JWTAuthorizationCredentials

load_dotenv()

AWS_REGION = os.environ.get("AWS_REGION")
USER_POOL_ID = os.environ.get("USER_POOL_ID")

# Get the JWKS from the Cognito User Pool
response = requests.get(
    f"https://cognito-idp.{AWS_REGION}.amazonaws.com/{USER_POOL_ID}/.well-known/jwks.json"
)

print(response.json())

# Check if 'keys' field is present in the response
if 'keys' not in response.json():
    raise ValueError("The 'keys' field is missing in the JWKS response")

jwks = JWKS.model_validate(response.json())

auth = JWTBearer(jwks)


async def get_current_user(
    credentials: JWTAuthorizationCredentials = Depends(auth),
) -> str:
    """
    Get the current user from the JWT token.

    :param credentials: JWTAuthorizationCredentials object.
    :return: Username of the user.
    """

    try:
        return credentials.claims["username"]
    except KeyError:
        HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Username missing")