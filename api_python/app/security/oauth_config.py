from authlib.integrations.starlette_client import OAuth
from fastapi.security import OAuth2PasswordBearer

from api_python.resources.credentials import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, SECRET_KEY

oauth = OAuth()
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    },
    authorize_state=SECRET_KEY
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
