from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


def error_response(
    code: str, message: str, status_code: int, details: dict | None = None
):
    return JSONResponse(
        status_code=status_code,
        content={
            "code": code,
            "message": message,
            "details": details or {},
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return error_response(
        code="VALIDATION_ERROR",
        message="Invalid request data",
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        details={"errors": exc.errors()},
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    # detail может быть dict (мы так делаем) или строкой
    if isinstance(exc.detail, dict):
        body = exc.detail
        # гарантируем поля
        if "code" not in body:
            body["code"] = "HTTP_ERROR"
        if "message" not in body:
            body["message"] = str(
                body.get("message") or body.get("detail") or "HTTP error"
            )
        if "details" not in body:
            body["details"] = {}
        return JSONResponse(status_code=exc.status_code, content=body)
    return error_response(
        code="HTTP_ERROR",
        message=str(exc.detail),
        status_code=exc.status_code,
    )
