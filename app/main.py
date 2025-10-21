# app/main.py
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.auth import hash_password
from app.auth import router as auth_router
from app.db import Base, engine
from app.errors import http_exception_handler, validation_exception_handler
from app.items import router as items_router
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.models import User

app = FastAPI(title="Study Planner API")

# создаём таблицы
Base.metadata.create_all(bind=engine)

# подключаем middleware безопасности (из P05)
app.add_middleware(SecurityHeadersMiddleware)

# глобальные обработчики ошибок
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)


@app.get("/health")
def health():
    return {"status": "ok"}


# создаём админа если нет
@app.on_event("startup")
def create_admin():
    from sqlalchemy.orm import Session

    from app.db import SessionLocal

    db: Session = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin = User(
                username="admin",
                password_hash=hash_password("admin"),
                role="admin",
            )
            db.add(admin)
            db.commit()
    finally:
        db.close()


# подключаем роутеры
app.include_router(auth_router)
app.include_router(items_router)
