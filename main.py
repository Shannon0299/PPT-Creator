import os
import io
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager

import google.generativeai as genai

from .ai_generator import generate_slide_content
from .ppt_builder import create_presentation

# --- Configuration & App State ---

# We'll use a dictionary to hold our "global" state, like the AI model
# This is populated during the 'startup' lifespan event
app_state = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    print("Starting up...")
    # Load API Key from environment variable
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Warning: GEMINI_API_KEY environment variable not set.")
        # You could raise an error here to stop startup if the key is required
        # raise ValueError("GEMINI_API_KEY is not set!")
    
    # Configure the Gemini client
    genai.configure(api_key=api_key)
    
    # Initialize the model and store it in app_state
    try:
        app_state["gemini_model"] = genai.GenerativeModel('gemini-2.5-flash-preview-09-2025')
        print("Gemini model loaded successfully.")
    except Exception as e:
        print(f"Error loading Gemini model: {e}")
        app_state["gemini_model"] = None
        
    yield
    
    # --- Shutdown ---
    print("Shutting down...")
    app_state.clear()


app = FastAPI(
    title="AI Content Generator API",
    description="Generates PowerPoint presentations from a topic.",
    lifespan=lifespan
)

# --- API Models ---

class PptRequest(BaseModel):
    """The request body for generating a PPT."""
    topic: str
    slide_count: int = 5
    audience: str = "University Students"

# --- API Endpoints ---

@app.get("/", tags=["General"])
async def read_root():
    """A simple health check endpoint."""
    return {"status": "OK", "message": "AI Content Generator API is running!"}


@app.post("/generate-ppt", tags=["Content Generation"])
async def generate_ppt_endpoint(request: PptRequest):
    """
    Generates and returns a PowerPoint presentation based on a topic.
    """
    model = app_state.get("gemini_model")
    if not model:
        raise HTTPException(
            status_code=503, 
            detail="AI service is not available. Check server logs."
        )

    print(f"Generating content for topic: {request.topic}")
    try:
        # 1. Call the AI to get structured content
        ai_response_json = await generate_slide_content(
            model=model,
            topic=request.topic,
            num_slides=request.slide_count,
            audience=request.audience
        )
        
        if not ai_response_json:
            raise HTTPException(status_code=500, detail="Failed to generate AI content.")

        print(f"Successfully generated AI content. Building PPT...")

        # 2. Build the PowerPoint file from the AI content
        presentation = create_presentation(ai_response_json)

        # 3. Save the presentation to an in-memory buffer
        file_buffer = io.BytesIO()
        presentation.save(file_buffer)
        file_buffer.seek(0) # Rewind the buffer to the beginning

        # 4. Stream the file back to the user
        filename = f"{request.topic.replace(' ', '_')}.pptx"
        headers = {
            'Content-Disposition': f'attachment; filename="{filename}"'
        }

        return StreamingResponse(
            file_buffer,
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            headers=headers
        )

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))
