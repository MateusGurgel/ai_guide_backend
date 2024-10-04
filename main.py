from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from modules.study_plan.study_plan_services import StudyPlanServices

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


class Item(BaseModel):
    topic: str
@app.post("/search")
def read_root(request: Item):
    books = StudyPlanServices.get_study_plan(request.topic)

    return {"response": books}