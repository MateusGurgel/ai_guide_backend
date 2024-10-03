from fastapi import FastAPI
from modules.study_plan.study_plan_services import StudyPlanServices

app = FastAPI()

@app.post("/search")
def read_root(user_message: str):
    books = StudyPlanServices.get_study_plan(user_message)

    return {"response": books}