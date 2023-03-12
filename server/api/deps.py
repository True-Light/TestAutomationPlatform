import uuid
import crud
import models
import schemas

from typing import Generator

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    SecurityScopes,
)
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from core.config import settings
from core.logger import logger_server
from db.session import get_db, connect_db

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token",
)


def get_uuid():
    return str(uuid.uuid4())


def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db),
) -> models.User:
    # logger.info(token)
    # logger.info(db)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        # logger.info(payload)
        # {'exp': 1667215955, 'sub': 'admin'}
        user_id: str = payload.get("sub")
        if not user_id:
            raise credentials_exception
    except (JWTError, ValidationError):
        raise credentials_exception
    user = crud.user.get(db, id=user_id)
    if not user:
        raise credentials_exception
    return user


def get_current_active_user(
        current_user: models.User = Security(get_current_user),
) -> models.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
