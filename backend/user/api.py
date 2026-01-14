from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from ninja import Router
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from rest_framework_simplejwt.tokens import RefreshToken

auth_router = Router()

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=150)
    email: EmailStr
    password1: str = Field(..., min_length=8)
    password2: str

class UpdateUserRequest(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_staff: bool
    first_name: str = ""
    last_name: str = ""

class AuthResponse(BaseModel):
    access: str
    refresh: str
    user: UserResponse

@auth_router.post("/login/", response=AuthResponse, auth=None)
def login(request, credentials: LoginRequest):
    user = authenticate(username=credentials.username, password=credentials.password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_staff': user.is_staff,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        }
    else:
        return {'error': 'Invalid credentials'}, 401

@auth_router.post("/register/", response=AuthResponse, auth=None)
def register(request, data: RegisterRequest):
    if data.password1 != data.password2:
        return {'error': 'Passwords do not match'}, 400

    if User.objects.filter(username=data.username).exists():
        return {'error': 'Username already exists'}, 400

    if User.objects.filter(email=data.email).exists():
        return {'error': 'Email already exists'}, 400

    user = User.objects.create_user(
        username=data.username,
        email=data.email,
        password=data.password1
    )
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
    }

@auth_router.post("/logout/", auth=None)
def logout(request, data: dict = None):
    if data and 'refresh' in data:
        try:
            token = RefreshToken(data['refresh'])
            token.blacklist()
        except Exception:
            pass
    return {'detail': 'Successfully logged out'}

@auth_router.get("/user/", response=UserResponse)
def get_user(request):
    user = request.auth
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_staff': user.is_staff,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }

@auth_router.patch("/user/", response=UserResponse)
def update_user(request, data: UpdateUserRequest):
    user = request.auth

    if data.username is not None:
        user.username = data.username
    if data.email is not None:
        user.email = data.email
    if data.first_name is not None:
        user.first_name = data.first_name
    if data.last_name is not None:
        user.last_name = data.last_name

    user.save()

    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_staff': user.is_staff,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }

