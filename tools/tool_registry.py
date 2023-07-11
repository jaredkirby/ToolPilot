from .dos_tool import DosTool
from .pilot_tool import PilotTool
from .instruct_tool import InstructTool
from .purpose_tool import PurposeTool
from .resume_tool import ResumeTool

TOOL_REGISTRY = {
    "Discipline of Study": DosTool(),
    "PromptPilot": PilotTool(),
    "Improve Prompt Instructions": InstructTool(),
    "Prompt Purpose": PurposeTool(),
    "Resume": ResumeTool(),
}
