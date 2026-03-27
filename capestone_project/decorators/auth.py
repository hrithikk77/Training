from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from config import settings
from sqlalchemy.orm import Session
from database import get_db
from models.db_models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def require_role(required_role: str):
    def role_checker(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username: str = payload.get("sub")
            
            if username is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            
            user = db.query(User).filter(User.username == username).first()
            if not user or user.role.value != required_role:
                raise HTTPException(status_code=403, detail="Not enough permissions")
            
            return {"sub": user.username, "role": user.role.value, "id": user.id}
            
        except JWTError:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
            
    return role_checker