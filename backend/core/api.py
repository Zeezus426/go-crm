# api.py
from ninja import NinjaAPI, Router
from ninja.security import HttpBearer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.http import HttpRequest
from pydantic import BaseModel
from rest_framework_simplejwt.tokens import RefreshToken
from ninja.errors import HttpError

User = get_user_model()

# 1. Define the Auth Class
class GlobalAuth(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str):
        # We use the underlying DRF SimpleJWT logic to validate the token
        # sent in the "Authorization: Bearer <token>" header
        jwt_auth = JWTAuthentication()
        
        try:
            # Manually validating the token
            validated_token = jwt_auth.get_validated_token(token)
            user = jwt_auth.get_user(validated_token)
            return user
        except (InvalidToken, TokenError):
            return None

# 2. Initialize the API with this Global Auth
core_router = Router(auth=GlobalAuth())

# 3. Create a Login Endpoint (Public, no auth required)

class LoginSchema(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access: str
    refresh: str

@core_router.post("/token", response=TokenResponse, auth=None) # auth=None makes it public
def login(request, credentials: LoginSchema):
    
    # 1. Authenticate user (Standard Django Auth)
    user = User.objects.filter(username=credentials.username).first()
    
    if user and user.check_password(credentials.password):
        # 2. Generate Tokens
        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
    
    # 3. Return 401 if invalid
    raise HttpError(401, "Invalid username or password")

# 4. Create a Protected Endpoint (To test if it works)
@core_router.get("/me")
def me(request):
    return {"username": request.auth.username, "email": request.auth.email}