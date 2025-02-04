from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from backend.src.routers import AuthorizationRouter, PasswordRecoveryRouter, RegistrationRouter

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.exception_handler(RequestValidationError)
async def validationExceptionHandler(request: Request, e: RequestValidationError):
    """
    Обработчик ошибок валидации

    :param request: тело запроса
    :param e: ошибка валидации
    """
    error = e.errors()[0]
    # if "ctx" in error.keys():
    #     msg = error["ctx"]["error"]
    # elif
    # msg = str(e.errors()[0]["ctx"]["error"]) if "ctx" in e.errors()[0].keys() else e.errors()[0]["msg"]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": str(error)}),
    )

app.include_router(RegistrationRouter.router)
app.include_router(AuthorizationRouter.router)
app.include_router(PasswordRecoveryRouter.router)
