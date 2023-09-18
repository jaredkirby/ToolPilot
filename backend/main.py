# main.py

from fastapi import FastAPI
from .routers import resume_tool_router, dos_tool_router  # Import routers

app = FastAPI()

# Include routers
app.include_router(
    resume_tool_router.router, prefix="/api/tool_1", tags=["Resume Tool"]
)
app.include_router(dos_tool_router.router, prefix="/api/tool_2", tags=["Dos Tool"])
