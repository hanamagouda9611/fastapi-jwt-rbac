from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from models import User, UserCreate,UserLogin, Token, Role
from database import AsyncSessionLocal
from sqlmodel.ext.asyncio.session import AsyncSession

SECRET_KEY = "WueMs8CK1BRUZn-Ct7p7Dz0NcTCbIxMTTybgGFx0y64"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter(
    tags=["auth"]
)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_token(user: User):
    data = {
        "sub": str(user.id),
        "role": user.role.value,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    async with AsyncSessionLocal() as session:
        user = await session.get(User, user_id)
        if not user:
            raise HTTPException(401, "User not found")
        return user

def require_admin(user: User = Depends(get_current_user)):
    if user.role != Role.admin:
        raise HTTPException(403, detail="Admins only")
    return user

@router.post("/register")
async def register(data: UserCreate):
    async with AsyncSessionLocal() as session:
        stmt = select(User).where(
            (User.username == data.username) &
            (User.role == data.role)
        )
        res = await session.exec(stmt)
        if res.first():
            raise HTTPException(400, detail="Username already exists with this role")

        user = User(
            username=data.username,
            hashed_password=hash_password(data.password),
            role=data.role
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

        return {
            "msg": "User created successfully",
            "user_id": user.id,
            "role": user.role.value
        }

@router.post("/login", response_model=Token)
async def login(data: UserLogin):
    async with AsyncSessionLocal() as session:

        stmt = select(User).where(
            (User.username == data.username) &
            (User.role == data.role)
        )
        res = await session.exec(stmt)
        user = res.first()

        if not user or not verify_password(data.password, user.hashed_password):
            raise HTTPException(401, detail="Invalid credentials or role")

        token = create_token(user)
        return {
            "user_id": user.id,
            "role": user.role.value,
            "access_token": token,
            "token_type": "bearer"
        }
