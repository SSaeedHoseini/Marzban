import logging

from apscheduler.schedulers.background import BackgroundScheduler
from config import DOCS
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_responses import custom_openapi

app = FastAPI(
    docs_url='/docs' if DOCS else None,
    redoc_url='/redoc' if DOCS else None
)
app.openapi = custom_openapi(app)
scheduler = BackgroundScheduler({'apscheduler.job_defaults.max_instances': 5})
logger = logging.getLogger('uvicorn.error')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from app import dashboard, jobs, views  # noqa


@app.on_event("startup")
def startup():
    scheduler.start()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = {}
    for error in exc.errors():
        details[error["loc"][1]] = error["msg"]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": details}),
    )