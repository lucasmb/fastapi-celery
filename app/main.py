import time
from typing import Union

from celery import Celery
from celery.result import AsyncResult
from fastapi import Body, Depends, FastAPI, Form, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
#DB
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import settings
from app.database import create_all, get_db
from app.models import Test as TestModel

#from app.worker import create_task

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# @app.on_event("startup")
# async def startup():
#     await create_all()



# celery = Celery(__name__)

# #redis://:password@hostname:port/db_number
# celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://:eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81@redis:6379/0")
# celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://:eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81@redis:6379/0")

celery = Celery(
    __name__,
    broker="redis://redi:6379/0",
    backend="redis://redi:6379/0",
)

@app.get("/")
def home(request: Request):
    print(templates)
    return templates.TemplateResponse("home.html", context={"request": request})



@app.post("/tasks", status_code=201)
def run_task(payload = Body(...)):
    task_type = payload["type"]
    task = create_task.delay(int(task_type))
    return JSONResponse({"task_id": task.id})


@app.get("/tasks/{task_id}")
def get_status(task_id):
    task_result = AsyncResult(task_id)
    print("TASK: ")
    print(task_result)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse(result)




@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True


@app.get("/hello")
async def read_root():
    print( settings.admin_email)
    return {"Hello": "World"}

@app.get("/db")
async def test_db(request: Request, db: AsyncSession = Depends(get_db)):
    print("DB TEST:")
    results = await db.execute(select(TestModel).where(TestModel.id == 1))
    print(results)
    return results.scalars().all()



@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


