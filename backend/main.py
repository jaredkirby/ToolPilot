# main.py

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .routers import resume_tool_router, dos_tool_router

# Initialize FastAPI app
app = FastAPI(
    title="AI Toolset API",
    description="API for various AI tools by Jared Kirby",
    version="1.0.0",
)


# Global exception handler (optional)
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": f"An unexpected error occurred: {str(exc)}"},
    )


# Include Resume Tool router
app.include_router(
    resume_tool_router.router, prefix="/api/tool_1", tags=["Resume Tool"]
)

# Include Dos Tool router
app.include_router(dos_tool_router.router, prefix="/api/tool_2", tags=["Dos Tool"])
