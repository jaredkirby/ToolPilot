from ..prompt.dos_tool import DosTool
from ..prompt.pilot_tool import PilotTool
from ..prompt.instruct_tool import InstructTool
from ..prompt.purpose_tool import PurposeTool

from ..stats.exam_tool import StatsExamTool
from ..stats.explain_tool import StatsExplainTool

from ..work.resume_tool import ResumeTool

TOOL_REGISTRY = {
    "Prompts": {
        "Discipline of Study": DosTool(),
        "PromptPilot": PilotTool(),
        "Improve Prompt Instructions": InstructTool(),
        "Prompt Purpose": PurposeTool(),
        "Resume": ResumeTool(),
    },
    "Stats": {
        "Answer an Exam Question": StatsExamTool(),
        "Explain a Concept or Term": StatsExplainTool(),
    },
}
