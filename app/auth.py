from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from app.database import engine
from app.models import User, UserRole
from app.settings import SECRET_KEY

# Load environment variables
config = Config(".env")
oauth = OAuth(config)

# Security configurations
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate password hash."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Get current user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        user = session.exec(statement).first()
        if user is None:
            raise credentials_exception
        return user

def check_admin_access(current_user: User = Depends(get_current_user)) -> User:
    """Check if user has admin access."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can perform this action"
        )
    return current_user

def check_teacher_access(current_user: User = Depends(get_current_user)) -> User:
    """Check if user has teacher access."""
    if current_user.role not in [UserRole.ADMIN, UserRole.TEACHER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only teachers and administrators can perform this action"
        )
    return current_user

async def get_oauth_user(provider: str, token: dict) -> Optional[User]:
    """Get or create user from OAuth provider."""
    with Session(engine) as session:
        if provider == "google":
            email = token.get("email")
            statement = select(User).where(User.email == email)
            user = session.exec(statement).first()
            
            if not user:
                # Create new user
                user = User(
                    email=email,
                    username=token.get("name", email),
                    hashed_password="",  # OAuth users don't need password
                    role=UserRole.STUDENT,  # Default role, can be changed by admin
                    oauth_provider=provider,
                    oauth_id=token.get("sub")
                )
                session.add(user)
                session.commit()
                session.refresh(user)
            
            return user
    return None 