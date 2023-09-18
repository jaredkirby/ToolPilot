# routers/resume_tool_router.py

from fastapi import APIRouter
from pydantic import BaseModel
from ..tools.resume_tool import ResumeTool  # Import your tool logic

router = APIRouter()


class ResumeInput(BaseModel):
    job_description: str
    resume: str
    temperature: float = 0.75


@router.post("/execute")
async def execute_resume_tool(input: ResumeInput):
    resume_tool = ResumeTool()  # Instantiate your ResumeTool class
    result = resume_tool.execute(input.job_description, input.resume, input.temperature)
    return {"result": result}
