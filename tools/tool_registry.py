import streamlit as st

from .dos_tool import DosTool
from .pilot_tool import PilotTool
from .instruct_tool import InstructTool
from .purpose_tool import PurposeTool
from .resume_tool import ResumeTool
from .research_tool import ResearchAgentTool
from .shopper_tool import ShopperTool
from .hiring_tool import HiringTool


metaphor_api_key = st.secrets["METAPHOR_API_KEY"]

TOOL_REGISTRY = {
    "Discipline of Study": DosTool(),
    "PromptPilot": PilotTool(),
    "Improve Prompt Instructions": InstructTool(),
    "Prompt Purpose": PurposeTool(),
    "Resume": ResumeTool(),
    # "Research Agent": ResearchAgentTool(metaphor_api_key),
    "Shopper": ShopperTool(),
    # "Hiring": HiringTool(),
}
