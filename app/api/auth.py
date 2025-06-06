# app/api/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.application.schemas.user_dto import UserCreateDTO, UserResponse, UserUpdateDTO
from app.application.services.user_service import UserService
from app.infrastructure.database import get_db
from sqlalchemy.orm import Session
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

# -- 1) Dependency pour extraire et valider le token --
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.APP_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = UserService(db).get_user_by_email(email)
    if not user:
        raise credentials_exception

    # On transforme l'entité en schéma de sortie
    return UserResponse.model_validate(user)

# -- 2) Login / Token --
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now() + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.APP_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = UserService(db).authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=UserResponse, status_code=201)
def register_user(user_data: UserCreateDTO, db: Session = Depends(get_db)):
    user_service = UserService(db)
    try:
        user_data.role = "user"  # Default role for new users
        user = user_service.create_user(user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return user

# -- 4) Nouvel endpoint /me --
@router.get("/me", response_model=UserResponse)
async def read_current_user(current_user: UserResponse = Depends(get_current_user)):
    return current_user

@router.put("/edit", response_model=UserResponse)
async def edit_current_user(
    update_data: UserUpdateDTO,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    user_service = UserService(db)
    updated_user = user_service.update_user(current_user.id, update_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

# -- 5) Endpoint pour supprimer un user --
@router.delete("/remove", status_code=204)
async def remove_current_user(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    user_service = UserService(db)
    user_service.delete_user(current_user.id)
    return None
