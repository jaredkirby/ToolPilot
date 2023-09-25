# routers/dos_tool_router.py

from fastapi import APIRouter
from pydantic import BaseModel, Field
from ..api_tools.dos_tool import DosTool
from ..utils.chat import create_chat


router = APIRouter()


class DosInput(BaseModel):
    topic: str = Field(..., description="The topic for which discipline is needed")
    temperature: float = Field(..., description="Model temperature")


@router.post("/dos-execute")
async def execute_dos_tool(input: DosInput):
    # Create an instance of DosTool
    dos_tool = DosTool()

    # Update the temperature if needed (Optional)
    dos_tool.temperature = input.temperature
    dos_tool.chat = create_chat(input.temperature, dos_tool.model)

    # Execute the tool
    result = dos_tool.execute(topic=input.topic)  # Explicitly pass 'topic'

    return {"result": result}
