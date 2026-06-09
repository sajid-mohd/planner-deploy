from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from fastapi import HTTPException
import httpx
from sqlalchemy.orm import Session
from ..config import settings
from ..users import services as user_services, schemas
import secrets

# OAuth setup
oauth = OAuth()

oauth.register(
    name="google",
    server_metadata_url=settings.GOOGLE_CONF_URL,
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid email profile",
        "prompt": "select_account",
    },
    authorize_params={
        "access_type": "offline"
    }
)


async def google_oauth_init(request: Request):
    try:
        base_url = str(request.base_url).rstrip("/")

        # Railway callback URL
        redirect_uri = f"{base_url}/api/auth/callback"

        print("=" * 50)
        print("GOOGLE LOGIN INIT")
        print(f"Base URL: {base_url}")
        print(f"Redirect URI: {redirect_uri}")
        print("=" * 50)

        return await oauth.google.authorize_redirect(
            request,
            redirect_uri,
            access_type="offline"
        )

    except Exception as e:
        print(f"Error in google_oauth_init: {e}")
        raise


async def get_google_oauth_token(request: Request):
    try:
        print("=" * 50)
        print("GOOGLE CALLBACK RECEIVED")
        print(f"Request URL: {request.url}")
        print("=" * 50)

        token = await oauth.google.authorize_access_token(request)

        if not token:
            raise HTTPException(
                status_code=400,
                detail="No token received from Google"
            )

        print(f"Token keys: {list(token.keys())}")

        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={
                    "Authorization": f"Bearer {token['access_token']}"
                }
            )

            if response.status_code != 200:
                print("Failed to fetch Google user info")
                print(response.text)

                raise HTTPException(
                    status_code=400,
                    detail="Failed to get user info from Google"
                )

            user_info = response.json()

            print("Google User:")
            print(user_info)

            if "email" not in user_info:
                raise HTTPException(
                    status_code=400,
                    detail="Email not provided by Google"
                )

            return user_info

    except Exception as e:
        print("GOOGLE AUTH ERROR")
        print(str(e))

        raise HTTPException(
            status_code=400,
            detail=f"Authentication failed: {str(e)}"
        )


ALLOWED_EMAILS = {
    "mdsajid2152@gmail.com",
    "awadtheman2@gmail.com",
    "khatoonkhamira23@gmail.com",
    "mdsajid84388@gmail.com"
}


async def get_or_create_user_from_google(
    db: Session,
    google_user: dict
):
    email = google_user.get("email")

    if not email:
        raise HTTPException(
            status_code=400,
            detail="Invalid Google user data"
        )

    if email not in ALLOWED_EMAILS:
        raise HTTPException(
            status_code=403,
            detail="Access restricted. This app is private."
        )

    user = user_services.get_user_by_email(
        db,
        email=email
    )

    if not user:
        # bcrypt-safe password length
        random_pass = secrets.token_urlsafe(32)[:32]

        username = email.split("@")[0]

        user_create = schemas.UserCreate(
            email=email,
            password=random_pass,
            username=username
        )

        user = user_services.create_user(
            db=db,
            user=user_create
        )

    return user
