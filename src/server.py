import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from core import analyze_procrastination, handle_procrastination
from api_models import create_model

app = FastAPI(title="ProctorAI API")

# Global variable to track if AI models are available
AI_MODELS_AVAILABLE = True
try:
    from api_models import create_model
except ImportError:
    AI_MODELS_AVAILABLE = False

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "ai_models": "available" if AI_MODELS_AVAILABLE else "unavailable"
    }

@app.post("/analyze")
async def analyze_screenshot(
    screenshot: UploadFile = File(...),
    prompt: str = Form(...),
    model_name: str = Form("claude-3-5-sonnet-20240620"),
    two_tier: bool = Form(False),
    router_model_name: str = Form("llava")
):
    if not AI_MODELS_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="AI models are not available. Please install required packages."
        )
    # Save the uploaded screenshot
    os.makedirs("screenshots", exist_ok=True)
    screenshot_path = os.path.join("screenshots", screenshot.filename)
    with open(screenshot_path, "wb") as buffer:
        content = await screenshot.read()
        buffer.write(content)
    
    # Analyze the screenshot
    determination, _ = analyze_procrastination(
        prompt,
        model_name=model_name,
        two_tier=two_tier,
        router_model_name=router_model_name
    )
    
    return {
        "result": "procrastinating" if "procrastinating" in determination.lower() else "not procrastinating",
        "determination": determination
    }

@app.post("/handle-procrastination")
async def trigger_procrastination_event(
    user_spec: str = Form(...),
    user_name: str = Form("Procrastinator"),
    model_name: str = Form("claude-3-5-sonnet-20240620"),
    tts: bool = Form(False),
    voice: str = Form("Patrick"),
    countdown_time: int = Form(15)
):
    if not AI_MODELS_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="AI models are not available. Please install required packages."
        )
    proctor_model = create_model(model_name)
    determination, image_filepaths = analyze_procrastination(user_spec, model_name)
    
    if "procrastinating" in determination.lower():
        handle_procrastination(
            user_spec,
            user_name,
            proctor_model,
            tts,
            voice,
            countdown_time,
            image_filepaths
        )
        return {"status": "Procrastination event triggered"}
    
    return {"status": "Not procrastinating"}

import asyncio
from concurrent.futures import ThreadPoolExecutor

def run_server(host="127.0.0.1", port=8000):
    """Run the FastAPI server"""
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    run_server()
