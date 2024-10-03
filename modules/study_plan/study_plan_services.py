from modules.study_plan.study_plan_writer.study_plan_writer_services import StudyPlanWritter
from openai_client import openai_client
class StudyPlanServices():

  @staticmethod
  def get_study_plan(study_plan: str) -> str:
    study_plan_writer = StudyPlanWritter(openai_client)
    return study_plan_writer.generate_study_plan(study_plan)